// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_engine_interfaces:srv/ResetJoints.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_engine_interfaces/srv/detail/reset_joints__rosidl_typesupport_introspection_c.h"
#include "aic_engine_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_engine_interfaces/srv/detail/reset_joints__functions.h"
#include "aic_engine_interfaces/srv/detail/reset_joints__struct.h"


// Include directives for member types
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `initial_positions`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_engine_interfaces__srv__ResetJoints_Request__init(message_memory);
}

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_fini_function(void * message_memory)
{
  aic_engine_interfaces__srv__ResetJoints_Request__fini(message_memory);
}

size_t aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__size_function__ResetJoints_Request__joint_names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__joint_names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__joint_names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Request__joint_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__joint_names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Request__joint_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__joint_names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Request__joint_names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__size_function__ResetJoints_Request__initial_positions(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__initial_positions(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__initial_positions(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Request__initial_positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__initial_positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Request__initial_positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__initial_positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Request__initial_positions(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_member_array[2] = {
  {
    "joint_names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Request, joint_names),  // bytes offset in struct
    NULL,  // default value
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__size_function__ResetJoints_Request__joint_names,  // size() function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__joint_names,  // get_const(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__joint_names,  // get(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Request__joint_names,  // fetch(index, &value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Request__joint_names,  // assign(index, value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Request__joint_names  // resize(index) function pointer
  },
  {
    "initial_positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Request, initial_positions),  // bytes offset in struct
    NULL,  // default value
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__size_function__ResetJoints_Request__initial_positions,  // size() function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Request__initial_positions,  // get_const(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__get_function__ResetJoints_Request__initial_positions,  // get(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Request__initial_positions,  // fetch(index, &value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Request__initial_positions,  // assign(index, value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Request__initial_positions  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_members = {
  "aic_engine_interfaces__srv",  // message namespace
  "ResetJoints_Request",  // message name
  2,  // number of fields
  sizeof(aic_engine_interfaces__srv__ResetJoints_Request),
  false,  // has_any_key_member_
  aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_member_array,  // message members
  aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle = {
  0,
  &aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_members,
  get_message_typesupport_handle_function,
  &aic_engine_interfaces__srv__ResetJoints_Request__get_type_hash,
  &aic_engine_interfaces__srv__ResetJoints_Request__get_type_description,
  &aic_engine_interfaces__srv__ResetJoints_Request__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_engine_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Request)() {
  if (!aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle.typesupport_identifier) {
    aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aic_engine_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__functions.h"
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__struct.h"


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_engine_interfaces__srv__ResetJoints_Response__init(message_memory);
}

void aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_fini_function(void * message_memory)
{
  aic_engine_interfaces__srv__ResetJoints_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_member_array[2] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_members = {
  "aic_engine_interfaces__srv",  // message namespace
  "ResetJoints_Response",  // message name
  2,  // number of fields
  sizeof(aic_engine_interfaces__srv__ResetJoints_Response),
  false,  // has_any_key_member_
  aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_member_array,  // message members
  aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle = {
  0,
  &aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_members,
  get_message_typesupport_handle_function,
  &aic_engine_interfaces__srv__ResetJoints_Response__get_type_hash,
  &aic_engine_interfaces__srv__ResetJoints_Response__get_type_description,
  &aic_engine_interfaces__srv__ResetJoints_Response__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_engine_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Response)() {
  if (!aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle.typesupport_identifier) {
    aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__rosidl_typesupport_introspection_c.h"
// already included above
// #include "aic_engine_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__functions.h"
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__struct.h"


// Include directives for member types
// Member `info`
#include "service_msgs/msg/service_event_info.h"
// Member `info`
#include "service_msgs/msg/detail/service_event_info__rosidl_typesupport_introspection_c.h"
// Member `request`
// Member `response`
#include "aic_engine_interfaces/srv/reset_joints.h"
// Member `request`
// Member `response`
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_engine_interfaces__srv__ResetJoints_Event__init(message_memory);
}

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_fini_function(void * message_memory)
{
  aic_engine_interfaces__srv__ResetJoints_Event__fini(message_memory);
}

size_t aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__size_function__ResetJoints_Event__request(
  const void * untyped_member)
{
  const aic_engine_interfaces__srv__ResetJoints_Request__Sequence * member =
    (const aic_engine_interfaces__srv__ResetJoints_Request__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__request(
  const void * untyped_member, size_t index)
{
  const aic_engine_interfaces__srv__ResetJoints_Request__Sequence * member =
    (const aic_engine_interfaces__srv__ResetJoints_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__request(
  void * untyped_member, size_t index)
{
  aic_engine_interfaces__srv__ResetJoints_Request__Sequence * member =
    (aic_engine_interfaces__srv__ResetJoints_Request__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Event__request(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aic_engine_interfaces__srv__ResetJoints_Request * item =
    ((const aic_engine_interfaces__srv__ResetJoints_Request *)
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__request(untyped_member, index));
  aic_engine_interfaces__srv__ResetJoints_Request * value =
    (aic_engine_interfaces__srv__ResetJoints_Request *)(untyped_value);
  *value = *item;
}

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Event__request(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aic_engine_interfaces__srv__ResetJoints_Request * item =
    ((aic_engine_interfaces__srv__ResetJoints_Request *)
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__request(untyped_member, index));
  const aic_engine_interfaces__srv__ResetJoints_Request * value =
    (const aic_engine_interfaces__srv__ResetJoints_Request *)(untyped_value);
  *item = *value;
}

bool aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Event__request(
  void * untyped_member, size_t size)
{
  aic_engine_interfaces__srv__ResetJoints_Request__Sequence * member =
    (aic_engine_interfaces__srv__ResetJoints_Request__Sequence *)(untyped_member);
  aic_engine_interfaces__srv__ResetJoints_Request__Sequence__fini(member);
  return aic_engine_interfaces__srv__ResetJoints_Request__Sequence__init(member, size);
}

size_t aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__size_function__ResetJoints_Event__response(
  const void * untyped_member)
{
  const aic_engine_interfaces__srv__ResetJoints_Response__Sequence * member =
    (const aic_engine_interfaces__srv__ResetJoints_Response__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__response(
  const void * untyped_member, size_t index)
{
  const aic_engine_interfaces__srv__ResetJoints_Response__Sequence * member =
    (const aic_engine_interfaces__srv__ResetJoints_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__response(
  void * untyped_member, size_t index)
{
  aic_engine_interfaces__srv__ResetJoints_Response__Sequence * member =
    (aic_engine_interfaces__srv__ResetJoints_Response__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Event__response(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const aic_engine_interfaces__srv__ResetJoints_Response * item =
    ((const aic_engine_interfaces__srv__ResetJoints_Response *)
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__response(untyped_member, index));
  aic_engine_interfaces__srv__ResetJoints_Response * value =
    (aic_engine_interfaces__srv__ResetJoints_Response *)(untyped_value);
  *value = *item;
}

void aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Event__response(
  void * untyped_member, size_t index, const void * untyped_value)
{
  aic_engine_interfaces__srv__ResetJoints_Response * item =
    ((aic_engine_interfaces__srv__ResetJoints_Response *)
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__response(untyped_member, index));
  const aic_engine_interfaces__srv__ResetJoints_Response * value =
    (const aic_engine_interfaces__srv__ResetJoints_Response *)(untyped_value);
  *item = *value;
}

bool aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Event__response(
  void * untyped_member, size_t size)
{
  aic_engine_interfaces__srv__ResetJoints_Response__Sequence * member =
    (aic_engine_interfaces__srv__ResetJoints_Response__Sequence *)(untyped_member);
  aic_engine_interfaces__srv__ResetJoints_Response__Sequence__fini(member);
  return aic_engine_interfaces__srv__ResetJoints_Response__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_member_array[3] = {
  {
    "info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Event, info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "request",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Event, request),  // bytes offset in struct
    NULL,  // default value
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__size_function__ResetJoints_Event__request,  // size() function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__request,  // get_const(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__request,  // get(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Event__request,  // fetch(index, &value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Event__request,  // assign(index, value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Event__request  // resize(index) function pointer
  },
  {
    "response",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    1,  // array size
    true,  // is upper bound
    offsetof(aic_engine_interfaces__srv__ResetJoints_Event, response),  // bytes offset in struct
    NULL,  // default value
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__size_function__ResetJoints_Event__response,  // size() function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_const_function__ResetJoints_Event__response,  // get_const(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__get_function__ResetJoints_Event__response,  // get(index) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__fetch_function__ResetJoints_Event__response,  // fetch(index, &value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__assign_function__ResetJoints_Event__response,  // assign(index, value) function pointer
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__resize_function__ResetJoints_Event__response  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_members = {
  "aic_engine_interfaces__srv",  // message namespace
  "ResetJoints_Event",  // message name
  3,  // number of fields
  sizeof(aic_engine_interfaces__srv__ResetJoints_Event),
  false,  // has_any_key_member_
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_member_array,  // message members
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_type_support_handle = {
  0,
  &aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_members,
  get_message_typesupport_handle_function,
  &aic_engine_interfaces__srv__ResetJoints_Event__get_type_hash,
  &aic_engine_interfaces__srv__ResetJoints_Event__get_type_description,
  &aic_engine_interfaces__srv__ResetJoints_Event__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_engine_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Event)() {
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, service_msgs, msg, ServiceEventInfo)();
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Request)();
  aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Response)();
  if (!aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_type_support_handle.typesupport_identifier) {
    aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "aic_engine_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "aic_engine_interfaces/srv/detail/reset_joints__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_members = {
  "aic_engine_interfaces__srv",  // service namespace
  "ResetJoints",  // service name
  // the following fields are initialized below on first access
  NULL,  // request message
  // aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle,
  NULL,  // response message
  // aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle
  NULL  // event_message
  // aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle
};


static rosidl_service_type_support_t aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_type_support_handle = {
  0,
  &aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_members,
  get_service_typesupport_handle_function,
  &aic_engine_interfaces__srv__ResetJoints_Request__rosidl_typesupport_introspection_c__ResetJoints_Request_message_type_support_handle,
  &aic_engine_interfaces__srv__ResetJoints_Response__rosidl_typesupport_introspection_c__ResetJoints_Response_message_type_support_handle,
  &aic_engine_interfaces__srv__ResetJoints_Event__rosidl_typesupport_introspection_c__ResetJoints_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    aic_engine_interfaces,
    srv,
    ResetJoints
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    aic_engine_interfaces,
    srv,
    ResetJoints
  ),
  &aic_engine_interfaces__srv__ResetJoints__get_type_hash,
  &aic_engine_interfaces__srv__ResetJoints__get_type_description,
  &aic_engine_interfaces__srv__ResetJoints__get_type_description_sources,
};

// Forward declaration of message type support functions for service members
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Request)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Response)(void);

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Event)(void);

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_engine_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints)(void) {
  if (!aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_type_support_handle.typesupport_identifier) {
    aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Response)()->data;
  }
  if (!service_members->event_members_) {
    service_members->event_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_engine_interfaces, srv, ResetJoints_Event)()->data;
  }

  return &aic_engine_interfaces__srv__detail__reset_joints__rosidl_typesupport_introspection_c__ResetJoints_service_type_support_handle;
}
