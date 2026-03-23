// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from aic_control_interfaces:srv/ChangeTargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/srv/change_target_mode.h"


#ifndef AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__STRUCT_H_
#define AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_mode'
#include "aic_control_interfaces/msg/detail/target_mode__struct.h"

/// Struct defined in srv/ChangeTargetMode in the package aic_control_interfaces.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Request
{
  /// Mode for target execution
  aic_control_interfaces__msg__TargetMode target_mode;
} aic_control_interfaces__srv__ChangeTargetMode_Request;

// Struct for a sequence of aic_control_interfaces__srv__ChangeTargetMode_Request.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Request__Sequence
{
  aic_control_interfaces__srv__ChangeTargetMode_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__srv__ChangeTargetMode_Request__Sequence;

// Constants defined in the message

/// Struct defined in srv/ChangeTargetMode in the package aic_control_interfaces.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Response
{
  /// indicate successful change of target mode
  bool success;
} aic_control_interfaces__srv__ChangeTargetMode_Response;

// Struct for a sequence of aic_control_interfaces__srv__ChangeTargetMode_Response.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Response__Sequence
{
  aic_control_interfaces__srv__ChangeTargetMode_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__srv__ChangeTargetMode_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  aic_control_interfaces__srv__ChangeTargetMode_Event__request__MAX_SIZE = 1
};
// response
enum
{
  aic_control_interfaces__srv__ChangeTargetMode_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/ChangeTargetMode in the package aic_control_interfaces.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Event
{
  service_msgs__msg__ServiceEventInfo info;
  aic_control_interfaces__srv__ChangeTargetMode_Request__Sequence request;
  aic_control_interfaces__srv__ChangeTargetMode_Response__Sequence response;
} aic_control_interfaces__srv__ChangeTargetMode_Event;

// Struct for a sequence of aic_control_interfaces__srv__ChangeTargetMode_Event.
typedef struct aic_control_interfaces__srv__ChangeTargetMode_Event__Sequence
{
  aic_control_interfaces__srv__ChangeTargetMode_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} aic_control_interfaces__srv__ChangeTargetMode_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__STRUCT_H_
