// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/joint_motion_update.h"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'target_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__struct.h"
// Member 'target_stiffness'
// Member 'target_damping'
// Member 'target_feedforward_torque'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.h"

/// Struct defined in msg/JointMotionUpdate in the package aic_control_interfaces.
/**
  * Command the robot to a target joint state.
 */
typedef struct aic_control_interfaces__msg__JointMotionUpdate
{
  /// The target joint configuration including set points for positions,
  /// velocities, accelerations, and efforts.
  trajectory_msgs__msg__JointTrajectoryPoint target_state;
  /// Stiffness and damping both evolve from a current value toward these target
  /// ones. This avoids sudden jumps when the values are changed.
  /// Specify for each joint.
  rosidl_runtime_c__double__Sequence target_stiffness;
  rosidl_runtime_c__double__Sequence target_damping;
  /// The mode of trajectory generation.
  aic_control_interfaces__msg__TrajectoryGenerationMode trajectory_generation_mode;
  rosidl_runtime_c__double__Sequence target_feedforward_torque;
} aic_control_interfaces__msg__JointMotionUpdate;

// Struct for a sequence of aic_control_interfaces__msg__JointMotionUpdate.
typedef struct aic_control_interfaces__msg__JointMotionUpdate__Sequence
{
  aic_control_interfaces__msg__JointMotionUpdate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__msg__JointMotionUpdate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_H_
