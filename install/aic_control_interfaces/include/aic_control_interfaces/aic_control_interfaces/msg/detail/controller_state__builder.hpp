// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/controller_state.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/msg/detail/controller_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace msg
{

namespace builder
{

class Init_ControllerState_fts_tare_offset
{
public:
  explicit Init_ControllerState_fts_tare_offset(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  ::aic_control_interfaces::msg::ControllerState fts_tare_offset(::aic_control_interfaces::msg::ControllerState::_fts_tare_offset_type arg)
  {
    msg_.fts_tare_offset = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_target_mode
{
public:
  explicit Init_ControllerState_target_mode(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_fts_tare_offset target_mode(::aic_control_interfaces::msg::ControllerState::_target_mode_type arg)
  {
    msg_.target_mode = std::move(arg);
    return Init_ControllerState_fts_tare_offset(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_reference_joint_state
{
public:
  explicit Init_ControllerState_reference_joint_state(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_target_mode reference_joint_state(::aic_control_interfaces::msg::ControllerState::_reference_joint_state_type arg)
  {
    msg_.reference_joint_state = std::move(arg);
    return Init_ControllerState_target_mode(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_tcp_error
{
public:
  explicit Init_ControllerState_tcp_error(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_reference_joint_state tcp_error(::aic_control_interfaces::msg::ControllerState::_tcp_error_type arg)
  {
    msg_.tcp_error = std::move(arg);
    return Init_ControllerState_reference_joint_state(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_reference_tcp_pose
{
public:
  explicit Init_ControllerState_reference_tcp_pose(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_tcp_error reference_tcp_pose(::aic_control_interfaces::msg::ControllerState::_reference_tcp_pose_type arg)
  {
    msg_.reference_tcp_pose = std::move(arg);
    return Init_ControllerState_tcp_error(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_tcp_velocity
{
public:
  explicit Init_ControllerState_tcp_velocity(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_reference_tcp_pose tcp_velocity(::aic_control_interfaces::msg::ControllerState::_tcp_velocity_type arg)
  {
    msg_.tcp_velocity = std::move(arg);
    return Init_ControllerState_reference_tcp_pose(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_tcp_pose
{
public:
  explicit Init_ControllerState_tcp_pose(::aic_control_interfaces::msg::ControllerState & msg)
  : msg_(msg)
  {}
  Init_ControllerState_tcp_velocity tcp_pose(::aic_control_interfaces::msg::ControllerState::_tcp_pose_type arg)
  {
    msg_.tcp_pose = std::move(arg);
    return Init_ControllerState_tcp_velocity(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

class Init_ControllerState_header
{
public:
  Init_ControllerState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ControllerState_tcp_pose header(::aic_control_interfaces::msg::ControllerState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_ControllerState_tcp_pose(msg_);
  }

private:
  ::aic_control_interfaces::msg::ControllerState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::msg::ControllerState>()
{
  return aic_control_interfaces::msg::builder::Init_ControllerState_header();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__BUILDER_HPP_
