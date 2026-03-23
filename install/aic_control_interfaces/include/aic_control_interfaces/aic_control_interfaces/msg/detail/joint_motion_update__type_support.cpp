// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "aic_control_interfaces/msg/detail/joint_motion_update__functions.h"
#include "aic_control_interfaces/msg/detail/joint_motion_update__struct.hpp"
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

void JointMotionUpdate_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) aic_control_interfaces::msg::JointMotionUpdate(_init);
}

void JointMotionUpdate_fini_function(void * message_memory)
{
  auto typed_message = static_cast<aic_control_interfaces::msg::JointMotionUpdate *>(message_memory);
  typed_message->~JointMotionUpdate();
}

size_t size_function__JointMotionUpdate__target_stiffness(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__JointMotionUpdate__target_stiffness(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__JointMotionUpdate__target_stiffness(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__JointMotionUpdate__target_stiffness(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__JointMotionUpdate__target_stiffness(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__JointMotionUpdate__target_stiffness(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__JointMotionUpdate__target_stiffness(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__JointMotionUpdate__target_stiffness(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__JointMotionUpdate__target_damping(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__JointMotionUpdate__target_damping(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__JointMotionUpdate__target_damping(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__JointMotionUpdate__target_damping(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__JointMotionUpdate__target_damping(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__JointMotionUpdate__target_damping(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__JointMotionUpdate__target_damping(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__JointMotionUpdate__target_damping(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__JointMotionUpdate__target_feedforward_torque(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__JointMotionUpdate__target_feedforward_torque(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__JointMotionUpdate__target_feedforward_torque(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__JointMotionUpdate__target_feedforward_torque(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__JointMotionUpdate__target_feedforward_torque(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__JointMotionUpdate__target_feedforward_torque(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__JointMotionUpdate__target_feedforward_torque(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__JointMotionUpdate__target_feedforward_torque(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember JointMotionUpdate_message_member_array[5] = {
  {
    "target_state",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<trajectory_msgs::msg::JointTrajectoryPoint>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::JointMotionUpdate, target_state),  // bytes offset in struct
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
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::JointMotionUpdate, target_stiffness),  // bytes offset in struct
    nullptr,  // default value
    size_function__JointMotionUpdate__target_stiffness,  // size() function pointer
    get_const_function__JointMotionUpdate__target_stiffness,  // get_const(index) function pointer
    get_function__JointMotionUpdate__target_stiffness,  // get(index) function pointer
    fetch_function__JointMotionUpdate__target_stiffness,  // fetch(index, &value) function pointer
    assign_function__JointMotionUpdate__target_stiffness,  // assign(index, value) function pointer
    resize_function__JointMotionUpdate__target_stiffness  // resize(index) function pointer
  },
  {
    "target_damping",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::JointMotionUpdate, target_damping),  // bytes offset in struct
    nullptr,  // default value
    size_function__JointMotionUpdate__target_damping,  // size() function pointer
    get_const_function__JointMotionUpdate__target_damping,  // get_const(index) function pointer
    get_function__JointMotionUpdate__target_damping,  // get(index) function pointer
    fetch_function__JointMotionUpdate__target_damping,  // fetch(index, &value) function pointer
    assign_function__JointMotionUpdate__target_damping,  // assign(index, value) function pointer
    resize_function__JointMotionUpdate__target_damping  // resize(index) function pointer
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
    offsetof(aic_control_interfaces::msg::JointMotionUpdate, trajectory_generation_mode),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "target_feedforward_torque",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_control_interfaces::msg::JointMotionUpdate, target_feedforward_torque),  // bytes offset in struct
    nullptr,  // default value
    size_function__JointMotionUpdate__target_feedforward_torque,  // size() function pointer
    get_const_function__JointMotionUpdate__target_feedforward_torque,  // get_const(index) function pointer
    get_function__JointMotionUpdate__target_feedforward_torque,  // get(index) function pointer
    fetch_function__JointMotionUpdate__target_feedforward_torque,  // fetch(index, &value) function pointer
    assign_function__JointMotionUpdate__target_feedforward_torque,  // assign(index, value) function pointer
    resize_function__JointMotionUpdate__target_feedforward_torque  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers JointMotionUpdate_message_members = {
  "aic_control_interfaces::msg",  // message namespace
  "JointMotionUpdate",  // message name
  5,  // number of fields
  sizeof(aic_control_interfaces::msg::JointMotionUpdate),
  false,  // has_any_key_member_
  JointMotionUpdate_message_member_array,  // message members
  JointMotionUpdate_init_function,  // function to initialize message memory (memory has to be allocated)
  JointMotionUpdate_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t JointMotionUpdate_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &JointMotionUpdate_message_members,
  get_message_typesupport_handle_function,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_hash,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_description,
  &aic_control_interfaces__msg__JointMotionUpdate__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace aic_control_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<aic_control_interfaces::msg::JointMotionUpdate>()
{
  return &::aic_control_interfaces::msg::rosidl_typesupport_introspection_cpp::JointMotionUpdate_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, aic_control_interfaces, msg, JointMotionUpdate)() {
  return &::aic_control_interfaces::msg::rosidl_typesupport_introspection_cpp::JointMotionUpdate_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
