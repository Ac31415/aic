// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "aic_model_interfaces/msg/detail/observation__rosidl_typesupport_introspection_c.h"
#include "aic_model_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "aic_model_interfaces/msg/detail/observation__functions.h"
#include "aic_model_interfaces/msg/detail/observation__struct.h"


// Include directives for member types
// Member `left_image`
// Member `center_image`
// Member `right_image`
#include "sensor_msgs/msg/image.h"
// Member `left_image`
// Member `center_image`
// Member `right_image`
#include "sensor_msgs/msg/detail/image__rosidl_typesupport_introspection_c.h"
// Member `left_camera_info`
// Member `center_camera_info`
// Member `right_camera_info`
#include "sensor_msgs/msg/camera_info.h"
// Member `left_camera_info`
// Member `center_camera_info`
// Member `right_camera_info`
#include "sensor_msgs/msg/detail/camera_info__rosidl_typesupport_introspection_c.h"
// Member `wrist_wrench`
#include "geometry_msgs/msg/wrench_stamped.h"
// Member `wrist_wrench`
#include "geometry_msgs/msg/detail/wrench_stamped__rosidl_typesupport_introspection_c.h"
// Member `joint_states`
#include "sensor_msgs/msg/joint_state.h"
// Member `joint_states`
#include "sensor_msgs/msg/detail/joint_state__rosidl_typesupport_introspection_c.h"
// Member `controller_state`
#include "aic_control_interfaces/msg/controller_state.h"
// Member `controller_state`
#include "aic_control_interfaces/msg/detail/controller_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  aic_model_interfaces__msg__Observation__init(message_memory);
}

void aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_fini_function(void * message_memory)
{
  aic_model_interfaces__msg__Observation__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[9] = {
  {
    "left_image",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, left_image),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "left_camera_info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, left_camera_info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_image",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, center_image),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "center_camera_info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, center_camera_info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_image",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, right_image),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "right_camera_info",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, right_camera_info),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "wrist_wrench",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, wrist_wrench),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_states",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, joint_states),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "controller_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(aic_model_interfaces__msg__Observation, controller_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_members = {
  "aic_model_interfaces__msg",  // message namespace
  "Observation",  // message name
  9,  // number of fields
  sizeof(aic_model_interfaces__msg__Observation),
  false,  // has_any_key_member_
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array,  // message members
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_init_function,  // function to initialize message memory (memory has to be allocated)
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_type_support_handle = {
  0,
  &aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_members,
  get_message_typesupport_handle_function,
  &aic_model_interfaces__msg__Observation__get_type_hash,
  &aic_model_interfaces__msg__Observation__get_type_description,
  &aic_model_interfaces__msg__Observation__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_aic_model_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_model_interfaces, msg, Observation)() {
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Image)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, CameraInfo)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Image)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, CameraInfo)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, Image)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, CameraInfo)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[6].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, WrenchStamped)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[7].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, JointState)();
  aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_member_array[8].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, aic_control_interfaces, msg, ControllerState)();
  if (!aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_type_support_handle.typesupport_identifier) {
    aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &aic_model_interfaces__msg__Observation__rosidl_typesupport_introspection_c__Observation_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
