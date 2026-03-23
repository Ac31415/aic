// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:msg/TrajectoryGenerationMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/trajectory_generation_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrajectoryGenerationMode_mode
{
public:
  Init_TrajectoryGenerationMode_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aic_control_interfaces::msg::TrajectoryGenerationMode mode(::aic_control_interfaces::msg::TrajectoryGenerationMode::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::msg::TrajectoryGenerationMode msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::msg::TrajectoryGenerationMode>()
{
  return aic_control_interfaces::msg::builder::Init_TrajectoryGenerationMode_mode();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__TRAJECTORY_GENERATION_MODE__BUILDER_HPP_
