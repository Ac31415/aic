// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "aic_model_interfaces/msg/observation.hpp"


#ifndef AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_HPP_
#define AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'left_image'
// Member 'center_image'
// Member 'right_image'
#include "sensor_msgs/msg/detail/image__struct.hpp"
// Member 'left_camera_info'
// Member 'center_camera_info'
// Member 'right_camera_info'
#include "sensor_msgs/msg/detail/camera_info__struct.hpp"
// Member 'wrist_wrench'
#include "geometry_msgs/msg/detail/wrench_stamped__struct.hpp"
// Member 'joint_states'
#include "sensor_msgs/msg/detail/joint_state__struct.hpp"
// Member 'controller_state'
#include "aic_control_interfaces/msg/detail/controller_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__aic_model_interfaces__msg__Observation __attribute__((deprecated))
#else
# define DEPRECATED__aic_model_interfaces__msg__Observation __declspec(deprecated)
#endif

namespace aic_model_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Observation_
{
  using Type = Observation_<ContainerAllocator>;

  explicit Observation_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : left_image(_init),
    left_camera_info(_init),
    center_image(_init),
    center_camera_info(_init),
    right_image(_init),
    right_camera_info(_init),
    wrist_wrench(_init),
    joint_states(_init),
    controller_state(_init)
  {
    (void)_init;
  }

  explicit Observation_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : left_image(_alloc, _init),
    left_camera_info(_alloc, _init),
    center_image(_alloc, _init),
    center_camera_info(_alloc, _init),
    right_image(_alloc, _init),
    right_camera_info(_alloc, _init),
    wrist_wrench(_alloc, _init),
    joint_states(_alloc, _init),
    controller_state(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _left_image_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _left_image_type left_image;
  using _left_camera_info_type =
    sensor_msgs::msg::CameraInfo_<ContainerAllocator>;
  _left_camera_info_type left_camera_info;
  using _center_image_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _center_image_type center_image;
  using _center_camera_info_type =
    sensor_msgs::msg::CameraInfo_<ContainerAllocator>;
  _center_camera_info_type center_camera_info;
  using _right_image_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _right_image_type right_image;
  using _right_camera_info_type =
    sensor_msgs::msg::CameraInfo_<ContainerAllocator>;
  _right_camera_info_type right_camera_info;
  using _wrist_wrench_type =
    geometry_msgs::msg::WrenchStamped_<ContainerAllocator>;
  _wrist_wrench_type wrist_wrench;
  using _joint_states_type =
    sensor_msgs::msg::JointState_<ContainerAllocator>;
  _joint_states_type joint_states;
  using _controller_state_type =
    aic_control_interfaces::msg::ControllerState_<ContainerAllocator>;
  _controller_state_type controller_state;

  // setters for named parameter idiom
  Type & set__left_image(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->left_image = _arg;
    return *this;
  }
  Type & set__left_camera_info(
    const sensor_msgs::msg::CameraInfo_<ContainerAllocator> & _arg)
  {
    this->left_camera_info = _arg;
    return *this;
  }
  Type & set__center_image(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->center_image = _arg;
    return *this;
  }
  Type & set__center_camera_info(
    const sensor_msgs::msg::CameraInfo_<ContainerAllocator> & _arg)
  {
    this->center_camera_info = _arg;
    return *this;
  }
  Type & set__right_image(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->right_image = _arg;
    return *this;
  }
  Type & set__right_camera_info(
    const sensor_msgs::msg::CameraInfo_<ContainerAllocator> & _arg)
  {
    this->right_camera_info = _arg;
    return *this;
  }
  Type & set__wrist_wrench(
    const geometry_msgs::msg::WrenchStamped_<ContainerAllocator> & _arg)
  {
    this->wrist_wrench = _arg;
    return *this;
  }
  Type & set__joint_states(
    const sensor_msgs::msg::JointState_<ContainerAllocator> & _arg)
  {
    this->joint_states = _arg;
    return *this;
  }
  Type & set__controller_state(
    const aic_control_interfaces::msg::ControllerState_<ContainerAllocator> & _arg)
  {
    this->controller_state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    aic_model_interfaces::msg::Observation_<ContainerAllocator> *;
  using ConstRawPtr =
    const aic_model_interfaces::msg::Observation_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      aic_model_interfaces::msg::Observation_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      aic_model_interfaces::msg::Observation_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__aic_model_interfaces__msg__Observation
    std::shared_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__aic_model_interfaces__msg__Observation
    std::shared_ptr<aic_model_interfaces::msg::Observation_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Observation_ & other) const
  {
    if (this->left_image != other.left_image) {
      return false;
    }
    if (this->left_camera_info != other.left_camera_info) {
      return false;
    }
    if (this->center_image != other.center_image) {
      return false;
    }
    if (this->center_camera_info != other.center_camera_info) {
      return false;
    }
    if (this->right_image != other.right_image) {
      return false;
    }
    if (this->right_camera_info != other.right_camera_info) {
      return false;
    }
    if (this->wrist_wrench != other.wrist_wrench) {
      return false;
    }
    if (this->joint_states != other.joint_states) {
      return false;
    }
    if (this->controller_state != other.controller_state) {
      return false;
    }
    return true;
  }
  bool operator!=(const Observation_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Observation_

// alias to use template instance with default allocator
using Observation =
  aic_model_interfaces::msg::Observation_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace aic_model_interfaces

#endif  // AIC_MODEL_INTERFACES__MSG__DETAIL__OBSERVATION__STRUCT_HPP_
