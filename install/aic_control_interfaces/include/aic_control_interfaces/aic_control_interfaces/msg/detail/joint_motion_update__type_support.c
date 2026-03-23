// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_control_interfaces/msg/detail/joint_motion_update__rosidl_typesupport_introspection_c.h"
#include "aic_control_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_control_interfaces/msg/detail/joint_motion_update__functions.h"
#include "aic_control_interfaces/msg/detail/joint_motion_update__struct.h"


// Include directives for member types
// Member `target_state`
#include "trajectory_msgs/msg/joint_trajectory_point.h"
// Member `target_state`
#include "trajectory_msgs/msg/detail/joint_trajectory_point__rosidl_typesupport_introspection_c.h"
// Member `target_stiffness`
// Member `target_damping`
// Member `target_feedforward_torque`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/trajectory_generation_mode.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_control_interfaces__msg__JointMotionUpdate__init(message_memory);
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_fini_function(void * message_memory)
{
  aic_control_interfaces__msg__JointMotionUpdate__fini(message_memory);
}

size_t aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_stiffness(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_stiffness(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_stiffness(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_stiffness(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_stiffness(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_stiffness(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_stiffness(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_stiffness(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_damping(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_damping(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_damping(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_damping(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_damping(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_damping(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_damping(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_damping(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_feedforward_torque(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_feedforward_torque(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_feedforward_torque(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_feedforward_torque(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_feedforward_torque(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_feedforward_torque(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_feedforward_torque(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_feedforward_torque(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_member_array[5] = {
  {
    "target_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__JointMotionUpdate, target_state),  // bytes offset in struct
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
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__JointMotionUpdate, target_stiffness),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_stiffness,  // size() function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_stiffness,  // get_const(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_stiffness,  // get(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_stiffness,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_stiffness,  // assign(index, value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_stiffness  // resize(index) function pointer
  },
  {
    "target_damping",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__JointMotionUpdate, target_damping),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_damping,  // size() function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_damping,  // get_const(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_damping,  // get(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_damping,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_damping,  // assign(index, value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_damping  // resize(index) function pointer
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
    offsetof(aic_control_interfaces__msg__JointMotionUpdate, trajectory_generation_mode),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_feedforward_torque",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces__msg__JointMotionUpdate, target_feedforward_torque),  // bytes offset in struct
    NULL,  // default value
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__size_function__JointMotionUpdate__target_feedforward_torque,  // size() function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_const_function__JointMotionUpdate__target_feedforward_torque,  // get_const(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__get_function__JointMotionUpdate__target_feedforward_torque,  // get(index) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__fetch_function__JointMotionUpdate__target_feedforward_torque,  // fetch(index, &value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__assign_function__JointMotionUpdate__target_feedforward_torque,  // assign(index, value) function pointer
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__resize_function__JointMotionUpdate__target_feedforward_torque  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_members = {
  "aic_control_interfaces__msg",  // message namespace
  "JointMotionUpdate",  // message name
  5,  // number of fields
  sizeof(aic_control_interfaces__msg__JointMotionUpdate),
  false,  // has_any_key_member_
  aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_member_array,  // message members
  aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_type_support_handle = {
  0,
  &aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_hash,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_description,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_control_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, JointMotionUpdate)() {
  aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, trajectory_msgs, msg, JointTrajectoryPoint)();
  aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, TrajectoryGenerationMode)();
  if (!aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_type_support_handle.typesupport_identifier) {
    aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_control_interfaces__msg__JointMotionUpdate__rosidl_typesupport_introspection_c__JointMotionUpdate_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
