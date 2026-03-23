// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/controller_state.h"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'tcp_pose'
// Member 'reference_tcp_pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'tcp_velocity'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'reference_joint_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__struct.h"
// Member 'target_mode'
#include "aic_control_interfaces/msg/detail/target_mode__struct.h"
// Member 'fts_tare_offset'
#include "geometry_msgs/msg/detail/wrench_stamped__struct.h"

/// Struct defined in msg/ControllerState in the package aic_control_interfaces.
/**
  * Current state of the AIC Controller which includes the computed cartesian and joint commands
 */
typedef struct aic_control_interfaces__msg__ControllerState
{
  /// Header
  std_msgs__msg__Header header;
  /// Current tcp pose.
  geometry_msgs__msg__Pose tcp_pose;
  /// Current tcp velocity.
  geometry_msgs__msg__Twist tcp_velocity;
  /// Reference tcp pose.
  geometry_msgs__msg__Pose reference_tcp_pose;
  /// Pose error from current to target tool pose in the form of (x,y,z,rx,ry,rz)
  double tcp_error[6];
  /// Reference joint state commands
  trajectory_msgs__msg__JointTrajectoryPoint reference_joint_state;
  /// Current mode for target execution
  aic_control_interfaces__msg__TargetMode target_mode;
  /// Tare offset for force torque sensor.
  /// header.frame_id: The reference coordinate frame of the tare values.
  geometry_msgs__msg__WrenchStamped fts_tare_offset;
} aic_control_interfaces__msg__ControllerState;

// Struct for a sequence of aic_control_interfaces__msg__ControllerState.
typedef struct aic_control_interfaces__msg__ControllerState__Sequence
{
  aic_control_interfaces__msg__ControllerState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__msg__ControllerState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_H_
