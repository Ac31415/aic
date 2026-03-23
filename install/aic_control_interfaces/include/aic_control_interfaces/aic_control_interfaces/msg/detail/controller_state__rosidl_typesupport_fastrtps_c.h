// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice
#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "aic_control_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "aic_control_interfaces/msg/detail/controller_state__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
bool cdr_serialize_aic_control_interfaces__msg__ControllerState(
  const aic_control_interfaces__msg__ControllerState * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
bool cdr_deserialize_aic_control_interfaces__msg__ControllerState(
  eprosima::fastcdr::Cdr &,
  aic_control_interfaces__msg__ControllerState * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
size_t get_serialized_size_aic_control_interfaces__msg__ControllerState(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
size_t max_serialized_size_aic_control_interfaces__msg__ControllerState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
bool cdr_serialize_key_aic_control_interfaces__msg__ControllerState(
  const aic_control_interfaces__msg__ControllerState * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
size_t get_serialized_size_key_aic_control_interfaces__msg__ControllerState(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
size_t max_serialized_size_key_aic_control_interfaces__msg__ControllerState(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_control_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, aic_control_interfaces, msg, ControllerState)();

#ifdef __cplusplus
}
#endif

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
