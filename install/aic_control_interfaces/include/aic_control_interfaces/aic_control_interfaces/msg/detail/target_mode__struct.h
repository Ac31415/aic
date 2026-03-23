// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:msg/TargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/target_mode.h"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__STRUCT_H_

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
  aic_control_interfaces__msg__TargetMode__MODE_UNSPECIFIED = 0
};

/// Constant 'MODE_CARTESIAN'.
enum
{
  aic_control_interfaces__msg__TargetMode__MODE_CARTESIAN = 1
};

/// Constant 'MODE_JOINT'.
enum
{
  aic_control_interfaces__msg__TargetMode__MODE_JOINT = 2
};

/// Struct defined in msg/TargetMode in the package aic_control_interfaces.
/**
  * There are two types of target modes.
  *   1. target_mode = MODE_CARTESIAN
  *      The controller will process Cartesian targets of type 'MotionUpdate' and 
  *      ignore other target types
  *   2. target_mode = MODE_JOINT
  *      The controller will process joint targets of type 'JointMotionUpdate' and 
  *      ignore other target types.
 */
typedef struct aic_control_interfaces__msg__TargetMode
{
  uint8_t mode;
} aic_control_interfaces__msg__TargetMode;

// Struct for a sequence of aic_control_interfaces__msg__TargetMode.
typedef struct aic_control_interfaces__msg__TargetMode__Sequence
{
  aic_control_interfaces__msg__TargetMode * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__msg__TargetMode__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__STRUCT_H_
