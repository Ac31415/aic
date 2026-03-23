// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from aic_control_interfaces:msg/TrajectoryGenerationMode.idl
// generated code does not contain a copyright notice

#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_aic_control_interfaces
const rosidl_type_hash_t *
aic_control_interfaces__msg__TrajectoryGenerationMode__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x08, 0x10, 0xb7, 0x7c, 0xac, 0xbc, 0x1e, 0x05,
      0x50, 0xa7, 0xa6, 0x73, 0x99, 0x70, 0xc2, 0x12,
      0x97, 0x9f, 0xde, 0x8a, 0xc0, 0x81, 0x08, 0x5c,
      0xdd, 0xe7, 0xa8, 0xce, 0xa4, 0x4e, 0xf0, 0x6d,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME[] = "aic_control_interfaces/msg/TrajectoryGenerationMode";

// Define type names, field names, and default values
static char aic_control_interfaces__msg__TrajectoryGenerationMode__FIELD_NAME__mode[] = "mode";

static rosidl_runtime_c__type_description__Field aic_control_interfaces__msg__TrajectoryGenerationMode__FIELDS[] = {
  {
    {aic_control_interfaces__msg__TrajectoryGenerationMode__FIELD_NAME__mode, 4, 4},
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
aic_control_interfaces__msg__TrajectoryGenerationMode__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME, 51, 51},
      {aic_control_interfaces__msg__TrajectoryGenerationMode__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# There are two ways that input targets can be provided for the MotionUpdate message.\n"
  "#   1. mode = MODE_VELOCITY\n"
  "#      In this case, a target velocity must be provided. The target pose\n"
  "#      will be ignored.\n"
  "#   2. mode = MODE_POSITION\n"
  "#      In this case, a target pose must be provided. The target velocity\n"
  "#      will be ignored.\n"
  "# Notes that messages with mode set to MODE_UNSPECIFIED will be ignored.\n"
  "uint8 MODE_UNSPECIFIED = 0\n"
  "uint8 MODE_VELOCITY = 1\n"
  "uint8 MODE_POSITION = 2\n"
  "uint8 mode";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
aic_control_interfaces__msg__TrajectoryGenerationMode__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME, 51, 51},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 495, 495},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
aic_control_interfaces__msg__TrajectoryGenerationMode__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *aic_control_interfaces__msg__TrajectoryGenerationMode__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
