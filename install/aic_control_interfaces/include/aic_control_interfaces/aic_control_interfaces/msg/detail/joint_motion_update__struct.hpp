// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_control_interfaces/msg/joint_motion_update.hpp"


#ifndef AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_HPP_
#define AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'target_state'
#include "trajectory_msgs/msg/detail/joint_trajectory_point__struct.hpp"
// Member 'trajectory_generation_mode'
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aic_control_interfaces__msg__JointMotionUpdate __attribute__((deprecated))
#else
# define DEPRECATED__aic_control_interfaces__msg__JointMotionUpdate __declspec(deprecated)
#endif

namespace aic_control_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct JointMotionUpdate_
{
  using Type = JointMotionUpdate_<ContainerAllocator>;

  explicit JointMotionUpdate_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_state(_init),
    trajectory_generation_mode(_init)
  {
    (void)_init;
  }

  explicit JointMotionUpdate_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_state(_alloc, _init),
    trajectory_generation_mode(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _target_state_type =
    trajectory_msgs::msg::JointTrajectoryPoint_<ContainerAllocator>;
  _target_state_type target_state;
  using _target_stiffness_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _target_stiffness_type target_stiffness;
  using _target_damping_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _target_damping_type target_damping;
  using _trajectory_generation_mode_type =
    aic_control_interfaces::msg::TrajectoryGenerationMode_<ContainerAllocator>;
  _trajectory_generation_mode_type trajectory_generation_mode;
  using _target_feedforward_torque_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _target_feedforward_torque_type target_feedforward_torque;

  // setters for named parameter idiom
  Type & set__target_state(
    const trajectory_msgs::msg::JointTrajectoryPoint_<ContainerAllocator> & _arg)
  {
    this->target_state = _arg;
    return *this;
  }
  Type & set__target_stiffness(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->target_stiffness = _arg;
    return *this;
  }
  Type & set__target_damping(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->target_damping = _arg;
    return *this;
  }
  Type & set__trajectory_generation_mode(
    const aic_control_interfaces::msg::TrajectoryGenerationMode_<ContainerAllocator> & _arg)
  {
    this->trajectory_generation_mode = _arg;
    return *this;
  }
  Type & set__target_feedforward_torque(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->target_feedforward_torque = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> *;
  using ConstRawPtr =
    const aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aic_control_interfaces__msg__JointMotionUpdate
    std::shared_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aic_control_interfaces__msg__JointMotionUpdate
    std::shared_ptr<aic_control_interfaces::msg::JointMotionUpdate_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const JointMotionUpdate_ & other) const
  {
    if (this->target_state != other.target_state) {
      return false;
    }
    if (this->target_stiffness != other.target_stiffness) {
      return false;
    }
    if (this->target_damping != other.target_damping) {
      return false;
    }
    if (this->trajectory_generation_mode != other.trajectory_generation_mode) {
      return false;
    }
    if (this->target_feedforward_torque != other.target_feedforward_torque) {
      return false;
    }
    return true;
  }
  bool operator!=(const JointMotionUpdate_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct JointMotionUpdate_

// alias to use template instance with default allocator
using JointMotionUpdate =
  aic_control_interfaces::msg::JointMotionUpdate_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aic_control_interfaces

#endif  // AIC_CONTROL_INTERFACES__MSG__DETAIL__JOINT_MOTION_UPDATE__STRUCT_HPP_
