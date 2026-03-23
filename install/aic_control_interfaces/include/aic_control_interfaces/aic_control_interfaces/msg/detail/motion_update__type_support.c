// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_control_interfaces/msg/detail/motion_update__rosidl_typesupport_introspection_c.h"
#include "aic_control_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_control_interfaces/msg/detail/motion_update__functions.h"
#include "aic_control_interfaces/msg/detail/motion_update__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `pose`
#include "geometry_msgs/msg/pose.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `velocity`
#include "geometry_msgs/msg/twist.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/twist__rosidl_typesupport_introspection_c.h"
// Member `feedforward_wrench_at_tip`
#include "geometry_msgs/msg/wrench.h"
// Member `feedforward_wrench_at_tip`
#include "geometry_msgs/msg/detail/wrench__rosidl_typesupport_introspection_c.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/trajectory_generation_mode.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_control_interfaces__msg__MotionUpdate__init(message_memory);
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_fini_function(void * message_memory)
{
  aic_control_interfaces__msg__MotionUpdate__fini(message_memory);
}

size_t aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__target_stiffness(
  const void * untyped_member)
{
  (void)untyped_member;
  return 36;
}

const void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_stiffness(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_stiffness(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__target_stiffness(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_stiffness(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__target_stiffness(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_stiffness(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__target_damping(
  const void * untyped_member)
{
  (void)untyped_member;
  return 36;
}

const void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_damping(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_damping(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__target_damping(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_damping(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__target_damping(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_damping(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

size_t aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__wrench_feedback_gains_at_tip(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__wrench_feedback_gains_at_tip(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__wrench_feedback_gains_at_tip(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__wrench_feedback_gains_at_tip(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__wrench_feedback_gains_at_tip(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__wrench_feedback_gains_at_tip(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__wrench_feedback_gains_at_tip(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_stiffness",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    36,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, target_stiffness),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__target_stiffness,  // size() function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_stiffness,  // get_const(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_stiffness,  // get(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__target_stiffness,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__target_stiffness,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_damping",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    36,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, target_damping),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__target_damping,  // size() function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__target_damping,  // get_const(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__target_damping,  // get(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__target_damping,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__target_damping,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedforward_wrench_at_tip",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, feedforward_wrench_at_tip),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "wrench_feedback_gains_at_tip",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, wrench_feedback_gains_at_tip),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__size_function__MotionUpdate__wrench_feedback_gains_at_tip,  // size() function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_const_function__MotionUpdate__wrench_feedback_gains_at_tip,  // get_const(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__get_function__MotionUpdate__wrench_feedback_gains_at_tip,  // get(index) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__fetch_function__MotionUpdate__wrench_feedback_gains_at_tip,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__assign_function__MotionUpdate__wrench_feedback_gains_at_tip,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "trajectory_generation_mode",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__MotionUpdate, trajectory_generation_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_members = {
  "aic_control_interfaces__msg",  // message namespace
  "MotionUpdate",  // message name
  8,  // number of fields
  sizeof(aic_control_interfaces__msg__MotionUpdate),
  false,  // has_any_key_member_
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array,  // message members
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_type_support_handle = {
  0,
  &aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__MotionUpdate__get_type_hash,
  &aic_control_interfaces__msg__MotionUpdate__get_type_description,
  &aic_control_interfaces__msg__MotionUpdate__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_control_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, MotionUpdate)() {
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Wrench)();
  aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, TrajectoryGenerationMode)();
  if (!aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_type_support_handle.typesupport_identifier) {
    aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_control_interfaces__msg__MotionUpdate__rosidl_typesupport_introspection_c__MotionUpdate_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
