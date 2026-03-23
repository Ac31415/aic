// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice
#include "aic_control_interfaces/msg/detail/joint_motion_update__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `target_state`
#include "trajectory_msgs/msg/detail/joint_trajectory_point__functions.h"
// Member `target_stiffness`
// Member `target_damping`
// Member `target_feedforward_torque`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `trajectory_generation_mode`
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__functions.h"

bool
aic_control_interfaces__msg__JointMotionUpdate__init(aic_control_interfaces__msg__JointMotionUpdate * msg)
{
  if (!msg) {
    return false;
  }
  // target_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__init(&msg->target_state)) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
    return false;
  }
  // target_stiffness
  if (!rosidl_runtime_c__double__Sequence__init(&msg->target_stiffness, 0)) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
    return false;
  }
  // target_damping
  if (!rosidl_runtime_c__double__Sequence__init(&msg->target_damping, 0)) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
    return false;
  }
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__init(&msg->trajectory_generation_mode)) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
    return false;
  }
  // target_feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__init(&msg->target_feedforward_torque, 0)) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
    return false;
  }
  return true;
}

void
aic_control_interfaces__msg__JointMotionUpdate__fini(aic_control_interfaces__msg__JointMotionUpdate * msg)
{
  if (!msg) {
    return;
  }
  // target_state
  trajectory_msgs__msg__JointTrajectoryPoint__fini(&msg->target_state);
  // target_stiffness
  rosidl_runtime_c__double__Sequence__fini(&msg->target_stiffness);
  // target_damping
  rosidl_runtime_c__double__Sequence__fini(&msg->target_damping);
  // trajectory_generation_mode
  aic_control_interfaces__msg__TrajectoryGenerationMode__fini(&msg->trajectory_generation_mode);
  // target_feedforward_torque
  rosidl_runtime_c__double__Sequence__fini(&msg->target_feedforward_torque);
}

bool
aic_control_interfaces__msg__JointMotionUpdate__are_equal(const aic_control_interfaces__msg__JointMotionUpdate * lhs, const aic_control_interfaces__msg__JointMotionUpdate * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // target_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__are_equal(
      &(lhs->target_state), &(rhs->target_state)))
  {
    return false;
  }
  // target_stiffness
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->target_stiffness), &(rhs->target_stiffness)))
  {
    return false;
  }
  // target_damping
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->target_damping), &(rhs->target_damping)))
  {
    return false;
  }
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__are_equal(
      &(lhs->trajectory_generation_mode), &(rhs->trajectory_generation_mode)))
  {
    return false;
  }
  // target_feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->target_feedforward_torque), &(rhs->target_feedforward_torque)))
  {
    return false;
  }
  return true;
}

bool
aic_control_interfaces__msg__JointMotionUpdate__copy(
  const aic_control_interfaces__msg__JointMotionUpdate * input,
  aic_control_interfaces__msg__JointMotionUpdate * output)
{
  if (!input || !output) {
    return false;
  }
  // target_state
  if (!trajectory_msgs__msg__JointTrajectoryPoint__copy(
      &(input->target_state), &(output->target_state)))
  {
    return false;
  }
  // target_stiffness
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->target_stiffness), &(output->target_stiffness)))
  {
    return false;
  }
  // target_damping
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->target_damping), &(output->target_damping)))
  {
    return false;
  }
  // trajectory_generation_mode
  if (!aic_control_interfaces__msg__TrajectoryGenerationMode__copy(
      &(input->trajectory_generation_mode), &(output->trajectory_generation_mode)))
  {
    return false;
  }
  // target_feedforward_torque
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->target_feedforward_torque), &(output->target_feedforward_torque)))
  {
    return false;
  }
  return true;
}

aic_control_interfaces__msg__JointMotionUpdate *
aic_control_interfaces__msg__JointMotionUpdate__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__JointMotionUpdate * msg = (aic_control_interfaces__msg__JointMotionUpdate *)allocator.allocate(sizeof(aic_control_interfaces__msg__JointMotionUpdate), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aic_control_interfaces__msg__JointMotionUpdate));
  bool success = aic_control_interfaces__msg__JointMotionUpdate__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aic_control_interfaces__msg__JointMotionUpdate__destroy(aic_control_interfaces__msg__JointMotionUpdate * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aic_control_interfaces__msg__JointMotionUpdate__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aic_control_interfaces__msg__JointMotionUpdate__Sequence__init(aic_control_interfaces__msg__JointMotionUpdate__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__JointMotionUpdate * data = NULL;

  if (size) {
    data = (aic_control_interfaces__msg__JointMotionUpdate *)allocator.zero_allocate(size, sizeof(aic_control_interfaces__msg__JointMotionUpdate), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aic_control_interfaces__msg__JointMotionUpdate__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aic_control_interfaces__msg__JointMotionUpdate__fini(&data[i - 1]);
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
aic_control_interfaces__msg__JointMotionUpdate__Sequence__fini(aic_control_interfaces__msg__JointMotionUpdate__Sequence * array)
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
      aic_control_interfaces__msg__JointMotionUpdate__fini(&array->data[i]);
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

aic_control_interfaces__msg__JointMotionUpdate__Sequence *
aic_control_interfaces__msg__JointMotionUpdate__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__JointMotionUpdate__Sequence * array = (aic_control_interfaces__msg__JointMotionUpdate__Sequence *)allocator.allocate(sizeof(aic_control_interfaces__msg__JointMotionUpdate__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aic_control_interfaces__msg__JointMotionUpdate__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aic_control_interfaces__msg__JointMotionUpdate__Sequence__destroy(aic_control_interfaces__msg__JointMotionUpdate__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aic_control_interfaces__msg__JointMotionUpdate__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aic_control_interfaces__msg__JointMotionUpdate__Sequence__are_equal(const aic_control_interfaces__msg__JointMotionUpdate__Sequence * lhs, const aic_control_interfaces__msg__JointMotionUpdate__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aic_control_interfaces__msg__JointMotionUpdate__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aic_control_interfaces__msg__JointMotionUpdate__Sequence__copy(
  const aic_control_interfaces__msg__JointMotionUpdate__Sequence * input,
  aic_control_interfaces__msg__JointMotionUpdate__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aic_control_interfaces__msg__JointMotionUpdate);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aic_control_interfaces__msg__JointMotionUpdate * data =
      (aic_control_interfaces__msg__JointMotionUpdate *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aic_control_interfaces__msg__JointMotionUpdate__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aic_control_interfaces__msg__JointMotionUpdate__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aic_control_interfaces__msg__JointMotionUpdate__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
