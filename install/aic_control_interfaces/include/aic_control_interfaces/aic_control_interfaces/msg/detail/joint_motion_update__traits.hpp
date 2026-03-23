// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/joint_motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/msg/detail/joint_motion_update__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__traits.hpp"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__traits.hpp"

namespace aic_control_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const JointMotionUpdate & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_state
  {
    out << "target_state: ";
    to_flow_style_yaml(msg.target_state, out);
    out << ", ";
  }

  // member: target_stiffness
  {
    if (msg.target_stiffness.size() == 0) {
      out << "target_stiffness: []";
    } else {
      out << "target_stiffness: [";
      size_t pending_items = msg.target_stiffness.size();
      for (auto item : msg.target_stiffness) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_damping
  {
    if (msg.target_damping.size() == 0) {
      out << "target_damping: []";
    } else {
      out << "target_damping: [";
      size_t pending_items = msg.target_damping.size();
      for (auto item : msg.target_damping) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: trajectory_generation_mode
  {
    out << "trajectory_generation_mode: ";
    to_flow_style_yaml(msg.trajectory_generation_mode, out);
    out << ", ";
  }

  // member: target_feedforward_torque
  {
    if (msg.target_feedforward_torque.size() == 0) {
      out << "target_feedforward_torque: []";
    } else {
      out << "target_feedforward_torque: [";
      size_t pending_items = msg.target_feedforward_torque.size();
      for (auto item : msg.target_feedforward_torque) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const JointMotionUpdate & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_state:\n";
    to_block_style_yaml(msg.target_state, out, indentation + 2);
  }

  // member: target_stiffness
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_stiffness.size() == 0) {
      out << "target_stiffness: []\n";
    } else {
      out << "target_stiffness:\n";
      for (auto item : msg.target_stiffness) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_damping
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_damping.size() == 0) {
      out << "target_damping: []\n";
    } else {
      out << "target_damping:\n";
      for (auto item : msg.target_damping) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: trajectory_generation_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "trajectory_generation_mode:\n";
    to_block_style_yaml(msg.trajectory_generation_mode, out, indentation + 2);
  }

  // member: target_feedforward_torque
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_feedforward_torque.size() == 0) {
      out << "target_feedforward_torque: []\n";
    } else {
      out << "target_feedforward_torque:\n";
      for (auto item : msg.target_feedforward_torque) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const JointMotionUpdate & msg, bool use_flow_style = false)
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
  const aic_control_interfaces::msg::JointMotionUpdate & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::msg::JointMotionUpdate & msg)
{
  return aic_control_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::msg::JointMotionUpdate>()
{
  return "aic_control_interfaces::msg::JointMotionUpdate";
}

template<>
inline const char * name<aic_control_interfaces::msg::JointMotionUpdate>()
{
  return "aic_control_interfaces/msg/JointMotionUpdate";
}

template<>
struct has_fixed_size<aic_control_interfaces::msg::JointMotionUpdate>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aic_control_interfaces::msg::JointMotionUpdate>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<aic_control_interfaces::msg::JointMotionUpdate>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__TRAITS_HPP_
