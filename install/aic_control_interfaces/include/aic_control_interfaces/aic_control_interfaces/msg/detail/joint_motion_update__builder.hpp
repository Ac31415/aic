// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/joint_motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/msg/detail/joint_motion_update__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace msg
{

namespace builder
{

class Init_JointMotionUpdate_target_feedforward_torque
{
public:
  explicit Init_JointMotionUpdate_target_feedforward_torque(::aic_control_interfaces::msg::JointMotionUpdate & msg)
  : msg_(msg)
  {}
  ::aic_control_interfaces::msg::JointMotionUpdate target_feedforward_torque(::aic_control_interfaces::msg::JointMotionUpdate::_target_feedforward_torque_type arg)
  {
    msg_.target_feedforward_torque = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::msg::JointMotionUpdate msg_;
};

class Init_JointMotionUpdate_trajectory_generation_mode
{
public:
  explicit Init_JointMotionUpdate_trajectory_generation_mode(::aic_control_interfaces::msg::JointMotionUpdate & msg)
  : msg_(msg)
  {}
  Init_JointMotionUpdate_target_feedforward_torque trajectory_generation_mode(::aic_control_interfaces::msg::JointMotionUpdate::_trajectory_generation_mode_type arg)
  {
    msg_.trajectory_generation_mode = std::move(arg);
    return Init_JointMotionUpdate_target_feedforward_torque(msg_);
  }

private:
  ::aic_control_interfaces::msg::JointMotionUpdate msg_;
};

class Init_JointMotionUpdate_target_damping
{
public:
  explicit Init_JointMotionUpdate_target_damping(::aic_control_interfaces::msg::JointMotionUpdate & msg)
  : msg_(msg)
  {}
  Init_JointMotionUpdate_trajectory_generation_mode target_damping(::aic_control_interfaces::msg::JointMotionUpdate::_target_damping_type arg)
  {
    msg_.target_damping = std::move(arg);
    return Init_JointMotionUpdate_trajectory_generation_mode(msg_);
  }

private:
  ::aic_control_interfaces::msg::JointMotionUpdate msg_;
};

class Init_JointMotionUpdate_target_stiffness
{
public:
  explicit Init_JointMotionUpdate_target_stiffness(::aic_control_interfaces::msg::JointMotionUpdate & msg)
  : msg_(msg)
  {}
  Init_JointMotionUpdate_target_damping target_stiffness(::aic_control_interfaces::msg::JointMotionUpdate::_target_stiffness_type arg)
  {
    msg_.target_stiffness = std::move(arg);
    return Init_JointMotionUpdate_target_damping(msg_);
  }

private:
  ::aic_control_interfaces::msg::JointMotionUpdate msg_;
};

class Init_JointMotionUpdate_target_state
{
public:
  Init_JointMotionUpdate_target_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_JointMotionUpdate_target_stiffness target_state(::aic_control_interfaces::msg::JointMotionUpdate::_target_state_type arg)
  {
    msg_.target_state = std::move(arg);
    return Init_JointMotionUpdate_target_stiffness(msg_);
  }

private:
  ::aic_control_interfaces::msg::JointMotionUpdate msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::msg::JointMotionUpdate>()
{
  return aic_control_interfaces::msg::builder::Init_JointMotionUpdate_target_state();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__BUILDER_HPP_
