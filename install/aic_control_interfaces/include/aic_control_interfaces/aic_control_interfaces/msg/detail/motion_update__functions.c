// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aic_control_interfaces:msg/MotionUpdate.idl
// generated code does not contain a copyright notice
#include "aic_control_interfaces/msg/detail/motion_update__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/twist__functions.h"
// Member `feedforward_wrench_at_tip`
#include "geometry_msgs/msg/detail/wrench__functions.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__functions.h"

bool
aic_control_interfaces__msg__MotionUpdate__init(aic_control_interfaces__msg__MotionUpdate * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
    return false;
  }
  // pose
  if (!geometry_msgs__msg__Pose__init(&msg->pose)) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__init(&msg->velocity)) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
    return false;
  }
  // target_stiffness
  // target_damping
  // feedforward_wrench_at_tip
  if (!geometry_msgs__msg__Wrench__init(&msg->feedforward_wrench_at_tip)) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
    return false;
  }
  // wrench_feedback_gains_at_tip
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__init(&msg->trajectory_generation_mode)) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
    return false;
  }
  return true;
}

void
aic_control_interfaces__msg__MotionUpdate__fini(aic_control_interfaces__msg__MotionUpdate * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // pose
  geometry_msgs__msg__Pose__fini(&msg->pose);
  // velocity
  geometry_msgs__msg__Twist__fini(&msg->velocity);
  // target_stiffness
  // target_damping
  // feedforward_wrench_at_tip
  geometry_msgs__msg__Wrench__fini(&msg->feedforward_wrench_at_tip);
  // wrench_feedback_gains_at_tip
  // trajectory_generation_mode
  aic_control_interfaces__msg__TrajectoryGenerationMode__fini(&msg->trajectory_generation_mode);
}

bool
aic_control_interfaces__msg__MotionUpdate__are_equal(const aic_control_interfaces__msg__MotionUpdate * lhs, const aic_control_interfaces__msg__MotionUpdate * rhs)
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
  // pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->pose), &(rhs->pose)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  // target_stiffness
  for (size_t i = 0; i < 36; ++i) {
    if (lhs->target_stiffness[i] != rhs->target_stiffness[i]) {
      return false;
    }
  }
  // target_damping
  for (size_t i = 0; i < 36; ++i) {
    if (lhs->target_damping[i] != rhs->target_damping[i]) {
      return false;
    }
  }
  // feedforward_wrench_at_tip
  if (!geometry_msgs__msg__Wrench__are_equal(
      &(lhs->feedforward_wrench_at_tip), &(rhs->feedforward_wrench_at_tip)))
  {
    return false;
  }
  // wrench_feedback_gains_at_tip
  for (size_t i = 0; i < 6; ++i) {
    if (lhs->wrench_feedback_gains_at_tip[i] != rhs->wrench_feedback_gains_at_tip[i]) {
      return false;
    }
  }
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__are_equal(
      &(lhs->trajectory_generation_mode), &(rhs->trajectory_generation_mode)))
  {
    return false;
  }
  return true;
}

bool
aic_control_interfaces__msg__MotionUpdate__copy(
  const aic_control_interfaces__msg__MotionUpdate * input,
  aic_control_interfaces__msg__MotionUpdate * output)
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
  // pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->pose), &(output->pose)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  // target_stiffness
  for (size_t i = 0; i < 36; ++i) {
    output->target_stiffness[i] = input->target_stiffness[i];
  }
  // target_damping
  for (size_t i = 0; i < 36; ++i) {
    output->target_damping[i] = input->target_damping[i];
  }
  // feedforward_wrench_at_tip
  if (!geometry_msgs__msg__Wrench__copy(
      &(input->feedforward_wrench_at_tip), &(output->feedforward_wrench_at_tip)))
  {
    return false;
  }
  // wrench_feedback_gains_at_tip
  for (size_t i = 0; i < 6; ++i) {
    output->wrench_feedback_gains_at_tip[i] = input->wrench_feedback_gains_at_tip[i];
  }
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__copy(
      &(input->trajectory_generation_mode), &(output->trajectory_generation_mode)))
  {
    return false;
  }
  return true;
}

aic_control_interfaces__msg__MotionUpdate *
aic_control_interfaces__msg__MotionUpdate__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__MotionUpdate * msg = (aic_control_interfaces__msg__MotionUpdate *)allocator.allocate(sizeof(aic_control_interfaces__msg__MotionUpdate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aic_control_interfaces__msg__MotionUpdate));
  bool success = aic_control_interfaces__msg__MotionUpdate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aic_control_interfaces__msg__MotionUpdate__destroy(aic_control_interfaces__msg__MotionUpdate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aic_control_interfaces__msg__MotionUpdate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aic_control_interfaces__msg__MotionUpdate__Sequence__init(aic_control_interfaces__msg__MotionUpdate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__MotionUpdate * data = NULL;

  if (size) {
    data = (aic_control_interfaces__msg__MotionUpdate *)allocator.zero_allocate(size, sizeof(aic_control_interfaces__msg__MotionUpdate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aic_control_interfaces__msg__MotionUpdate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aic_control_interfaces__msg__MotionUpdate__fini(&data[i - 1]);
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
aic_control_interfaces__msg__MotionUpdate__Sequence__fini(aic_control_interfaces__msg__MotionUpdate__Sequence * array)
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
      aic_control_interfaces__msg__MotionUpdate__fini(&array->data[i]);
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

aic_control_interfaces__msg__MotionUpdate__Sequence *
aic_control_interfaces__msg__MotionUpdate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__MotionUpdate__Sequence * array = (aic_control_interfaces__msg__MotionUpdate__Sequence *)allocator.allocate(sizeof(aic_control_interfaces__msg__MotionUpdate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aic_control_interfaces__msg__MotionUpdate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aic_control_interfaces__msg__MotionUpdate__Sequence__destroy(aic_control_interfaces__msg__MotionUpdate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aic_control_interfaces__msg__MotionUpdate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aic_control_interfaces__msg__MotionUpdate__Sequence__are_equal(const aic_control_interfaces__msg__MotionUpdate__Sequence * lhs, const aic_control_interfaces__msg__MotionUpdate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aic_control_interfaces__msg__MotionUpdate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aic_control_interfaces__msg__MotionUpdate__Sequence__copy(
  const aic_control_interfaces__msg__MotionUpdate__Sequence * input,
  aic_control_interfaces__msg__MotionUpdate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aic_control_interfaces__msg__MotionUpdate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aic_control_interfaces__msg__MotionUpdate * data =
      (aic_control_interfaces__msg__MotionUpdate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aic_control_interfaces__msg__MotionUpdate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aic_control_interfaces__msg__MotionUpdate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aic_control_interfaces__msg__MotionUpdate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
