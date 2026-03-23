// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/controller_state.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'tcp_pose'
// Member 'reference_tcp_pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'tcp_velocity'
#include "geometry_msgs/msg/detail/twist__struct.hpp"
// Member 'reference_joint_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__struct.hpp"
// Member 'target_mode'
#include "aic_control_interfaces/msg/detail/target_mode__struct.hpp"
// Member 'fts_tare_offset'
#include "geometry_msgs/msg/detail/wrench_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aic_control_interfaces__msg__ControllerState __attribute__((deprecated))
#else
# define DEPRECATED__aic_control_interfaces__msg__ControllerState __declspec(deprecated)
#endif

namespace aic_control_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ControllerState_
{
  using Type = ControllerState_<ContainerAllocator>;

  explicit ControllerState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    tcp_pose(_init),
    tcp_velocity(_init),
    reference_tcp_pose(_init),
    reference_joint_state(_init),
    target_mode(_init),
    fts_tare_offset(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->tcp_error.begin(), this->tcp_error.end(), 0.0);
    }
  }

  explicit ControllerState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    tcp_pose(_alloc, _init),
    tcp_velocity(_alloc, _init),
    reference_tcp_pose(_alloc, _init),
    tcp_error(_alloc),
    reference_joint_state(_alloc, _init),
    target_mode(_alloc, _init),
    fts_tare_offset(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->tcp_error.begin(), this->tcp_error.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _tcp_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _tcp_pose_type tcp_pose;
  using _tcp_velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _tcp_velocity_type tcp_velocity;
  using _reference_tcp_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _reference_tcp_pose_type reference_tcp_pose;
  using _tcp_error_type =
    std::array<double, 6>;
  _tcp_error_type tcp_error;
  using _reference_joint_state_type =
    trajectory_msgs::msg::JointTrajectoryPoint_<ContainerAllocator>;
  _reference_joint_state_type reference_joint_state;
  using _target_mode_type =
    aic_control_interfaces::msg::TargetMode_<ContainerAllocator>;
  _target_mode_type target_mode;
  using _fts_tare_offset_type =
    geometry_msgs::msg::WrenchStamped_<ContainerAllocator>;
  _fts_tare_offset_type fts_tare_offset;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__tcp_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->tcp_pose = _arg;
    return *this;
  }
  Type & set__tcp_velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->tcp_velocity = _arg;
    return *this;
  }
  Type & set__reference_tcp_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->reference_tcp_pose = _arg;
    return *this;
  }
  Type & set__tcp_error(
    const std::array<double, 6> & _arg)
  {
    this->tcp_error = _arg;
    return *this;
  }
  Type & set__reference_joint_state(
    const trajectory_msgs::msg::JointTrajectoryPoint_<ContainerAllocator> & _arg)
  {
    this->reference_joint_state = _arg;
    return *this;
  }
  Type & set__target_mode(
    const aic_control_interfaces::msg::TargetMode_<ContainerAllocator> & _arg)
  {
    this->target_mode = _arg;
    return *this;
  }
  Type & set__fts_tare_offset(
    const geometry_msgs::msg::WrenchStamped_<ContainerAllocator> & _arg)
  {
    this->fts_tare_offset = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aic_control_interfaces::msg::ControllerState_<ContainerAllocator> *;
  using ConstRawPtr =
    const aic_control_interfaces::msg::ControllerState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::ControllerState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::ControllerState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aic_control_interfaces__msg__ControllerState
    std::shared_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aic_control_interfaces__msg__ControllerState
    std::shared_ptr<aic_control_interfaces::msg::ControllerState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ControllerState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->tcp_pose != other.tcp_pose) {
      return false;
    }
    if (this->tcp_velocity != other.tcp_velocity) {
      return false;
    }
    if (this->reference_tcp_pose != other.reference_tcp_pose) {
      return false;
    }
    if (this->tcp_error != other.tcp_error) {
      return false;
    }
    if (this->reference_joint_state != other.reference_joint_state) {
      return false;
    }
    if (this->target_mode != other.target_mode) {
      return false;
    }
    if (this->fts_tare_offset != other.fts_tare_offset) {
      return false;
    }
    return true;
  }
  bool operator!=(const ControllerState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ControllerState_

// alias to use template instance with default allocator
using ControllerState =
  aic_control_interfaces::msg::ControllerState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__CONTROLLER_STATE__STRUCT_HPP_
