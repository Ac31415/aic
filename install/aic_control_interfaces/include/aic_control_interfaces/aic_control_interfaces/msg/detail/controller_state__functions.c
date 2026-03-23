// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aic_control_interfaces:msg/ControllerState.idl
// generated code does not contain a copyright notice
#include "aic_control_interfaces/msg/detail/controller_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `tcp_pose`
// Member `reference_tcp_pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `tcp_velocity`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `reference_joint_state`
#include "trajectory_msgs/msg/detail/joint_trajectory_point__functions.h"
// Member `target_mode`
#include "aic_control_interfaces/msg/detail/target_mode__functions.h"
// Member `fts_tare_offset`
#include "geometry_msgs/msg/detail/wrench_stamped__functions.h"

bool
aic_control_interfaces__msg__ControllerState__init(aic_control_interfaces__msg__ControllerState * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // tcp_pose
  if (!geometry_msgs__msg__Pose__init(&msg->tcp_pose)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // tcp_velocity
  if (!geometry_msgs__msg__Twist__init(&msg->tcp_velocity)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // reference_tcp_pose
  if (!geometry_msgs__msg__Pose__init(&msg->reference_tcp_pose)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // tcp_error
  // reference_joint_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__init(&msg->reference_joint_state)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // target_mode
  if (!aic_control_interfaces__msg__TargetMode__init(&msg->target_mode)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  // fts_tare_offset
  if (!geometry_msgs__msg__WrenchStamped__init(&msg->fts_tare_offset)) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
    return false;
  }
  return true;
}

void
aic_control_interfaces__msg__ControllerState__fini(aic_control_interfaces__msg__ControllerState * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // tcp_pose
  geometry_msgs__msg__Pose__fini(&msg->tcp_pose);
  // tcp_velocity
  geometry_msgs__msg__Twist__fini(&msg->tcp_velocity);
  // reference_tcp_pose
  geometry_msgs__msg__Pose__fini(&msg->reference_tcp_pose);
  // tcp_error
  // reference_joint_state
  trajectory_msgs__msg__JointTrajectoryPoint__fini(&msg->reference_joint_state);
  // target_mode
  aic_control_interfaces__msg__TargetMode__fini(&msg->target_mode);
  // fts_tare_offset
  geometry_msgs__msg__WrenchStamped__fini(&msg->fts_tare_offset);
}

bool
aic_control_interfaces__msg__ControllerState__are_equal(const aic_control_interfaces__msg__ControllerState * lhs, const aic_control_interfaces__msg__ControllerState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // tcp_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->tcp_pose), &(rhs->tcp_pose)))
  {
    return false;
  }
  // tcp_velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->tcp_velocity), &(rhs->tcp_velocity)))
  {
    return false;
  }
  // reference_tcp_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->reference_tcp_pose), &(rhs->reference_tcp_pose)))
  {
    return false;
  }
  // tcp_error
  for (size_t i = 0; i < 6; ++i) {
    if (lhs->tcp_error[i] != rhs->tcp_error[i]) {
      return false;
    }
  }
  // reference_joint_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__are_equal(
      &(lhs->reference_joint_state), &(rhs->reference_joint_state)))
  {
    return false;
  }
  // target_mode
  if (!aic_control_interfaces__msg__TargetMode__are_equal(
      &(lhs->target_mode), &(rhs->target_mode)))
  {
    return false;
  }
  // fts_tare_offset
  if (!geometry_msgs__msg__WrenchStamped__are_equal(
      &(lhs->fts_tare_offset), &(rhs->fts_tare_offset)))
  {
    return false;
  }
  return true;
}

bool
aic_control_interfaces__msg__ControllerState__copy(
  const aic_control_interfaces__msg__ControllerState * input,
  aic_control_interfaces__msg__ControllerState * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // tcp_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->tcp_pose), &(output->tcp_pose)))
  {
    return false;
  }
  // tcp_velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->tcp_velocity), &(output->tcp_velocity)))
  {
    return false;
  }
  // reference_tcp_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->reference_tcp_pose), &(output->reference_tcp_pose)))
  {
    return false;
  }
  // tcp_error
  for (size_t i = 0; i < 6; ++i) {
    output->tcp_error[i] = input->tcp_error[i];
  }
  // reference_joint_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__copy(
      &(input->reference_joint_state), &(output->reference_joint_state)))
  {
    return false;
  }
  // target_mode
  if (!aic_control_interfaces__msg__TargetMode__copy(
      &(input->target_mode), &(output->target_mode)))
  {
    return false;
  }
  // fts_tare_offset
  if (!geometry_msgs__msg__WrenchStamped__copy(
      &(input->fts_tare_offset), &(output->fts_tare_offset)))
  {
    return false;
  }
  return true;
}

aic_control_interfaces__msg__ControllerState *
aic_control_interfaces__msg__ControllerState__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__ControllerState * msg = (aic_control_interfaces__msg__ControllerState *)allocator.allocate(sizeof(aic_control_interfaces__msg__ControllerState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aic_control_interfaces__msg__ControllerState));
  bool success = aic_control_interfaces__msg__ControllerState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aic_control_interfaces__msg__ControllerState__destroy(aic_control_interfaces__msg__ControllerState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aic_control_interfaces__msg__ControllerState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aic_control_interfaces__msg__ControllerState__Sequence__init(aic_control_interfaces__msg__ControllerState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__ControllerState * data = NULL;

  if (size) {
    data = (aic_control_interfaces__msg__ControllerState *)allocator.zero_allocate(size, sizeof(aic_control_interfaces__msg__ControllerState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aic_control_interfaces__msg__ControllerState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aic_control_interfaces__msg__ControllerState__fini(&data[i - 1]);
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
aic_control_interfaces__msg__ControllerState__Sequence__fini(aic_control_interfaces__msg__ControllerState__Sequence * array)
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
      aic_control_interfaces__msg__ControllerState__fini(&array->data[i]);
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

aic_control_interfaces__msg__ControllerState__Sequence *
aic_control_interfaces__msg__ControllerState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__ControllerState__Sequence * array = (aic_control_interfaces__msg__ControllerState__Sequence *)allocator.allocate(sizeof(aic_control_interfaces__msg__ControllerState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aic_control_interfaces__msg__ControllerState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aic_control_interfaces__msg__ControllerState__Sequence__destroy(aic_control_interfaces__msg__ControllerState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aic_control_interfaces__msg__ControllerState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aic_control_interfaces__msg__ControllerState__Sequence__are_equal(const aic_control_interfaces__msg__ControllerState__Sequence * lhs, const aic_control_interfaces__msg__ControllerState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aic_control_interfaces__msg__ControllerState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aic_control_interfaces__msg__ControllerState__Sequence__copy(
  const aic_control_interfaces__msg__ControllerState__Sequence * input,
  aic_control_interfaces__msg__ControllerState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aic_control_interfaces__msg__ControllerState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aic_control_interfaces__msg__ControllerState * data =
      (aic_control_interfaces__msg__ControllerState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aic_control_interfaces__msg__ControllerState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aic_control_interfaces__msg__ControllerState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aic_control_interfaces__msg__ControllerState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
