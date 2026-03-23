#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "kinematics_interface_pinocchio::kinematics_interface_pinocchio" for configuration ""
set_property(TARGET kinematics_interface_pinocchio::kinematics_interface_pinocchio APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(kinematics_interface_pinocchio::kinematics_interface_pinocchio PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libkinematics_interface_pinocchio.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libkinematics_interface_pinocchio.dylib"
  )

list(APPEND _cmake_import_check_targets kinematics_interface_pinocchio::kinematics_interface_pinocchio )
list(APPEND _cmake_import_check_files_for_kinematics_interface_pinocchio::kinematics_interface_pinocchio "${_IMPORT_PREFIX}/lib/libkinematics_interface_pinocchio.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
