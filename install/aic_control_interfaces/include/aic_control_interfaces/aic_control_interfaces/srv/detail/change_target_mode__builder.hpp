// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from aic_control_interfaces:srv/ChangeTargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/srv/change_target_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__BUILDER_HPP_
#define AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "aic_control_interfaces/srv/detail/change_target_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace aic_control_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeTargetMode_Request_target_mode
{
public:
  Init_ChangeTargetMode_Request_target_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aic_control_interfaces::srv::ChangeTargetMode_Request target_mode(::aic_control_interfaces::srv::ChangeTargetMode_Request::_target_mode_type arg)
  {
    msg_.target_mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::srv::ChangeTargetMode_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::srv::ChangeTargetMode_Request>()
{
  return aic_control_interfaces::srv::builder::Init_ChangeTargetMode_Request_target_mode();
}

}  // namespace aic_control_interfaces


namespace aic_control_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeTargetMode_Response_success
{
public:
  Init_ChangeTargetMode_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::aic_control_interfaces::srv::ChangeTargetMode_Response success(::aic_control_interfaces::srv::ChangeTargetMode_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::srv::ChangeTargetMode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::srv::ChangeTargetMode_Response>()
{
  return aic_control_interfaces::srv::builder::Init_ChangeTargetMode_Response_success();
}

}  // namespace aic_control_interfaces


namespace aic_control_interfaces
{

namespace srv
{

namespace builder
{

class Init_ChangeTargetMode_Event_response
{
public:
  explicit Init_ChangeTargetMode_Event_response(::aic_control_interfaces::srv::ChangeTargetMode_Event & msg)
  : msg_(msg)
  {}
  ::aic_control_interfaces::srv::ChangeTargetMode_Event response(::aic_control_interfaces::srv::ChangeTargetMode_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::aic_control_interfaces::srv::ChangeTargetMode_Event msg_;
};

class Init_ChangeTargetMode_Event_request
{
public:
  explicit Init_ChangeTargetMode_Event_request(::aic_control_interfaces::srv::ChangeTargetMode_Event & msg)
  : msg_(msg)
  {}
  Init_ChangeTargetMode_Event_response request(::aic_control_interfaces::srv::ChangeTargetMode_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_ChangeTargetMode_Event_response(msg_);
  }

private:
  ::aic_control_interfaces::srv::ChangeTargetMode_Event msg_;
};

class Init_ChangeTargetMode_Event_info
{
public:
  Init_ChangeTargetMode_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ChangeTargetMode_Event_request info(::aic_control_interfaces::srv::ChangeTargetMode_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_ChangeTargetMode_Event_request(msg_);
  }

private:
  ::aic_control_interfaces::srv::ChangeTargetMode_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::aic_control_interfaces::srv::ChangeTargetMode_Event>()
{
  return aic_control_interfaces::srv::builder::Init_ChangeTargetMode_Event_info();
}

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__BUILDER_HPP_
