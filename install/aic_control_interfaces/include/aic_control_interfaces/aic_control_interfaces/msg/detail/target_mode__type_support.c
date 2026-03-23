// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_control_interfaces:msg/TargetMode.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_control_interfaces/msg/detail/target_mode__rosidl_typesupport_introspection_c.h"
#include "aic_control_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_control_interfaces/msg/detail/target_mode__functions.h"
#include "aic_control_interfaces/msg/detail/target_mode__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_control_interfaces__msg__TargetMode__init(message_memory);
}

void aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_fini_function(void * message_memory)
{
  aic_control_interfaces__msg__TargetMode__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_member_array[1] = {
  {
    "mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__TargetMode, mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_members = {
  "aic_control_interfaces__msg",  // message namespace
  "TargetMode",  // message name
  1,  // number of fields
  sizeof(aic_control_interfaces__msg__TargetMode),
  false,  // has_any_key_member_
  aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_member_array,  // message members
  aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_type_support_handle = {
  0,
  &aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__TargetMode__get_type_hash,
  &aic_control_interfaces__msg__TargetMode__get_type_description,
  &aic_control_interfaces__msg__TargetMode__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_control_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, TargetMode)() {
  if (!aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_type_support_handle.typesupport_identifier) {
    aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_control_interfaces__msg__TargetMode__rosidl_typesupport_introspection_c__TargetMode_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
