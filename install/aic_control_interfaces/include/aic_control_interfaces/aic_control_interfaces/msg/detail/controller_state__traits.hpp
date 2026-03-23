// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/controller_state.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/msg/detail/controller_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'tcp_pose'
// Member 'reference_tcp_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'tcp_velocity'
#include "geometry_msgs/msg/detail/twist__traits.hpp"
// Member 'reference_joint_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__traits.hpp"
// Member 'target_mode'
#include "aic_control_interfaces/msg/detail/target_mode__traits.hpp"
// Member 'fts_tare_offset'
#include "geometry_msgs/msg/detail/wrench_stamped__traits.hpp"

namespace aic_control_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const ControllerState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: tcp_pose
  {
    out << "tcp_pose: ";
    to_flow_style_yaml(msg.tcp_pose, out);
    out << ", ";
  }

  // member: tcp_velocity
  {
    out << "tcp_velocity: ";
    to_flow_style_yaml(msg.tcp_velocity, out);
    out << ", ";
  }

  // member: reference_tcp_pose
  {
    out << "reference_tcp_pose: ";
    to_flow_style_yaml(msg.reference_tcp_pose, out);
    out << ", ";
  }

  // member: tcp_error
  {
    if (msg.tcp_error.size() == 0) {
      out << "tcp_error: []";
    } else {
      out << "tcp_error: [";
      size_t pending_items = msg.tcp_error.size();
      for (auto item : msg.tcp_error) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: reference_joint_state
  {
    out << "reference_joint_state: ";
    to_flow_style_yaml(msg.reference_joint_state, out);
    out << ", ";
  }

  // member: target_mode
  {
    out << "target_mode: ";
    to_flow_style_yaml(msg.target_mode, out);
    out << ", ";
  }

  // member: fts_tare_offset
  {
    out << "fts_tare_offset: ";
    to_flow_style_yaml(msg.fts_tare_offset, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ControllerState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: tcp_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tcp_pose:\n";
    to_block_style_yaml(msg.tcp_pose, out, indentation + 2);
  }

  // member: tcp_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tcp_velocity:\n";
    to_block_style_yaml(msg.tcp_velocity, out, indentation + 2);
  }

  // member: reference_tcp_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reference_tcp_pose:\n";
    to_block_style_yaml(msg.reference_tcp_pose, out, indentation + 2);
  }

  // member: tcp_error
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.tcp_error.size() == 0) {
      out << "tcp_error: []\n";
    } else {
      out << "tcp_error:\n";
      for (auto item : msg.tcp_error) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: reference_joint_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reference_joint_state:\n";
    to_block_style_yaml(msg.reference_joint_state, out, indentation + 2);
  }

  // member: target_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_mode:\n";
    to_block_style_yaml(msg.target_mode, out, indentation + 2);
  }

  // member: fts_tare_offset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fts_tare_offset:\n";
    to_block_style_yaml(msg.fts_tare_offset, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ControllerState & msg, bool use_flow_style = false)
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

}  // namespace aic_control_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use aic_control_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aic_control_interfaces::msg::ControllerState & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::msg::ControllerState & msg)
{
  return aic_control_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::msg::ControllerState>()
{
  return "aic_control_interfaces::msg::ControllerState";
}

template<>
inline const char * name<aic_control_interfaces::msg::ControllerState>()
{
  return "aic_control_interfaces/msg/ControllerState";
}

template<>
struct has_fixed_size<aic_control_interfaces::msg::ControllerState>
  : std::integral_constant<bool, has_fixed_size<aic_control_interfaces::msg::TargetMode>::value && has_fixed_size<geometry_msgs::msg::Pose>::value && has_fixed_size<geometry_msgs::msg::Twist>::value && has_fixed_size<geometry_msgs::msg::WrenchStamped>::value && has_fixed_size<std_msgs::msg::Header>::value && has_fixed_size<trajectory_msgs::msg::JointTrajectoryPoint>::value> {};

template<>
struct has_bounded_size<aic_control_interfaces::msg::ControllerState>
  : std::integral_constant<bool, has_bounded_size<aic_control_interfaces::msg::TargetMode>::value && has_bounded_size<geometry_msgs::msg::Pose>::value && has_bounded_size<geometry_msgs::msg::Twist>::value && has_bounded_size<geometry_msgs::msg::WrenchStamped>::value && has_bounded_size<std_msgs::msg::Header>::value && has_bounded_size<trajectory_msgs::msg::JointTrajectoryPoint>::value> {};

template<>
struct is_message<aic_control_interfaces::msg::ControllerState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__TRAITS_HPP_
