// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_model_interfaces/msg/observation.hpp"


#ifndef AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__BUILDER_HPP_
#define AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_model_interfaces/msg/detail/observation__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_model_interfaces
{

namespace msg
{

namespace builder
{

class Init_Observation_controller_state
{
public:
  explicit Init_Observation_controller_state(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  ::aic_model_interfaces::msg::Observation controller_state(::aic_model_interfaces::msg::Observation::_controller_state_type arg)
  {
    msg_.controller_state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_joint_states
{
public:
  explicit Init_Observation_joint_states(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_controller_state joint_states(::aic_model_interfaces::msg::Observation::_joint_states_type arg)
  {
    msg_.joint_states = std::move(arg);
    return Init_Observation_controller_state(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_wrist_wrench
{
public:
  explicit Init_Observation_wrist_wrench(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_joint_states wrist_wrench(::aic_model_interfaces::msg::Observation::_wrist_wrench_type arg)
  {
    msg_.wrist_wrench = std::move(arg);
    return Init_Observation_joint_states(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_right_camera_info
{
public:
  explicit Init_Observation_right_camera_info(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_wrist_wrench right_camera_info(::aic_model_interfaces::msg::Observation::_right_camera_info_type arg)
  {
    msg_.right_camera_info = std::move(arg);
    return Init_Observation_wrist_wrench(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_right_image
{
public:
  explicit Init_Observation_right_image(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_right_camera_info right_image(::aic_model_interfaces::msg::Observation::_right_image_type arg)
  {
    msg_.right_image = std::move(arg);
    return Init_Observation_right_camera_info(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_center_camera_info
{
public:
  explicit Init_Observation_center_camera_info(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_right_image center_camera_info(::aic_model_interfaces::msg::Observation::_center_camera_info_type arg)
  {
    msg_.center_camera_info = std::move(arg);
    return Init_Observation_right_image(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_center_image
{
public:
  explicit Init_Observation_center_image(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_center_camera_info center_image(::aic_model_interfaces::msg::Observation::_center_image_type arg)
  {
    msg_.center_image = std::move(arg);
    return Init_Observation_center_camera_info(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_left_camera_info
{
public:
  explicit Init_Observation_left_camera_info(::aic_model_interfaces::msg::Observation & msg)
  : msg_(msg)
  {}
  Init_Observation_center_image left_camera_info(::aic_model_interfaces::msg::Observation::_left_camera_info_type arg)
  {
    msg_.left_camera_info = std::move(arg);
    return Init_Observation_center_image(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

class Init_Observation_left_image
{
public:
  Init_Observation_left_image()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Observation_left_camera_info left_image(::aic_model_interfaces::msg::Observation::_left_image_type arg)
  {
    msg_.left_image = std::move(arg);
    return Init_Observation_left_camera_info(msg_);
  }

private:
  ::aic_model_interfaces::msg::Observation msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_model_interfaces::msg::Observation>()
{
  return aic_model_interfaces::msg::builder::Init_Observation_left_image();
}

}  // namespace aic_model_interfaces

#endif  // AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__BUILDER_HPP_
