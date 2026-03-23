// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from aic_control_interfaces:srv/ChangeTargetMode.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/srv/change_target_mode.hpp"


#ifndef AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__TRAITS_HPP_
#define AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "aic_control_interfaces/srv/detail/change_target_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_mode'
#include "aic_control_interfaces/msg/detail/target_mode__traits.hpp"

namespace aic_control_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ChangeTargetMode_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_mode
  {
    out << "target_mode: ";
    to_flow_style_yaml(msg.target_mode, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChangeTargetMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_mode:\n";
    to_block_style_yaml(msg.target_mode, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChangeTargetMode_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aic_control_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use aic_control_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aic_control_interfaces::srv::ChangeTargetMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::srv::ChangeTargetMode_Request & msg)
{
  return aic_control_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::srv::ChangeTargetMode_Request>()
{
  return "aic_control_interfaces::srv::ChangeTargetMode_Request";
}

template<>
inline const char * name<aic_control_interfaces::srv::ChangeTargetMode_Request>()
{
  return "aic_control_interfaces/srv/ChangeTargetMode_Request";
}

template<>
struct has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode_Request>
  : std::integral_constant<bool, has_fixed_size<aic_control_interfaces::msg::TargetMode>::value> {};

template<>
struct has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Request>
  : std::integral_constant<bool, has_bounded_size<aic_control_interfaces::msg::TargetMode>::value> {};

template<>
struct is_message<aic_control_interfaces::srv::ChangeTargetMode_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace aic_control_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ChangeTargetMode_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChangeTargetMode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChangeTargetMode_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aic_control_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use aic_control_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aic_control_interfaces::srv::ChangeTargetMode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::srv::ChangeTargetMode_Response & msg)
{
  return aic_control_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::srv::ChangeTargetMode_Response>()
{
  return "aic_control_interfaces::srv::ChangeTargetMode_Response";
}

template<>
inline const char * name<aic_control_interfaces::srv::ChangeTargetMode_Response>()
{
  return "aic_control_interfaces/srv/ChangeTargetMode_Response";
}

template<>
struct has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<aic_control_interfaces::srv::ChangeTargetMode_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace aic_control_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const ChangeTargetMode_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ChangeTargetMode_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ChangeTargetMode_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace aic_control_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use aic_control_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const aic_control_interfaces::srv::ChangeTargetMode_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  aic_control_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use aic_control_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const aic_control_interfaces::srv::ChangeTargetMode_Event & msg)
{
  return aic_control_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<aic_control_interfaces::srv::ChangeTargetMode_Event>()
{
  return "aic_control_interfaces::srv::ChangeTargetMode_Event";
}

template<>
inline const char * name<aic_control_interfaces::srv::ChangeTargetMode_Event>()
{
  return "aic_control_interfaces/srv/ChangeTargetMode_Event";
}

template<>
struct has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Event>
  : std::integral_constant<bool, has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Request>::value && has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<aic_control_interfaces::srv::ChangeTargetMode_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<aic_control_interfaces::srv::ChangeTargetMode>()
{
  return "aic_control_interfaces::srv::ChangeTargetMode";
}

template<>
inline const char * name<aic_control_interfaces::srv::ChangeTargetMode>()
{
  return "aic_control_interfaces/srv/ChangeTargetMode";
}

template<>
struct has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode>
  : std::integral_constant<
    bool,
    has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode_Request>::value &&
    has_fixed_size<aic_control_interfaces::srv::ChangeTargetMode_Response>::value
  >
{
};

template<>
struct has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode>
  : std::integral_constant<
    bool,
    has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Request>::value &&
    has_bounded_size<aic_control_interfaces::srv::ChangeTargetMode_Response>::value
  >
{
};

template<>
struct is_service<aic_control_interfaces::srv::ChangeTargetMode>
  : std::true_type
{
};

template<>
struct is_service_request<aic_control_interfaces::srv::ChangeTargetMode_Request>
  : std::true_type
{
};

template<>
struct is_service_response<aic_control_interfaces::srv::ChangeTargetMode_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AIC_CONTROL_INTERFACES__SRV__DETAIL__CHANGE_TARGET_MODE__TRAITS_HPP_
