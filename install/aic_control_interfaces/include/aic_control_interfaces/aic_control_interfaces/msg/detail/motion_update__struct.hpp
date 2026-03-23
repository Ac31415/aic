// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_HPP_

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
// Member 'pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"
// Member 'velocity'
#include "geometry_msgs/msg/detail/twist__struct.hpp"
// Member 'feedforward_wrench_at_tip'
#include "geometry_msgs/msg/detail/wrench__struct.hpp"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aic_control_interfaces__msg__MotionUpdate __attribute__((deprecated))
#else
# define DEPRECATED__aic_control_interfaces__msg__MotionUpdate __declspec(deprecated)
#endif

namespace aic_control_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotionUpdate_
{
  using Type = MotionUpdate_<ContainerAllocator>;

  explicit MotionUpdate_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    pose(_init),
    velocity(_init),
    feedforward_wrench_at_tip(_init),
    trajectory_generation_mode(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 36>::iterator, double>(this->target_stiffness.begin(), this->target_stiffness.end(), 0.0);
      std::fill<typename std::array<double, 36>::iterator, double>(this->target_damping.begin(), this->target_damping.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->wrench_feedback_gains_at_tip.begin(), this->wrench_feedback_gains_at_tip.end(), 0.0);
    }
  }

  explicit MotionUpdate_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    pose(_alloc, _init),
    velocity(_alloc, _init),
    target_stiffness(_alloc),
    target_damping(_alloc),
    feedforward_wrench_at_tip(_alloc, _init),
    wrench_feedback_gains_at_tip(_alloc),
    trajectory_generation_mode(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 36>::iterator, double>(this->target_stiffness.begin(), this->target_stiffness.end(), 0.0);
      std::fill<typename std::array<double, 36>::iterator, double>(this->target_damping.begin(), this->target_damping.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->wrench_feedback_gains_at_tip.begin(), this->wrench_feedback_gains_at_tip.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _pose_type pose;
  using _velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _velocity_type velocity;
  using _target_stiffness_type =
    std::array<double, 36>;
  _target_stiffness_type target_stiffness;
  using _target_damping_type =
    std::array<double, 36>;
  _target_damping_type target_damping;
  using _feedforward_wrench_at_tip_type =
    geometry_msgs::msg::Wrench_<ContainerAllocator>;
  _feedforward_wrench_at_tip_type feedforward_wrench_at_tip;
  using _wrench_feedback_gains_at_tip_type =
    std::array<double, 6>;
  _wrench_feedback_gains_at_tip_type wrench_feedback_gains_at_tip;
  using _trajectory_generation_mode_type =
    aic_control_interfaces::msg::TrajectoryGenerationMode_<ContainerAllocator>;
  _trajectory_generation_mode_type trajectory_generation_mode;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->pose = _arg;
    return *this;
  }
  Type & set__velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__target_stiffness(
    const std::array<double, 36> & _arg)
  {
    this->target_stiffness = _arg;
    return *this;
  }
  Type & set__target_damping(
    const std::array<double, 36> & _arg)
  {
    this->target_damping = _arg;
    return *this;
  }
  Type & set__feedforward_wrench_at_tip(
    const geometry_msgs::msg::Wrench_<ContainerAllocator> & _arg)
  {
    this->feedforward_wrench_at_tip = _arg;
    return *this;
  }
  Type & set__wrench_feedback_gains_at_tip(
    const std::array<double, 6> & _arg)
  {
    this->wrench_feedback_gains_at_tip = _arg;
    return *this;
  }
  Type & set__trajectory_generation_mode(
    const aic_control_interfaces::msg::TrajectoryGenerationMode_<ContainerAllocator> & _arg)
  {
    this->trajectory_generation_mode = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> *;
  using ConstRawPtr =
    const aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aic_control_interfaces__msg__MotionUpdate
    std::shared_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aic_control_interfaces__msg__MotionUpdate
    std::shared_ptr<aic_control_interfaces::msg::MotionUpdate_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotionUpdate_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->pose != other.pose) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->target_stiffness != other.target_stiffness) {
      return false;
    }
    if (this->target_damping != other.target_damping) {
      return false;
    }
    if (this->feedforward_wrench_at_tip != other.feedforward_wrench_at_tip) {
      return false;
    }
    if (this->wrench_feedback_gains_at_tip != other.wrench_feedback_gains_at_tip) {
      return false;
    }
    if (this->trajectory_generation_mode != other.trajectory_generation_mode) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotionUpdate_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotionUpdate_

// alias to use template instance with default allocator
using MotionUpdate =
  aic_control_interfaces::msg::MotionUpdate_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__MOTION_UPDATE__STRUCT_HPP_
