#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "diagnostic_updater::diagnostic_updater" for configuration ""
set_property(TARGET diagnostic_updater::diagnostic_updater APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(diagnostic_updater::diagnostic_updater PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdiagnostic_updater.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libdiagnostic_updater.dylib"
  )

list(APPEND _cmake_import_check_targets diagnostic_updater::diagnostic_updater )
list(APPEND _cmake_import_check_files_for_diagnostic_updater::diagnostic_updater "${_IMPORT_PREFIX}/lib/libdiagnostic_updater.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
