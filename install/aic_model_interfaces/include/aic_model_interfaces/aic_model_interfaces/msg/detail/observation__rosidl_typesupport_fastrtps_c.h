// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice
#ifndef AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "aic_model_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "aic_model_interfaces/msg/detail/observation__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
bool cdr_serialize_aic_model_interfaces__msg__Observation(
  const aic_model_interfaces__msg__Observation * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
bool cdr_deserialize_aic_model_interfaces__msg__Observation(
  eprosima::fastcdr::Cdr &,
  aic_model_interfaces__msg__Observation * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
size_t get_serialized_size_aic_model_interfaces__msg__Observation(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
size_t max_serialized_size_aic_model_interfaces__msg__Observation(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
bool cdr_serialize_key_aic_model_interfaces__msg__Observation(
  const aic_model_interfaces__msg__Observation * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
size_t get_serialized_size_key_aic_model_interfaces__msg__Observation(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
size_t max_serialized_size_key_aic_model_interfaces__msg__Observation(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_aic_model_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, aic_model_interfaces, msg, Observation)();

#ifdef __cplusplus
}
#endif

#endif  // AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
