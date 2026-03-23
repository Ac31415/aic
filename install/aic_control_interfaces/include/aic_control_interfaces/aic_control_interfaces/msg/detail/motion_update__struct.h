// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/motion_update.h"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_H_

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
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__struct.h"
// Member 'feedforward_wrench_at_tip'
#include "geometry_msgs/msg/detail/wrench__struct.h"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.h"

/// Struct defined in msg/MotionUpdate in the package aic_control_interfaces.
/**
  * Command the robot to a target cartesian state.
 */
typedef struct aic_control_interfaces__msg__MotionUpdate
{
  /// Header
  std_msgs__msg__Header header;
  /// Note: These targets are used according to the trajectory_generation_mode specified below.
  /// Pose target.
  geometry_msgs__msg__Pose pose;
  /// Velocity target.
  geometry_msgs__msg__Twist velocity;
  /// Impedance matrices for Cartesian impedance control.
  /// 6x6 row-major matrix
  double target_stiffness[36];
  /// 6x6 row-major matrix
  double target_damping[36];
  geometry_msgs__msg__Wrench feedforward_wrench_at_tip;
  /// Feedback gains of force feedback control. These gains must be in [0, 0.95]
  /// to minimize risk of instability.
  double wrench_feedback_gains_at_tip[6];
  /// The mode of trajectory generation.
  aic_control_interfaces__msg__TrajectoryGenerationMode trajectory_generation_mode;
} aic_control_interfaces__msg__MotionUpdate;

// Struct for a sequence of aic_control_interfaces__msg__MotionUpdate.
typedef struct aic_control_interfaces__msg__MotionUpdate__Sequence
{
  aic_control_interfaces__msg__MotionUpdate * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__msg__MotionUpdate__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_H_
