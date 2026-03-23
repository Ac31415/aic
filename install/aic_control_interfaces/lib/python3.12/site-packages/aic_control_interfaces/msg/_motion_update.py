# generated from rosidl_generator_py/resource/_idl.py.em
# with input from aic_control_interfaces:msg/MotionUpdate.idl
# generated code does not contain a copyright notice

# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
from os import getenv

ros_python_check_fields = getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# Member 'target_stiffness'
# Member 'target_damping'
# Member 'wrench_feedback_gains_at_tip'
import numpy  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MotionUpdate(type):
    """Metaclass of message 'MotionUpdate'."""

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
                'aic_control_interfaces.msg.MotionUpdate')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__motion_update
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__motion_update
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__motion_update
            cls._TYPE_SUPPORT = module.type_support_msg__msg__motion_update
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__motion_update

            from aic_control_interfaces.msg import TrajectoryGenerationMode
            if TrajectoryGenerationMode.__class__._TYPE_SUPPORT is None:
                TrajectoryGenerationMode.__class__.__import_type_support__()

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

            from geometry_msgs.msg import Wrench
            if Wrench.__class__._TYPE_SUPPORT is None:
                Wrench.__class__.__import_type_support__()

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MotionUpdate(metaclass=Metaclass_MotionUpdate):
    """Message class 'MotionUpdate'."""

    __slots__ = [
        '_header',
        '_pose',
        '_velocity',
        '_target_stiffness',
        '_target_damping',
        '_feedforward_wrench_at_tip',
        '_wrench_feedback_gains_at_tip',
        '_trajectory_generation_mode',
        '_check_fields',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'pose': 'geometry_msgs/Pose',
        'velocity': 'geometry_msgs/Twist',
        'target_stiffness': 'double[36]',
        'target_damping': 'double[36]',
        'feedforward_wrench_at_tip': 'geometry_msgs/Wrench',
        'wrench_feedback_gains_at_tip': 'double[6]',
        'trajectory_generation_mode': 'aic_control_interfaces/TrajectoryGenerationMode',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 36),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 36),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Wrench'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('double'), 6),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['aic_control_interfaces', 'msg'], 'TrajectoryGenerationMode'),  # noqa: E501
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
        self.pose = kwargs.get('pose', Pose())
        from geometry_msgs.msg import Twist
        self.velocity = kwargs.get('velocity', Twist())
        if 'target_stiffness' not in kwargs:
            self.target_stiffness = numpy.zeros(36, dtype=numpy.float64)
        else:
            self.target_stiffness = kwargs.get('target_stiffness')
        if 'target_damping' not in kwargs:
            self.target_damping = numpy.zeros(36, dtype=numpy.float64)
        else:
            self.target_damping = kwargs.get('target_damping')
        from geometry_msgs.msg import Wrench
        self.feedforward_wrench_at_tip = kwargs.get('feedforward_wrench_at_tip', Wrench())
        if 'wrench_feedback_gains_at_tip' not in kwargs:
            self.wrench_feedback_gains_at_tip = numpy.zeros(6, dtype=numpy.float64)
        else:
            self.wrench_feedback_gains_at_tip = kwargs.get('wrench_feedback_gains_at_tip')
        from aic_control_interfaces.msg import TrajectoryGenerationMode
        self.trajectory_generation_mode = kwargs.get('trajectory_generation_mode', TrajectoryGenerationMode())

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
        if self.pose != other.pose:
            return False
        if self.velocity != other.velocity:
            return False
        if any(self.target_stiffness != other.target_stiffness):
            return False
        if any(self.target_damping != other.target_damping):
            return False
        if self.feedforward_wrench_at_tip != other.feedforward_wrench_at_tip:
            return False
        if any(self.wrench_feedback_gains_at_tip != other.wrench_feedback_gains_at_tip):
            return False
        if self.trajectory_generation_mode != other.trajectory_generation_mode:
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
    def pose(self):
        """Message field 'pose'."""
        return self._pose

    @pose.setter
    def pose(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'pose' field must be a sub message of type 'Pose'"
        self._pose = value

    @builtins.property
    def velocity(self):
        """Message field 'velocity'."""
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'velocity' field must be a sub message of type 'Twist'"
        self._velocity = value

    @builtins.property
    def target_stiffness(self):
        """Message field 'target_stiffness'."""
        return self._target_stiffness

    @target_stiffness.setter
    def target_stiffness(self, value):
        if self._check_fields:
            if isinstance(value, numpy.ndarray):
                assert value.dtype == numpy.float64, \
                    "The 'target_stiffness' numpy.ndarray() must have the dtype of 'numpy.float64'"
                assert value.size == 36, \
                    "The 'target_stiffness' numpy.ndarray() must have a size of 36"
                self._target_stiffness = value
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
                 len(value) == 36 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'target_stiffness' field must be a set or sequence with length 36 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._target_stiffness = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def target_damping(self):
        """Message field 'target_damping'."""
        return self._target_damping

    @target_damping.setter
    def target_damping(self, value):
        if self._check_fields:
            if isinstance(value, numpy.ndarray):
                assert value.dtype == numpy.float64, \
                    "The 'target_damping' numpy.ndarray() must have the dtype of 'numpy.float64'"
                assert value.size == 36, \
                    "The 'target_damping' numpy.ndarray() must have a size of 36"
                self._target_damping = value
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
                 len(value) == 36 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -1.7976931348623157e+308 or val > 1.7976931348623157e+308) or math.isinf(val) for val in value)), \
                "The 'target_damping' field must be a set or sequence with length 36 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._target_damping = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def feedforward_wrench_at_tip(self):
        """Message field 'feedforward_wrench_at_tip'."""
        return self._feedforward_wrench_at_tip

    @feedforward_wrench_at_tip.setter
    def feedforward_wrench_at_tip(self, value):
        if self._check_fields:
            from geometry_msgs.msg import Wrench
            assert \
                isinstance(value, Wrench), \
                "The 'feedforward_wrench_at_tip' field must be a sub message of type 'Wrench'"
        self._feedforward_wrench_at_tip = value

    @builtins.property
    def wrench_feedback_gains_at_tip(self):
        """Message field 'wrench_feedback_gains_at_tip'."""
        return self._wrench_feedback_gains_at_tip

    @wrench_feedback_gains_at_tip.setter
    def wrench_feedback_gains_at_tip(self, value):
        if self._check_fields:
            if isinstance(value, numpy.ndarray):
                assert value.dtype == numpy.float64, \
                    "The 'wrench_feedback_gains_at_tip' numpy.ndarray() must have the dtype of 'numpy.float64'"
                assert value.size == 6, \
                    "The 'wrench_feedback_gains_at_tip' numpy.ndarray() must have a size of 6"
                self._wrench_feedback_gains_at_tip = value
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
                "The 'wrench_feedback_gains_at_tip' field must be a set or sequence with length 6 and each value of type 'float' and each double in [-179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000, 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000]"
        self._wrench_feedback_gains_at_tip = numpy.array(value, dtype=numpy.float64)

    @builtins.property
    def trajectory_generation_mode(self):
        """Message field 'trajectory_generation_mode'."""
        return self._trajectory_generation_mode

    @trajectory_generation_mode.setter
    def trajectory_generation_mode(self, value):
        if self._check_fields:
            from aic_control_interfaces.msg import TrajectoryGenerationMode
            assert \
                isinstance(value, TrajectoryGenerationMode), \
                "The 'trajectory_generation_mode' field must be a sub message of type 'TrajectoryGenerationMode'"
        self._trajectory_generation_mode = value
