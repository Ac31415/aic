// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_control_interfaces/msg/detail/controller_state__rosidl_typesupport_introspection_c.h"
#include "aic_control_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_control_interfaces/msg/detail/controller_state__functions.h"
#include "aic_control_interfaces/msg/detail/controller_state__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `tcp_pose`
// Member `reference_tcp_pose`
#include "geometry_msgs/msg/pose.h"
// Member `tcp_pose`
// Member `reference_tcp_pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `tcp_velocity`
#include "geometry_msgs/msg/twist.h"
// Member `tcp_velocity`
#include "geometry_msgs/msg/detail/twist__rosidl_typesupport_introspection_c.h"
// Member `reference_joint_state`
#include "trajectory_msgs/msg/joint_trajectory_point.h"
// Member `reference_joint_state`
#include "trajectory_msgs/msg/detail/joint_trajectory_point__rosidl_typesupport_introspection_c.h"
// Member `target_mode`
#include "aic_control_interfaces/msg/target_mode.h"
// Member `target_mode`
#include "aic_control_interfaces/msg/detail/target_mode__rosidl_typesupport_introspection_c.h"
// Member `fts_tare_offset`
#include "geometry_msgs/msg/wrench_stamped.h"
// Member `fts_tare_offset`
#include "geometry_msgs/msg/detail/wrench_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_control_interfaces__msg__ControllerState__init(message_memory);
}

void aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_fini_function(void * message_memory)
{
  aic_control_interfaces__msg__ControllerState__fini(message_memory);
}

size_t aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__size_function__ControllerState__tcp_error(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_const_function__ControllerState__tcp_error(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_function__ControllerState__tcp_error(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__fetch_function__ControllerState__tcp_error(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_const_function__ControllerState__tcp_error(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__assign_function__ControllerState__tcp_error(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_function__ControllerState__tcp_error(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tcp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, tcp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tcp_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, tcp_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reference_tcp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, reference_tcp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "tcp_error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, tcp_error),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__size_function__ControllerState__tcp_error,  // size() function pointer
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_const_function__ControllerState__tcp_error,  // get_const(index) function pointer
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__get_function__ControllerState__tcp_error,  // get(index) function pointer
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__fetch_function__ControllerState__tcp_error,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__assign_function__ControllerState__tcp_error,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reference_joint_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, reference_joint_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, target_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "fts_tare_offset",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__ControllerState, fts_tare_offset),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_members = {
  "aic_control_interfaces__msg",  // message namespace
  "ControllerState",  // message name
  8,  // number of fields
  sizeof(aic_control_interfaces__msg__ControllerState),
  false,  // has_any_key_member_
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array,  // message members
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_type_support_handle = {
  0,
  &aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__ControllerState__get_type_hash,
  &aic_control_interfaces__msg__ControllerState__get_type_description,
  &aic_control_interfaces__msg__ControllerState__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_control_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, ControllerState)() {
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trajectory_msgs, msg, JointTrajectoryPoint)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, TargetMode)();
  aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, WrenchStamped)();
  if (!aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_type_support_handle.typesupport_identifier) {
    aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_control_interfaces__msg__ControllerState__rosidl_typesupport_introspection_c__ControllerState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
