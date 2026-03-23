// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:msg/TargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/target_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/msg/detail/target_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace aic_control_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TargetMode & msg,
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
  const TargetMode & msg,
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

inline std::string to_yaml(const TargetMode & msg, bool use_flow_style = false)
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
  const aic_control_interfaces::msg::TargetMode & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::msg::TargetMode & msg)
{
  return aic_control_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::msg::TargetMode>()
{
  return "aic_control_interfaces::msg::TargetMode";
}

template<>
inline const char * name<aic_control_interfaces::msg::TargetMode>()
{
  return "aic_control_interfaces/msg/TargetMode";
}

template<>
struct has_fixed_size<aic_control_interfaces::msg::TargetMode>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aic_control_interfaces::msg::TargetMode>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aic_control_interfaces::msg::TargetMode>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__TRAITS_HPP_
