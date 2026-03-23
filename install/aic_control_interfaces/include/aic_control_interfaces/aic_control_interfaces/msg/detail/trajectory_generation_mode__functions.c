// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from aic_control_interfaces:msg/TrajectoryGenerationMode.idl
// generated code does not contain a copyright notice
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
aic_control_interfaces__msg__TrajectoryGenerationMode__init(aic_control_interfaces__msg__TrajectoryGenerationMode * msg)
{
  if (!msg) {
    return false;
  }
  // mode
  return true;
}

void
aic_control_interfaces__msg__TrajectoryGenerationMode__fini(aic_control_interfaces__msg__TrajectoryGenerationMode * msg)
{
  if (!msg) {
    return;
  }
  // mode
}

bool
aic_control_interfaces__msg__TrajectoryGenerationMode__are_equal(const aic_control_interfaces__msg__TrajectoryGenerationMode * lhs, const aic_control_interfaces__msg__TrajectoryGenerationMode * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // mode
  if (lhs->mode != rhs->mode) {
    return false;
  }
  return true;
}

bool
aic_control_interfaces__msg__TrajectoryGenerationMode__copy(
  const aic_control_interfaces__msg__TrajectoryGenerationMode * input,
  aic_control_interfaces__msg__TrajectoryGenerationMode * output)
{
  if (!input || !output) {
    return false;
  }
  // mode
  output->mode = input->mode;
  return true;
}

aic_control_interfaces__msg__TrajectoryGenerationMode *
aic_control_interfaces__msg__TrajectoryGenerationMode__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__TrajectoryGenerationMode * msg = (aic_control_interfaces__msg__TrajectoryGenerationMode *)allocator.allocate(sizeof(aic_control_interfaces__msg__TrajectoryGenerationMode), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(aic_control_interfaces__msg__TrajectoryGenerationMode));
  bool success = aic_control_interfaces__msg__TrajectoryGenerationMode__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
aic_control_interfaces__msg__TrajectoryGenerationMode__destroy(aic_control_interfaces__msg__TrajectoryGenerationMode * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    aic_control_interfaces__msg__TrajectoryGenerationMode__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__init(aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__TrajectoryGenerationMode * data = NULL;

  if (size) {
    data = (aic_control_interfaces__msg__TrajectoryGenerationMode *)allocator.zero_allocate(size, sizeof(aic_control_interfaces__msg__TrajectoryGenerationMode), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = aic_control_interfaces__msg__TrajectoryGenerationMode__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        aic_control_interfaces__msg__TrajectoryGenerationMode__fini(&data[i - 1]);
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
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__fini(aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * array)
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
      aic_control_interfaces__msg__TrajectoryGenerationMode__fini(&array->data[i]);
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

aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence *
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * array = (aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence *)allocator.allocate(sizeof(aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__destroy(aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__are_equal(const aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * lhs, const aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!aic_control_interfaces__msg__TrajectoryGenerationMode__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence__copy(
  const aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * input,
  aic_control_interfaces__msg__TrajectoryGenerationMode__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(aic_control_interfaces__msg__TrajectoryGenerationMode);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    aic_control_interfaces__msg__TrajectoryGenerationMode * data =
      (aic_control_interfaces__msg__TrajectoryGenerationMode *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!aic_control_interfaces__msg__TrajectoryGenerationMode__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          aic_control_interfaces__msg__TrajectoryGenerationMode__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!aic_control_interfaces__msg__TrajectoryGenerationMode__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
