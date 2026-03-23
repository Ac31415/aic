// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/msg/detail/motion_update__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace msg
{

namespace builder
{

class Init_MotionUpdate_trajectory_generation_mode
{
public:
  explicit Init_MotionUpdate_trajectory_generation_mode(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  ::aic_control_interfaces::msg::MotionUpdate trajectory_generation_mode(::aic_control_interfaces::msg::MotionUpdate::_trajectory_generation_mode_type arg)
  {
    msg_.trajectory_generation_mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_wrench_feedback_gains_at_tip
{
public:
  explicit Init_MotionUpdate_wrench_feedback_gains_at_tip(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_trajectory_generation_mode wrench_feedback_gains_at_tip(::aic_control_interfaces::msg::MotionUpdate::_wrench_feedback_gains_at_tip_type arg)
  {
    msg_.wrench_feedback_gains_at_tip = std::move(arg);
    return Init_MotionUpdate_trajectory_generation_mode(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_feedforward_wrench_at_tip
{
public:
  explicit Init_MotionUpdate_feedforward_wrench_at_tip(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_wrench_feedback_gains_at_tip feedforward_wrench_at_tip(::aic_control_interfaces::msg::MotionUpdate::_feedforward_wrench_at_tip_type arg)
  {
    msg_.feedforward_wrench_at_tip = std::move(arg);
    return Init_MotionUpdate_wrench_feedback_gains_at_tip(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_target_damping
{
public:
  explicit Init_MotionUpdate_target_damping(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_feedforward_wrench_at_tip target_damping(::aic_control_interfaces::msg::MotionUpdate::_target_damping_type arg)
  {
    msg_.target_damping = std::move(arg);
    return Init_MotionUpdate_feedforward_wrench_at_tip(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_target_stiffness
{
public:
  explicit Init_MotionUpdate_target_stiffness(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_target_damping target_stiffness(::aic_control_interfaces::msg::MotionUpdate::_target_stiffness_type arg)
  {
    msg_.target_stiffness = std::move(arg);
    return Init_MotionUpdate_target_damping(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_velocity
{
public:
  explicit Init_MotionUpdate_velocity(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_target_stiffness velocity(::aic_control_interfaces::msg::MotionUpdate::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_MotionUpdate_target_stiffness(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_pose
{
public:
  explicit Init_MotionUpdate_pose(::aic_control_interfaces::msg::MotionUpdate & msg)
  : msg_(msg)
  {}
  Init_MotionUpdate_velocity pose(::aic_control_interfaces::msg::MotionUpdate::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_MotionUpdate_velocity(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

class Init_MotionUpdate_header
{
public:
  Init_MotionUpdate_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionUpdate_pose header(::aic_control_interfaces::msg::MotionUpdate::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_MotionUpdate_pose(msg_);
  }

private:
  ::aic_control_interfaces::msg::MotionUpdate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::msg::MotionUpdate>()
{
  return aic_control_interfaces::msg::builder::Init_MotionUpdate_header();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__BUILDER_HPP_
