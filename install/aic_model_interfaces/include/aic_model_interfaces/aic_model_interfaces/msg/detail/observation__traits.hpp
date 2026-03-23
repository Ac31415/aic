// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_model_interfaces/msg/observation.hpp"


#ifndef AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__TRAITS_HPP_
#define AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_model_interfaces/msg/detail/observation__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'left_image'
// Member 'center_image'
// Member 'right_image'
#include "sensor_msgs/msg/detail/image__traits.hpp"
// Member 'left_camera_info'
// Member 'center_camera_info'
// Member 'right_camera_info'
#include "sensor_msgs/msg/detail/camera_info__traits.hpp"
// Member 'wrist_wrench'
#include "geometry_msgs/msg/detail/wrench_stamped__traits.hpp"
// Member 'joint_states'
#include "sensor_msgs/msg/detail/joint_state__traits.hpp"
// Member 'controller_state'
#include "aic_control_interfaces/msg/detail/controller_state__traits.hpp"

namespace aic_model_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Observation & msg,
  std::ostream & out)
{
  out << "{";
  // member: left_image
  {
    out << "left_image: ";
    to_flow_style_yaml(msg.left_image, out);
    out << ", ";
  }

  // member: left_camera_info
  {
    out << "left_camera_info: ";
    to_flow_style_yaml(msg.left_camera_info, out);
    out << ", ";
  }

  // member: center_image
  {
    out << "center_image: ";
    to_flow_style_yaml(msg.center_image, out);
    out << ", ";
  }

  // member: center_camera_info
  {
    out << "center_camera_info: ";
    to_flow_style_yaml(msg.center_camera_info, out);
    out << ", ";
  }

  // member: right_image
  {
    out << "right_image: ";
    to_flow_style_yaml(msg.right_image, out);
    out << ", ";
  }

  // member: right_camera_info
  {
    out << "right_camera_info: ";
    to_flow_style_yaml(msg.right_camera_info, out);
    out << ", ";
  }

  // member: wrist_wrench
  {
    out << "wrist_wrench: ";
    to_flow_style_yaml(msg.wrist_wrench, out);
    out << ", ";
  }

  // member: joint_states
  {
    out << "joint_states: ";
    to_flow_style_yaml(msg.joint_states, out);
    out << ", ";
  }

  // member: controller_state
  {
    out << "controller_state: ";
    to_flow_style_yaml(msg.controller_state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Observation & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: left_image
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_image:\n";
    to_block_style_yaml(msg.left_image, out, indentation + 2);
  }

  // member: left_camera_info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "left_camera_info:\n";
    to_block_style_yaml(msg.left_camera_info, out, indentation + 2);
  }

  // member: center_image
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_image:\n";
    to_block_style_yaml(msg.center_image, out, indentation + 2);
  }

  // member: center_camera_info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_camera_info:\n";
    to_block_style_yaml(msg.center_camera_info, out, indentation + 2);
  }

  // member: right_image
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_image:\n";
    to_block_style_yaml(msg.right_image, out, indentation + 2);
  }

  // member: right_camera_info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "right_camera_info:\n";
    to_block_style_yaml(msg.right_camera_info, out, indentation + 2);
  }

  // member: wrist_wrench
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "wrist_wrench:\n";
    to_block_style_yaml(msg.wrist_wrench, out, indentation + 2);
  }

  // member: joint_states
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joint_states:\n";
    to_block_style_yaml(msg.joint_states, out, indentation + 2);
  }

  // member: controller_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "controller_state:\n";
    to_block_style_yaml(msg.controller_state, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Observation & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace aic_model_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use aic_model_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aic_model_interfaces::msg::Observation & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_model_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_model_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_model_interfaces::msg::Observation & msg)
{
  return aic_model_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_model_interfaces::msg::Observation>()
{
  return "aic_model_interfaces::msg::Observation";
}

template<>
inline const char * name<aic_model_interfaces::msg::Observation>()
{
  return "aic_model_interfaces/msg/Observation";
}

template<>
struct has_fixed_size<aic_model_interfaces::msg::Observation>
  : std::integral_constant<bool, has_fixed_size<aic_control_interfaces::msg::ControllerState>::value && has_fixed_size<geometry_msgs::msg::WrenchStamped>::value && has_fixed_size<sensor_msgs::msg::CameraInfo>::value && has_fixed_size<sensor_msgs::msg::Image>::value && has_fixed_size<sensor_msgs::msg::JointState>::value> {};

template<>
struct has_bounded_size<aic_model_interfaces::msg::Observation>
  : std::integral_constant<bool, has_bounded_size<aic_control_interfaces::msg::ControllerState>::value && has_bounded_size<geometry_msgs::msg::WrenchStamped>::value && has_bounded_size<sensor_msgs::msg::CameraInfo>::value && has_bounded_size<sensor_msgs::msg::Image>::value && has_bounded_size<sensor_msgs::msg::JointState>::value> {};

template<>
struct is_message<aic_model_interfaces::msg::Observation>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__TRAITS_HPP_
