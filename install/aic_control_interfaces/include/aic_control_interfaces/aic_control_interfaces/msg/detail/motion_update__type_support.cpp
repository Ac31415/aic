// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "aic_control_interfaces/msg/detail/motion_update__functions.h"
#include "aic_control_interfaces/msg/detail/motion_update__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace aic_control_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void MotionUpdate_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aic_control_interfaces::msg::MotionUpdate(_init);
}

void MotionUpdate_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aic_control_interfaces::msg::MotionUpdate *>(message_memory);
  typed_message->~MotionUpdate();
}

size_t size_function__MotionUpdate__target_stiffness(const void * untyped_member)
{
  (void)untyped_member;
  return 36;
}

const void * get_const_function__MotionUpdate__target_stiffness(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionUpdate__target_stiffness(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionUpdate__target_stiffness(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__MotionUpdate__target_stiffness(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__MotionUpdate__target_stiffness(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__MotionUpdate__target_stiffness(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__MotionUpdate__target_damping(const void * untyped_member)
{
  (void)untyped_member;
  return 36;
}

const void * get_const_function__MotionUpdate__target_damping(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionUpdate__target_damping(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 36> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionUpdate__target_damping(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__MotionUpdate__target_damping(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__MotionUpdate__target_damping(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__MotionUpdate__target_damping(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__MotionUpdate__wrench_feedback_gains_at_tip(const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * get_const_function__MotionUpdate__wrench_feedback_gains_at_tip(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void * get_function__MotionUpdate__wrench_feedback_gains_at_tip(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 6> *>(untyped_member);
  return &member[index];
}

void fetch_function__MotionUpdate__wrench_feedback_gains_at_tip(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__MotionUpdate__wrench_feedback_gains_at_tip(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__MotionUpdate__wrench_feedback_gains_at_tip(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__MotionUpdate__wrench_feedback_gains_at_tip(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember MotionUpdate_message_member_array[8] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Pose>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Twist>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, velocity),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "target_stiffness",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    36,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, target_stiffness),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionUpdate__target_stiffness,  // size() function pointer
    get_const_function__MotionUpdate__target_stiffness,  // get_const(index) function pointer
    get_function__MotionUpdate__target_stiffness,  // get(index) function pointer
    fetch_function__MotionUpdate__target_stiffness,  // fetch(index, &value) function pointer
    assign_function__MotionUpdate__target_stiffness,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "target_damping",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    36,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, target_damping),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionUpdate__target_damping,  // size() function pointer
    get_const_function__MotionUpdate__target_damping,  // get_const(index) function pointer
    get_function__MotionUpdate__target_damping,  // get(index) function pointer
    fetch_function__MotionUpdate__target_damping,  // fetch(index, &value) function pointer
    assign_function__MotionUpdate__target_damping,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "feedforward_wrench_at_tip",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Wrench>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, feedforward_wrench_at_tip),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "wrench_feedback_gains_at_tip",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, wrench_feedback_gains_at_tip),  // bytes offset in struct
    nullptr,  // default value
    size_function__MotionUpdate__wrench_feedback_gains_at_tip,  // size() function pointer
    get_const_function__MotionUpdate__wrench_feedback_gains_at_tip,  // get_const(index) function pointer
    get_function__MotionUpdate__wrench_feedback_gains_at_tip,  // get(index) function pointer
    fetch_function__MotionUpdate__wrench_feedback_gains_at_tip,  // fetch(index, &value) function pointer
    assign_function__MotionUpdate__wrench_feedback_gains_at_tip,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "trajectory_generation_mode",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<aic_control_interfaces::msg::TrajectoryGenerationMode>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::MotionUpdate, trajectory_generation_mode),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers MotionUpdate_message_members = {
  "aic_control_interfaces::msg",  // message namespace
  "MotionUpdate",  // message name
  8,  // number of fields
  sizeof(aic_control_interfaces::msg::MotionUpdate),
  false,  // has_any_key_member_
  MotionUpdate_message_member_array,  // message members
  MotionUpdate_init_function,  // function to initialize message memory (memory has to be allocated)
  MotionUpdate_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t MotionUpdate_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &MotionUpdate_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__MotionUpdate__get_type_hash,
  &aic_control_interfaces__msg__MotionUpdate__get_type_description,
  &aic_control_interfaces__msg__MotionUpdate__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace aic_control_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aic_control_interfaces::msg::MotionUpdate>()
{
  return &::aic_control_interfaces::msg::rosidl_typesupport_introspection_cpp::MotionUpdate_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aic_control_interfaces, msg, MotionUpdate)() {
  return &::aic_control_interfaces::msg::rosidl_typesupport_introspection_cpp::MotionUpdate_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
