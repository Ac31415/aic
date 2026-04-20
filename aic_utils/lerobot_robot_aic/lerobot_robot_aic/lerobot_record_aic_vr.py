#
#  Copyright (C) 2026 Intrinsic Innovation LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""lerobot-record-vr — LeRobot recording with VR lifecycle management.

This script mirrors ``lerobot-record`` but adds VR-specific lifecycle hooks
around the reset phase so that:

1. **During reset** (scene reload / robot repositioning): VR pose publishing is
   paused.  The AIC controller is not sent any new targets, so the sim can
   reposition the robot freely without fighting VR commands.

2. **At the start of each new episode**: The VR reference frame is re-captured
   from the loaded scene's initial TCP pose, ensuring the robot starts from the
   correct initial position rather than the pose from the previous episode.

This matches the behaviour of the keyboard-teleop version of ``lerobot-record``,
where teleoperation is implicitly "stopped" during reset (zero-velocity commands)
and resumes naturally at episode start.

Usage (same flags as ``lerobot-record``):

    lerobot-record-vr \\
        --robot.type=aic_controller --robot.id=aic \\
        --teleop.type=aic_vr --teleop.id=aic \\
        --robot.teleop_target_mode=vr_cartesian \\
        --dataset.repo_id=<hf-repo> \\
        --dataset.single_task="<task description>" \\
        --dataset.push_to_hub=false \\
        --display_data=true

Note: This script also works transparently with non-VR teleop types; the VR
lifecycle calls (pause / start_episode) are no-ops when the teleop is not an
``AICVRTeleop`` instance.
"""

import logging
from dataclasses import asdict
from pprint import pformat

from lerobot.common.control_utils import (
    init_keyboard_listener,
    is_headless,
    sanity_check_dataset_name,
    sanity_check_dataset_robot_compatibility,
)
from lerobot.configs import parser
from lerobot.datasets import (
    LeRobotDataset,
    VideoEncodingManager,
    aggregate_pipeline_dataset_features,
    create_initial_features,
)
from lerobot.policies import (
    ActionInterpolator,
    make_policy,
    make_pre_post_processors,
)
from lerobot.processor import make_default_processors, rename_stats
from lerobot.robots import make_robot_from_config
from lerobot.scripts.lerobot_record import RecordConfig, record_loop
from lerobot.teleoperators import make_teleoperator_from_config
from lerobot.utils.feature_utils import combine_feature_dicts
from lerobot.utils.import_utils import register_third_party_plugins
from lerobot.utils.utils import init_logging, log_say
from lerobot.utils.visualization_utils import init_rerun

from .aic_teleop import AICVRTeleop


@parser.wrap()
def record_vr(cfg: RecordConfig) -> LeRobotDataset:
    """Record a LeRobot dataset with VR-aware reset-phase management."""
    init_logging()
    logging.info(pformat(asdict(cfg)))
    if cfg.display_data:
        init_rerun(session_name="recording", ip=cfg.display_ip, port=cfg.display_port)
    display_compressed_images = (
        True
        if (cfg.display_data and cfg.display_ip is not None and cfg.display_port is not None)
        else cfg.display_compressed_images
    )

    robot = make_robot_from_config(cfg.robot)
    teleop = make_teleoperator_from_config(cfg.teleop) if cfg.teleop is not None else None

    # Identify VR teleop for lifecycle management (pause / start_episode).
    vr_teleop = teleop if isinstance(teleop, AICVRTeleop) else None

    teleop_action_processor, robot_action_processor, robot_observation_processor = (
        make_default_processors()
    )

    dataset_features = combine_feature_dicts(
        aggregate_pipeline_dataset_features(
            pipeline=teleop_action_processor,
            initial_features=create_initial_features(action=robot.action_features),
            use_videos=cfg.dataset.video,
        ),
        aggregate_pipeline_dataset_features(
            pipeline=robot_observation_processor,
            initial_features=create_initial_features(observation=robot.observation_features),
            use_videos=cfg.dataset.video,
        ),
    )

    dataset = None
    listener = None

    try:
        if cfg.resume:
            num_cameras = len(robot.cameras) if hasattr(robot, "cameras") else 0
            dataset = LeRobotDataset.resume(
                cfg.dataset.repo_id,
                root=cfg.dataset.root,
                batch_encoding_size=cfg.dataset.video_encoding_batch_size,
                vcodec=cfg.dataset.vcodec,
                streaming_encoding=cfg.dataset.streaming_encoding,
                encoder_queue_maxsize=cfg.dataset.encoder_queue_maxsize,
                encoder_threads=cfg.dataset.encoder_threads,
                image_writer_processes=cfg.dataset.num_image_writer_processes
                if num_cameras > 0
                else 0,
                image_writer_threads=cfg.dataset.num_image_writer_threads_per_camera * num_cameras
                if num_cameras > 0
                else 0,
            )
            sanity_check_dataset_robot_compatibility(dataset, robot, cfg.dataset.fps, dataset_features)
        else:
            sanity_check_dataset_name(cfg.dataset.repo_id, cfg.policy)
            dataset = LeRobotDataset.create(
                cfg.dataset.repo_id,
                cfg.dataset.fps,
                root=cfg.dataset.root,
                robot_type=robot.name,
                features=dataset_features,
                use_videos=cfg.dataset.video,
                image_writer_processes=cfg.dataset.num_image_writer_processes,
                image_writer_threads=cfg.dataset.num_image_writer_threads_per_camera
                * len(robot.cameras),
                batch_encoding_size=cfg.dataset.video_encoding_batch_size,
                vcodec=cfg.dataset.vcodec,
                streaming_encoding=cfg.dataset.streaming_encoding,
                encoder_queue_maxsize=cfg.dataset.encoder_queue_maxsize,
                encoder_threads=cfg.dataset.encoder_threads,
            )

        policy = (
            None
            if cfg.policy is None
            else make_policy(cfg.policy, ds_meta=dataset.meta, rename_map=cfg.dataset.rename_map)
        )
        preprocessor = None
        postprocessor = None
        interpolator = None
        if cfg.policy is not None:
            preprocessor, postprocessor = make_pre_post_processors(
                policy_cfg=cfg.policy,
                pretrained_path=cfg.policy.pretrained_path,
                dataset_stats=rename_stats(dataset.meta.stats, cfg.dataset.rename_map),
                preprocessor_overrides={
                    "device_processor": {"device": cfg.policy.device},
                    "rename_observations_processor": {"rename_map": cfg.dataset.rename_map},
                },
            )
            if cfg.interpolation_multiplier > 1:
                interpolator = ActionInterpolator(multiplier=cfg.interpolation_multiplier)
                logging.info(
                    f"Action interpolation enabled: {cfg.interpolation_multiplier}x control rate"
                )

        robot.connect()
        if teleop is not None:
            teleop.connect()

        listener, events = init_keyboard_listener()

        if not cfg.dataset.streaming_encoding:
            logging.info(
                "Streaming encoding is disabled. If you have capable hardware, consider enabling "
                "it for way faster episode saving. --dataset.streaming_encoding=true "
                "--dataset.encoder_threads=2 # --dataset.vcodec=auto. More info in the "
                "documentation: https://huggingface.co/docs/lerobot/streaming_video_encoding"
            )

        with VideoEncodingManager(dataset):
            recorded_episodes = 0
            while recorded_episodes < cfg.dataset.num_episodes and not events["stop_recording"]:
                # ── VR lifecycle: prepare for a new recording episode ─────────────
                # Enters VR TRACKING mode and re-captures the reference TCP pose so
                # the robot starts from the loaded scene's initial position.
                if vr_teleop is not None:
                    vr_teleop.start_episode()

                log_say(f"Recording episode {dataset.num_episodes}", cfg.play_sounds)
                record_loop(
                    robot=robot,
                    events=events,
                    fps=cfg.dataset.fps,
                    teleop_action_processor=teleop_action_processor,
                    robot_action_processor=robot_action_processor,
                    robot_observation_processor=robot_observation_processor,
                    teleop=teleop,
                    policy=policy,
                    preprocessor=preprocessor,
                    postprocessor=postprocessor,
                    dataset=dataset,
                    control_time_s=cfg.dataset.episode_time_s,
                    single_task=cfg.dataset.single_task,
                    display_data=cfg.display_data,
                    interpolator=interpolator,
                    display_compressed_images=display_compressed_images,
                )

                # Execute a few seconds without recording to give time to reset the
                # environment (scene reload / robot repositioning).
                # Skip reset for the last episode to be recorded.
                if not events["stop_recording"] and (
                    (recorded_episodes < cfg.dataset.num_episodes - 1)
                    or events["rerecord_episode"]
                ):
                    # ── VR lifecycle: pause during reset ─────────────────────────
                    # Stops VR publishing so the AIC controller is not disturbed
                    # while the scene is being reloaded.
                    if vr_teleop is not None:
                        vr_teleop.pause()

                    log_say("Reset the environment", cfg.play_sounds)
                    record_loop(
                        robot=robot,
                        events=events,
                        fps=cfg.dataset.fps,
                        teleop_action_processor=teleop_action_processor,
                        robot_action_processor=robot_action_processor,
                        robot_observation_processor=robot_observation_processor,
                        teleop=teleop,
                        control_time_s=cfg.dataset.reset_time_s,
                        single_task=cfg.dataset.single_task,
                        display_data=cfg.display_data,
                    )

                if events["rerecord_episode"]:
                    log_say("Re-record episode", cfg.play_sounds)
                    events["rerecord_episode"] = False
                    events["exit_early"] = False
                    dataset.clear_episode_buffer()
                    continue

                dataset.save_episode()
                recorded_episodes += 1

    finally:
        log_say("Stop recording", cfg.play_sounds, blocking=True)

        if dataset:
            dataset.finalize()

        if robot.is_connected:
            robot.disconnect()
        if teleop and teleop.is_connected:
            teleop.disconnect()

        if not is_headless() and listener:
            listener.stop()

        if cfg.dataset.push_to_hub:
            dataset.push_to_hub(tags=cfg.dataset.tags, private=cfg.dataset.private)

        log_say("Exiting", cfg.play_sounds)

    return dataset


def main():
    register_third_party_plugins()
    record_vr()


if __name__ == "__main__":
    main()
