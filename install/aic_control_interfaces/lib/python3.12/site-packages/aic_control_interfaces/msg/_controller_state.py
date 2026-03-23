# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aic_control_interfaces:msg/ControllerState.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# Member 'tcp_error'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ControllerState(type):
    """Metaclass of message 'ControllerState'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('aic_control_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'aic_control_interfaces.msg.ControllerState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__controller_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__controller_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__controller_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__controller_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__controller_state

            from aic_control_interfaces.msg import TargetMode
            if TargetMode.__class__._TYPE_SUPPORT is None:
                TargetMode.__class__.__import_type_support__()

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

            from geometry_msgs.msg import WrenchStamped
            if WrenchStamped.__class__._TYPE_SUPPORT is None:
                WrenchStamped.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

            from trajectory_msgs.msg import JointTrajectoryPoint
            if JointTrajectoryPoint.__class__._TYPE_SUPPORT is None:
                JointTrajectoryPoint.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ControllerState(metaclass=Metaclass_ControllerState):
    """Message class 'ControllerState'."""

    __slots__ = [
        '_header',
        '_tcp_pose',
        '_tcp_velocity',
        '_reference_tcp_pose',
        '_tcp_error',
        '_reference_joint_state',
        '_target_mode',
        '_fts_tare_offset',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'tcp_pose': 'geometry_msgs/Pose',
        'tcp_velocity': 'geometry_msgs/Twist',
        'reference_tcp_pose': 'geometry_msgs/Pose',
        'tcp_error': 'double[6]',
        'reference_joint_state': 'trajectory_msgs/JointTrajectoryPoint',
        'target_mode': 'aic_control_interfaces/TargetMode',
        'fts_tare_offset': 'geometry_msgs/WrenchStamped',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 6),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['trajectory_msgs', 'msg'], 'JointTrajectoryPoint'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aic_control_interfaces', 'msg'], 'TargetMode'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'WrenchStamped'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        if 'check_fields' in kwargs:
            self._check_fields = kwargs['check_fields']
        else:
            self._check_fields = ros_python_check_fields == '1'
        if self._check_fields:
            assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
                'Invalid arguments passed to constructor: %s' % \
                ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        from geometry_msgs.msg import Pose
        self.tcp_pose = kwargs.get('tcp_pose', Pose())
        from geometry_msgs.msg import Twist
        self.tcp_velocity = kwargs.get('tcp_velocity', Twist())
        from geometry_msgs.msg import Pose
        self.reference_tcp_pose = kwargs.get('reference_tcp_pose', Pose())
        if 'tcp_error' not in kwargs:
            self.tcp_error = numpy.zeros(6, dtype=numpy.float64)
        else:
            self.tcp_error = kwargs.get('tcp_error')
        from trajectory_msgs.msg import JointTrajectoryPoint
        self.reference_joint_state = kwargs.get('reference_joint_state', JointTrajectoryPoint())
        from aic_control_interfaces.msg import TargetMode
        self.target_mode = kwargs.get('target_mode', TargetMode())
        from geometry_msgs.msg import WrenchStamped
        self.fts_tare_offset = kwargs.get('fts_tare_offset', WrenchStamped())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    if self._check_fields:
                        assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.tcp_pose != other.tcp_pose:
            return False
        if self.tcp_velocity != other.tcp_velocity:
            return False
        if self.reference_tcp_pose != other.reference_tcp_pose:
            return False
        if any(self.tcp_error != other.tcp_error):
            return False
        if self.reference_joint_state != other.reference_joint_state:
            return False
        if self.target_mode != other.target_mode:
            return False
        if self.fts_tare_offset != other.fts_tare_offset:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if self._check_fields:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def tcp_pose(self):
        """Message field 'tcp_pose'."""
        return self._tcp_pose

    @tcp_pose.setter
    def tcp_pose(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'tcp_pose' field must be a sub message of type 'Pose'"
        self._tcp_pose = value

    @builtins.property
    def tcp_velocity(self):
        """Message field 'tcp_velocity'."""
        return self._tcp_velocity

    @tcp_velocity.setter
    def tcp_velocity(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'tcp_velocity' field must be a sub message of type 'Twist'"
        self._tcp_velocity = value

    @builtins.property
    def reference_tcp_pose(self):
        """Message field 'reference_tcp_pose'."""
        return self._reference_tcp_pose

    @reference_tcp_pose.setter
    def reference_tcp_pose(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'reference_tcp_pose' field must be a sub message of type 'Pose'"
        self._reference_tcp_pose = value

    @builtins.property
    def tcp_error(self):
        """Message field 'tcp_error'."""
        return self._tcp_error

    @tcp_error.setter
    def tcp_error(self, value):
        if self._check_fields:
            if isinstance(value, numpy.ndarray):
                assert value.dtype == numpy.float64, \
                    "The 'tcp_error' numpy.ndarray() must have the dtype of 'numpy.float64'"
                assert value.size == 6, \
                    "The 'tcp_error' numpy.ndarray() must have a size of 6"
                self._tcp_error = value
                return
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'tcp_error' field must be a set or sequence with length 6 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._tcp_error = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def reference_joint_state(self):
        """Message field 'reference_joint_state'."""
        return self._reference_joint_state

    @reference_joint_state.setter
    def reference_joint_state(self, value):
        if self._check_fields:
            from trajectory_msgs.msg import JointTrajectoryPoint
            assert \
                isinstance(value, JointTrajectoryPoint), \
                "The 'reference_joint_state' field must be a sub message of type 'JointTrajectoryPoint'"
        self._reference_joint_state = value

    @builtins.property
    def target_mode(self):
        """Message field 'target_mode'."""
        return self._target_mode

    @target_mode.setter
    def target_mode(self, value):
        if self._check_fields:
            from aic_control_interfaces.msg import TargetMode
            assert \
                isinstance(value, TargetMode), \
                "The 'target_mode' field must be a sub message of type 'TargetMode'"
        self._target_mode = value

    @builtins.property
    def fts_tare_offset(self):
        """Message field 'fts_tare_offset'."""
        return self._fts_tare_offset

    @fts_tare_offset.setter
    def fts_tare_offset(self, value):
        if self._check_fields:
            from geometry_msgs.msg import WrenchStamped
            assert \
                isinstance(value, WrenchStamped), \
                "The 'fts_tare_offset' field must be a sub message of type 'WrenchStamped'"
        self._fts_tare_offset = value
