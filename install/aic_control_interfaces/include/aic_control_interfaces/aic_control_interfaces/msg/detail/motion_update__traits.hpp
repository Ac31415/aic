// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/msg/detail/motion_update__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__traits.hpp"
// Member 'feedforward_wrench_at_tip'
#include "geometry_msgs/msg/detail/wrench__traits.hpp"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__traits.hpp"

namespace aic_control_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const MotionUpdate & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: pose
  {
    out << "pose: ";
    to_flow_style_yaml(msg.pose, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    to_flow_style_yaml(msg.velocity, out);
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

  // member: feedforward_wrench_at_tip
  {
    out << "feedforward_wrench_at_tip: ";
    to_flow_style_yaml(msg.feedforward_wrench_at_tip, out);
    out << ", ";
  }

  // member: wrench_feedback_gains_at_tip
  {
    if (msg.wrench_feedback_gains_at_tip.size() == 0) {
      out << "wrench_feedback_gains_at_tip: []";
    } else {
      out << "wrench_feedback_gains_at_tip: [";
      size_t pending_items = msg.wrench_feedback_gains_at_tip.size();
      for (auto item : msg.wrench_feedback_gains_at_tip) {
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
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotionUpdate & msg,
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

  // member: pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "pose:\n";
    to_block_style_yaml(msg.pose, out, indentation + 2);
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity:\n";
    to_block_style_yaml(msg.velocity, out, indentation + 2);
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

  // member: feedforward_wrench_at_tip
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedforward_wrench_at_tip:\n";
    to_block_style_yaml(msg.feedforward_wrench_at_tip, out, indentation + 2);
  }

  // member: wrench_feedback_gains_at_tip
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.wrench_feedback_gains_at_tip.size() == 0) {
      out << "wrench_feedback_gains_at_tip: []\n";
    } else {
      out << "wrench_feedback_gains_at_tip:\n";
      for (auto item : msg.wrench_feedback_gains_at_tip) {
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotionUpdate & msg, bool use_flow_style = false)
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
  const aic_control_interfaces::msg::MotionUpdate & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::msg::MotionUpdate & msg)
{
  return aic_control_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::msg::MotionUpdate>()
{
  return "aic_control_interfaces::msg::MotionUpdate";
}

template<>
inline const char * name<aic_control_interfaces::msg::MotionUpdate>()
{
  return "aic_control_interfaces/msg/MotionUpdate";
}

template<>
struct has_fixed_size<aic_control_interfaces::msg::MotionUpdate>
  : std::integral_constant<bool, has_fixed_size<aic_control_interfaces::msg::TrajectoryGenerationMode>::value && has_fixed_size<geometry_msgs::msg::Pose>::value && has_fixed_size<geometry_msgs::msg::Twist>::value && has_fixed_size<geometry_msgs::msg::Wrench>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<aic_control_interfaces::msg::MotionUpdate>
  : std::integral_constant<bool, has_bounded_size<aic_control_interfaces::msg::TrajectoryGenerationMode>::value && has_bounded_size<geometry_msgs::msg::Pose>::value && has_bounded_size<geometry_msgs::msg::Twist>::value && has_bounded_size<geometry_msgs::msg::Wrench>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<aic_control_interfaces::msg::MotionUpdate>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__TRAITS_HPP_
