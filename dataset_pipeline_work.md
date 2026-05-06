cd ~/ws_aic_caai/src/aic
cd oculus_reader/
pixi run python3 oculus_reader/viz_transforms.py





cd ws_aic_caai/src/aic/
export DBX_CONTAINER_MANAGER=docker
distrobox enter -r aic_eval
/entrypoint.sh spawn_task_board:=true     task_board_x:=0.3 task_board_y:=-0.1 task_board_z:=1.2     task_board_roll:=0.0 task_board_pitch:=0.0 task_board_yaw:=0.785     sfp_mount_rail_0_present:=true sfp_mount_rail_0_translation:=-0.08     sc_mount_rail_0_present:=true sc_mount_rail_0_translation:=-0.09     nic_card_mount_0_present:=true nic_card_mount_0_translation:=0.005     sc_port_0_present:=true sc_port_0_translation:=-0.04     spawn_cable:=true cable_type:=sfp_sc_cable attach_cable_to_gripper:=true     ground_truth:=true start_aic_engine:=false






cd ws_aic_caai/src/aic/
pixi run lerobot-record         --robot.type=aic_controller --robot.id=aic         --teleop.type=aic_oculus   --teleop.id=aic         --robot.teleop_target_mode=cartesian         --robot.cartesian_command_mode=position         --teleop.cartesian_command_mode=position         --robot.teleop_frame_id=base_link         --dataset.repo_id=caai-aic/test-dataset          --dataset.single_task="insert cable"         --dataset.push_to_hub=false         --play_sounds=false         --display_data=true 










create a framework that allows users to record robot arm training data to huggingface. specifically, when the user first launches the framework, the following steps would take place:

1. # launch the vr control: #

    the following commands would be run after the user is prompted to connect the quest 3 vr headset to the computer:

    - cd ~/ws_aic_caai/src/aic/oculus_reader/
    - pixi run python3 oculus_reader/viz_transforms.py

2. # launch the mechanism that fetches the info about the existing datasets on the huggingface page: #

    the framework would fetch the info about the following datasets on the huggingface page and display the number of episodes of each datasets (include also the number of episodes left before reaching 100, if the number of episodes of a dataset is greater than or equal to 100, do not display the number of episodes left before reaching 10):

    - caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_0
    - caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_0
    - caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_1
    - caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_1
    - caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_2
    - caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_2
    - caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_3
    - caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_3
    - caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_4
    - caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_4
    - caai-aic/corrected_sc_to_sc_port_base_of_sc_port_0
    - caai-aic/corrected_sc_to_sc_port_base_of_sc_port_1

3. # prompt the user to choose which task to record for: #

    - the user would be asked to choose which task to record for the dataset
    - on this page the user would also have the option to quit the framework

4. # launch the scene and the data record mechanism with appropriate arguments #

    when the user clicks a specific task to record for, the following would take place:

    - the scene would be launched with the following commands:
        - cd ws_aic_caai/src/aic/
        - export DBX_CONTAINER_MANAGER=docker
        - distrobox enter -r aic_eval
        - wait until fully entering the docker container through distrobox
        - /entrypoint.sh [parameters] (where the [parameters] would be randomly generated following the logic of `/home/minghanwei/ws_aic_caai/src/aic/automated scene gen script ref.py`)
    - after the gazebo scene is FULLY LOADED, on another shell session or terminal:
        - cd ws_aic_caai/src/aic/
        - depending on the task chosen, one of the following commands would be run:

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_0 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_0 of nic_card_mount_0" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_0'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_0 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_1 of nic_card_mount_0" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_0'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_1 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_0 of nic_card_mount_1" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_1'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_1 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_1 of nic_card_mount_1" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_1'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_2 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_0 of nic_card_mount_2" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_2'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_2 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_1 of nic_card_mount_2" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_2'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_3 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_0 of nic_card_mount_3" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_3'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_3 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_1 of nic_card_mount_3" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_3'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_4 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_0 of nic_card_mount_4" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_0_of_nic_card_mount_4'

            - pixi run lerobot-record --robot.type=aic_controller --robot.id=aic --teleop.type=aic_oculus --teleop.id=aic --robot.teleop_target_mode=cartesian --robot.cartesian_command_mode=position --teleop.cartesian_command_mode=position --robot.teleop_frame_id=base_link --dataset.push_to_hub=true --dataset.private=true --dataset.num_episodes=[num] --play_sounds=false --display_data=true --dataset.reset_time_s=30 --dataset.episode_time_s=600 --resume=true --dataset.repo_id=caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_4 --dataset.single_task="Insert sfp_tip of sfp_sc into sfp_port_1 of nic_card_mount_4" --dataset.root='/home/minghanwei/.cache/huggingface/lerobot/caai-aic/corrected_sfp_to_sfp_port_1_of_nic_card_mount_4'

        where the [num] value would be set by the user before the recording mechanims is run.

5. # what happens when the user presses the right arrow key 2 times when they try to end the current episode recording: #
    - display BOTH the number of remaining episodes left in the current session, and the total number of episodes left before reaching 100 episodes (if already greater than or equal to 100, do not display this number)

6. # what happens when the user presses the esc key when they try to end the current recording session: #
    - waiting until the recording uploaded to huggingface is complete
    - bring the user back to the page diaplaying the UPDATED number of episodes of each datasets (include also the number of episodes left before reaching 100, if the number of episodes of a dataset is greater than or equal to 100, do not display the number of episodes left before reaching 10), that still allows the user to choose which task to record next.
    - the user would have the option to quit the whole framework here. 
