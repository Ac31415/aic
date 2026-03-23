// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_model_interfaces/msg/observation.h"


#ifndef AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_H_
#define AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'left_image'
// Member 'center_image'
// Member 'right_image'
#include "sensor_msgs/msg/detail/image__struct.h"
// Member 'left_camera_info'
// Member 'center_camera_info'
// Member 'right_camera_info'
#include "sensor_msgs/msg/detail/camera_info__struct.h"
// Member 'wrist_wrench'
#include "geometry_msgs/msg/detail/wrench_stamped__struct.h"
// Member 'joint_states'
#include "sensor_msgs/msg/detail/joint_state__struct.h"
// Member 'controller_state'
#include "aic_control_interfaces/msg/detail/controller_state__struct.h"

/// Struct defined in msg/Observation in the package aic_model_interfaces.
typedef struct aic_model_interfaces__msg__Observation
{
  sensor_msgs__msg__Image left_image;
  sensor_msgs__msg__CameraInfo left_camera_info;
  sensor_msgs__msg__Image center_image;
  sensor_msgs__msg__CameraInfo center_camera_info;
  sensor_msgs__msg__Image right_image;
  sensor_msgs__msg__CameraInfo right_camera_info;
  geometry_msgs__msg__WrenchStamped wrist_wrench;
  sensor_msgs__msg__JointState joint_states;
  aic_control_interfaces__msg__ControllerState controller_state;
} aic_model_interfaces__msg__Observation;

// Struct for a sequence of aic_model_interfaces__msg__Observation.
typedef struct aic_model_interfaces__msg__Observation__Sequence
{
  aic_model_interfaces__msg__Observation * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_model_interfaces__msg__Observation__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_H_
