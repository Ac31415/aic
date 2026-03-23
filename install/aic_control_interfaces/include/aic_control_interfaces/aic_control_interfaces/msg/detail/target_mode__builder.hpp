// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:msg/TargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/target_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/msg/detail/target_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace msg
{

namespace builder
{

class Init_TargetMode_mode
{
public:
  Init_TargetMode_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aic_control_interfaces::msg::TargetMode mode(::aic_control_interfaces::msg::TargetMode::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::msg::TargetMode msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::msg::TargetMode>()
{
  return aic_control_interfaces::msg::builder::Init_TargetMode_mode();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TARGET_MODE__BUILDER_HPP_
