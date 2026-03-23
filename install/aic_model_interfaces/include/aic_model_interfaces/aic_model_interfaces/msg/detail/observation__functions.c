// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aic_model_interfaces:msg/Observation.idl
// generated code does not contain a copyright notice
#include "aic_model_interfaces/msg/detail/observation__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `left_image`
// Member `center_image`
// Member `right_image`
#include "sensor_msgs/msg/detail/image__functions.h"
// Member `left_camera_info`
// Member `center_camera_info`
// Member `right_camera_info`
#include "sensor_msgs/msg/detail/camera_info__functions.h"
// Member `wrist_wrench`
#include "geometry_msgs/msg/detail/wrench_stamped__functions.h"
// Member `joint_states`
#include "sensor_msgs/msg/detail/joint_state__functions.h"
// Member `controller_state`
#include "aic_control_interfaces/msg/detail/controller_state__functions.h"

bool
aic_model_interfaces__msg__Observation__init(aic_model_interfaces__msg__Observation * msg)
{
  if (!msg) {
    return false;
  }
  // left_image
  if (!sensor_msgs__msg__Image__init(&msg->left_image)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // left_camera_info
  if (!sensor_msgs__msg__CameraInfo__init(&msg->left_camera_info)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // center_image
  if (!sensor_msgs__msg__Image__init(&msg->center_image)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // center_camera_info
  if (!sensor_msgs__msg__CameraInfo__init(&msg->center_camera_info)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // right_image
  if (!sensor_msgs__msg__Image__init(&msg->right_image)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // right_camera_info
  if (!sensor_msgs__msg__CameraInfo__init(&msg->right_camera_info)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // wrist_wrench
  if (!geometry_msgs__msg__WrenchStamped__init(&msg->wrist_wrench)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // joint_states
  if (!sensor_msgs__msg__JointState__init(&msg->joint_states)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  // controller_state
  if (!aic_control_interfaces__msg__ControllerState__init(&msg->controller_state)) {
    aic_model_interfaces__msg__Observation__fini(msg);
    return false;
  }
  return true;
}

void
aic_model_interfaces__msg__Observation__fini(aic_model_interfaces__msg__Observation * msg)
{
  if (!msg) {
    return;
  }
  // left_image
  sensor_msgs__msg__Image__fini(&msg->left_image);
  // left_camera_info
  sensor_msgs__msg__CameraInfo__fini(&msg->left_camera_info);
  // center_image
  sensor_msgs__msg__Image__fini(&msg->center_image);
  // center_camera_info
  sensor_msgs__msg__CameraInfo__fini(&msg->center_camera_info);
  // right_image
  sensor_msgs__msg__Image__fini(&msg->right_image);
  // right_camera_info
  sensor_msgs__msg__CameraInfo__fini(&msg->right_camera_info);
  // wrist_wrench
  geometry_msgs__msg__WrenchStamped__fini(&msg->wrist_wrench);
  // joint_states
  sensor_msgs__msg__JointState__fini(&msg->joint_states);
  // controller_state
  aic_control_interfaces__msg__ControllerState__fini(&msg->controller_state);
}

bool
aic_model_interfaces__msg__Observation__are_equal(const aic_model_interfaces__msg__Observation * lhs, const aic_model_interfaces__msg__Observation * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // left_image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->left_image), &(rhs->left_image)))
  {
    return false;
  }
  // left_camera_info
  if (!sensor_msgs__msg__CameraInfo__are_equal(
      &(lhs->left_camera_info), &(rhs->left_camera_info)))
  {
    return false;
  }
  // center_image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->center_image), &(rhs->center_image)))
  {
    return false;
  }
  // center_camera_info
  if (!sensor_msgs__msg__CameraInfo__are_equal(
      &(lhs->center_camera_info), &(rhs->center_camera_info)))
  {
    return false;
  }
  // right_image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->right_image), &(rhs->right_image)))
  {
    return false;
  }
  // right_camera_info
  if (!sensor_msgs__msg__CameraInfo__are_equal(
      &(lhs->right_camera_info), &(rhs->right_camera_info)))
  {
    return false;
  }
  // wrist_wrench
  if (!geometry_msgs__msg__WrenchStamped__are_equal(
      &(lhs->wrist_wrench), &(rhs->wrist_wrench)))
  {
    return false;
  }
  // joint_states
  if (!sensor_msgs__msg__JointState__are_equal(
      &(lhs->joint_states), &(rhs->joint_states)))
  {
    return false;
  }
  // controller_state
  if (!aic_control_interfaces__msg__ControllerState__are_equal(
      &(lhs->controller_state), &(rhs->controller_state)))
  {
    return false;
  }
  return true;
}

bool
aic_model_interfaces__msg__Observation__copy(
  const aic_model_interfaces__msg__Observation * input,
  aic_model_interfaces__msg__Observation * output)
{
  if (!input || !output) {
    return false;
  }
  // left_image
  if (!sensor_msgs__msg__Image__copy(
      &(input->left_image), &(output->left_image)))
  {
    return false;
  }
  // left_camera_info
  if (!sensor_msgs__msg__CameraInfo__copy(
      &(input->left_camera_info), &(output->left_camera_info)))
  {
    return false;
  }
  // center_image
  if (!sensor_msgs__msg__Image__copy(
      &(input->center_image), &(output->center_image)))
  {
    return false;
  }
  // center_camera_info
  if (!sensor_msgs__msg__CameraInfo__copy(
      &(input->center_camera_info), &(output->center_camera_info)))
  {
    return false;
  }
  // right_image
  if (!sensor_msgs__msg__Image__copy(
      &(input->right_image), &(output->right_image)))
  {
    return false;
  }
  // right_camera_info
  if (!sensor_msgs__msg__CameraInfo__copy(
      &(input->right_camera_info), &(output->right_camera_info)))
  {
    return false;
  }
  // wrist_wrench
  if (!geometry_msgs__msg__WrenchStamped__copy(
      &(input->wrist_wrench), &(output->wrist_wrench)))
  {
    return false;
  }
  // joint_states
  if (!sensor_msgs__msg__JointState__copy(
      &(input->joint_states), &(output->joint_states)))
  {
    return false;
  }
  // controller_state
  if (!aic_control_interfaces__msg__ControllerState__copy(
      &(input->controller_state), &(output->controller_state)))
  {
    return false;
  }
  return true;
}

aic_model_interfaces__msg__Observation *
aic_model_interfaces__msg__Observation__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_model_interfaces__msg__Observation * msg = (aic_model_interfaces__msg__Observation *)allocator.allocate(sizeof(aic_model_interfaces__msg__Observation), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aic_model_interfaces__msg__Observation));
  bool success = aic_model_interfaces__msg__Observation__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aic_model_interfaces__msg__Observation__destroy(aic_model_interfaces__msg__Observation * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aic_model_interfaces__msg__Observation__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aic_model_interfaces__msg__Observation__Sequence__init(aic_model_interfaces__msg__Observation__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_model_interfaces__msg__Observation * data = NULL;

  if (size) {
    data = (aic_model_interfaces__msg__Observation *)allocator.zero_allocate(size, sizeof(aic_model_interfaces__msg__Observation), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aic_model_interfaces__msg__Observation__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aic_model_interfaces__msg__Observation__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
aic_model_interfaces__msg__Observation__Sequence__fini(aic_model_interfaces__msg__Observation__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      aic_model_interfaces__msg__Observation__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

aic_model_interfaces__msg__Observation__Sequence *
aic_model_interfaces__msg__Observation__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_model_interfaces__msg__Observation__Sequence * array = (aic_model_interfaces__msg__Observation__Sequence *)allocator.allocate(sizeof(aic_model_interfaces__msg__Observation__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aic_model_interfaces__msg__Observation__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aic_model_interfaces__msg__Observation__Sequence__destroy(aic_model_interfaces__msg__Observation__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aic_model_interfaces__msg__Observation__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aic_model_interfaces__msg__Observation__Sequence__are_equal(const aic_model_interfaces__msg__Observation__Sequence * lhs, const aic_model_interfaces__msg__Observation__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aic_model_interfaces__msg__Observation__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aic_model_interfaces__msg__Observation__Sequence__copy(
  const aic_model_interfaces__msg__Observation__Sequence * input,
  aic_model_interfaces__msg__Observation__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aic_model_interfaces__msg__Observation);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aic_model_interfaces__msg__Observation * data =
      (aic_model_interfaces__msg__Observation *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aic_model_interfaces__msg__Observation__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aic_model_interfaces__msg__Observation__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aic_model_interfaces__msg__Observation__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
