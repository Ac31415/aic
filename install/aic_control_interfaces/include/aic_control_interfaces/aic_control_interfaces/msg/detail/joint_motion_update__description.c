// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from aic_control_interfaces:msg/JointMotionUpdate.idl
// generated code does not contain a copyright notice

#include "aic_control_interfaces/msg/detail/joint_motion_update__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_aic_control_interfaces
const rosidl_type_hash_t *
aic_control_interfaces__msg__JointMotionUpdate__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xba, 0xaa, 0xe2, 0xa9, 0x83, 0xe6, 0x73, 0xe1,
      0x91, 0xe3, 0xa6, 0x92, 0xeb, 0x2d, 0x7d, 0xf3,
      0x80, 0x52, 0x37, 0x1e, 0xc0, 0x07, 0x68, 0x80,
      0xda, 0x37, 0xcf, 0xe5, 0xff, 0x14, 0x2a, 0xbd,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "aic_control_interfaces/msg/detail/trajectory_generation_mode__functions.h"
#include "builtin_interfaces/msg/detail/duration__functions.h"
#include "trajectory_msgs/msg/detail/joint_trajectory_point__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t aic_control_interfaces__msg__TrajectoryGenerationMode__EXPECTED_HASH = {1, {
    0x08, 0x10, 0xb7, 0x7c, 0xac, 0xbc, 0x1e, 0x05,
    0x50, 0xa7, 0xa6, 0x73, 0x99, 0x70, 0xc2, 0x12,
    0x97, 0x9f, 0xde, 0x8a, 0xc0, 0x81, 0x08, 0x5c,
    0xdd, 0xe7, 0xa8, 0xce, 0xa4, 0x4e, 0xf0, 0x6d,
  }};
static const rosidl_type_hash_t builtin_interfaces__msg__Duration__EXPECTED_HASH = {1, {
    0xe8, 0xd0, 0x09, 0xf6, 0x59, 0x81, 0x6f, 0x75,
    0x8b, 0x75, 0x33, 0x4e, 0xe1, 0xa9, 0xca, 0x5b,
    0x5c, 0x0b, 0x85, 0x98, 0x43, 0x26, 0x1f, 0x14,
    0xc7, 0xf9, 0x37, 0x34, 0x95, 0x99, 0xd9, 0x3b,
  }};
static const rosidl_type_hash_t trajectory_msgs__msg__JointTrajectoryPoint__EXPECTED_HASH = {1, {
    0xde, 0x89, 0x07, 0x03, 0x6d, 0x8b, 0xd4, 0x5a,
    0xac, 0x6f, 0x30, 0xcc, 0x90, 0x44, 0xa3, 0xd4,
    0xa3, 0x29, 0xc4, 0x2c, 0xbf, 0x71, 0x9a, 0xff,
    0x7d, 0x95, 0xa5, 0x84, 0xcf, 0xa5, 0x32, 0xd7,
  }};
#endif

static char aic_control_interfaces__msg__JointMotionUpdate__TYPE_NAME[] = "aic_control_interfaces/msg/JointMotionUpdate";
static char aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME[] = "aic_control_interfaces/msg/TrajectoryGenerationMode";
static char builtin_interfaces__msg__Duration__TYPE_NAME[] = "builtin_interfaces/msg/Duration";
static char trajectory_msgs__msg__JointTrajectoryPoint__TYPE_NAME[] = "trajectory_msgs/msg/JointTrajectoryPoint";

// Define type names, field names, and default values
static char aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_state[] = "target_state";
static char aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_stiffness[] = "target_stiffness";
static char aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_damping[] = "target_damping";
static char aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__trajectory_generation_mode[] = "trajectory_generation_mode";
static char aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_feedforward_torque[] = "target_feedforward_torque";

static rosidl_runtime_c__type_description__Field aic_control_interfaces__msg__JointMotionUpdate__FIELDS[] = {
  {
    {aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_state, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {trajectory_msgs__msg__JointTrajectoryPoint__TYPE_NAME, 40, 40},
    },
    {NULL, 0, 0},
  },
  {
    {aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_stiffness, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_damping, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__trajectory_generation_mode, 26, 26},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME, 51, 51},
    },
    {NULL, 0, 0},
  },
  {
    {aic_control_interfaces__msg__JointMotionUpdate__FIELD_NAME__target_feedforward_torque, 25, 25},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription aic_control_interfaces__msg__JointMotionUpdate__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {aic_control_interfaces__msg__TrajectoryGenerationMode__TYPE_NAME, 51, 51},
    {NULL, 0, 0},
  },
  {
    {builtin_interfaces__msg__Duration__TYPE_NAME, 31, 31},
    {NULL, 0, 0},
  },
  {
    {trajectory_msgs__msg__JointTrajectoryPoint__TYPE_NAME, 40, 40},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
aic_control_interfaces__msg__JointMotionUpdate__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {aic_control_interfaces__msg__JointMotionUpdate__TYPE_NAME, 44, 44},
      {aic_control_interfaces__msg__JointMotionUpdate__FIELDS, 5, 5},
    },
    {aic_control_interfaces__msg__JointMotionUpdate__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
  };
  if (!constructed) {
    assert(0 == memcmp(&aic_control_interfaces__msg__TrajectoryGenerationMode__EXPECTED_HASH, aic_control_interfaces__msg__TrajectoryGenerationMode__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = aic_control_interfaces__msg__TrajectoryGenerationMode__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&builtin_interfaces__msg__Duration__EXPECTED_HASH, builtin_interfaces__msg__Duration__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = builtin_interfaces__msg__Duration__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&trajectory_msgs__msg__JointTrajectoryPoint__EXPECTED_HASH, trajectory_msgs__msg__JointTrajectoryPoint__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = trajectory_msgs__msg__JointTrajectoryPoint__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Command the robot to a target joint state.\n"
  "\n"
  "# The target joint configuration including set points for positions,\n"
  "# velocities, accelerations, and efforts.\n"
  "trajectory_msgs/JointTrajectoryPoint target_state\n"
  "\n"
  "# Stiffness and damping both evolve from a current value toward these target\n"
  "# ones. This avoids sudden jumps when the values are changed.\n"
  "# Specify for each joint.\n"
  "float64[] target_stiffness\n"
  "float64[] target_damping\n"
  "\n"
  "# [OPTIONAL] The mode of trajectory generation.\n"
  "TrajectoryGenerationMode trajectory_generation_mode\n"
  "\n"
  "float64[] target_feedforward_torque\n"
  "";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
aic_control_interfaces__msg__JointMotionUpdate__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {aic_control_interfaces__msg__JointMotionUpdate__TYPE_NAME, 44, 44},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 564, 564},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
aic_control_interfaces__msg__JointMotionUpdate__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *aic_control_interfaces__msg__JointMotionUpdate__get_individual_type_description_source(NULL),
    sources[1] = *aic_control_interfaces__msg__TrajectoryGenerationMode__get_individual_type_description_source(NULL);
    sources[2] = *builtin_interfaces__msg__Duration__get_individual_type_description_source(NULL);
    sources[3] = *trajectory_msgs__msg__JointTrajectoryPoint__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
