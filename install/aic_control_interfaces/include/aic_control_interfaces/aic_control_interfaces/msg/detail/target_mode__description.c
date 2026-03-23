// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from aic_control_interfaces:msg/TargetMode.idl
// generated code does not contain a copyright notice

#include "aic_control_interfaces/msg/detail/target_mode__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_aic_control_interfaces
const rosidl_type_hash_t *
aic_control_interfaces__msg__TargetMode__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd1, 0xe9, 0xf0, 0xa2, 0x1c, 0x03, 0xd5, 0xfe,
      0x82, 0x3c, 0xd1, 0xdf, 0xb2, 0xbe, 0x0b, 0xc1,
      0x93, 0xfb, 0x53, 0xa7, 0x75, 0xb0, 0x9b, 0x31,
      0x7a, 0x5c, 0x0f, 0xda, 0x56, 0xaf, 0x5a, 0x24,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char aic_control_interfaces__msg__TargetMode__TYPE_NAME[] = "aic_control_interfaces/msg/TargetMode";

// Define type names, field names, and default values
static char aic_control_interfaces__msg__TargetMode__FIELD_NAME__mode[] = "mode";

static rosidl_runtime_c__type_description__Field aic_control_interfaces__msg__TargetMode__FIELDS[] = {
  {
    {aic_control_interfaces__msg__TargetMode__FIELD_NAME__mode, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
aic_control_interfaces__msg__TargetMode__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {aic_control_interfaces__msg__TargetMode__TYPE_NAME, 37, 37},
      {aic_control_interfaces__msg__TargetMode__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# There are two types of target modes.\n"
  "#   1. target_mode = MODE_CARTESIAN\n"
  "#      The controller will process Cartesian targets of type 'MotionUpdate' and \n"
  "#      ignore other target types\n"
  "#   2. target_mode = MODE_JOINT\n"
  "#      The controller will process joint targets of type 'JointMotionUpdate' and \n"
  "#      ignore other target types.\n"
  "uint8 MODE_UNSPECIFIED = 0 \n"
  "uint8 MODE_CARTESIAN = 1   \n"
  "uint8 MODE_JOINT = 2       \n"
  "uint8 mode";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
aic_control_interfaces__msg__TargetMode__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {aic_control_interfaces__msg__TargetMode__TYPE_NAME, 37, 37},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 432, 432},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
aic_control_interfaces__msg__TargetMode__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *aic_control_interfaces__msg__TargetMode__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
