// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:msg/TrajectoryGenerationMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/trajectory_generation_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aic_control_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrajectoryGenerationMode & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode
  {
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TrajectoryGenerationMode & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode: ";
    rosidl_generator_traits::value_to_yaml(msg.mode, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TrajectoryGenerationMode & msg, bool use_flow_style = false)
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
  const aic_control_interfaces::msg::TrajectoryGenerationMode & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::msg::TrajectoryGenerationMode & msg)
{
  return aic_control_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::msg::TrajectoryGenerationMode>()
{
  return "aic_control_interfaces::msg::TrajectoryGenerationMode";
}

template<>
inline const char * name<aic_control_interfaces::msg::TrajectoryGenerationMode>()
{
  return "aic_control_interfaces/msg/TrajectoryGenerationMode";
}

template<>
struct has_fixed_size<aic_control_interfaces::msg::TrajectoryGenerationMode>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aic_control_interfaces::msg::TrajectoryGenerationMode>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aic_control_interfaces::msg::TrajectoryGenerationMode>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__TRAITS_HPP_
