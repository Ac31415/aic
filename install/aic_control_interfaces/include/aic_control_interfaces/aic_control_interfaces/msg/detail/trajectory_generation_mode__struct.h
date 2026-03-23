// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:msg/TrajectoryGenerationMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/trajectory_generation_mode.h"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Constant 'MODE_UNSPECIFIED'.
enum
{
  aic_control_interfaces__msg__TrajectoryGenerationMode__MODE_UNSPECIFIED = 0
};

/// Constant 'MODE_VELOCITY'.
enum
{
  aic_control_interfaces__msg__TrajectoryGenerationMode__MODE_VELOCITY = 1
};

/// Constant 'MODE_POSITION'.
enum
{
  aic_control_interfaces__msg__TrajectoryGenerationMode__MODE_POSITION = 2
};

/// Struct defined in msg/TrajectoryGenerationMode in the package aic_control_interfaces.
/**
  * There are two ways that input targets can be provided for the MotionUpdate message.
  *   1. mode = MODE_VELOCITY
  *      In this case, a target velocity must be provided. The target pose
  *      will be ignored.
  *   2. mode = MODE_POSITION
  *      In this case, a target pose must be provided. The target velocity
  *      will be ignored.
  * Notes that messages with mode set to MODE_UNSPECIFIED will be ignored.
 */
typedef struct aic_control_interfaces__msg__TrajectoryGenerationMode
{
  uint8_t mode;
} aic_control_interfaces__msg__TrajectoryGenerationMode;

// Struct for a sequence of aic_control_interfaces__msg__TrajectoryGenerationMode.
typedef struct aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence
{
  aic_control_interfaces__msg__TrajectoryGenerationMode * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__STRUCT_H_
