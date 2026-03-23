#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "diagnostic_aggregator::diagnostic_aggregator" for configuration ""
set_property(TARGET diagnostic_aggregator::diagnostic_aggregator APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(diagnostic_aggregator::diagnostic_aggregator PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdiagnostic_aggregator.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libdiagnostic_aggregator.dylib"
  )

list(APPEND _cmake_import_check_targets diagnostic_aggregator::diagnostic_aggregator )
list(APPEND _cmake_import_check_files_for_diagnostic_aggregator::diagnostic_aggregator "${_IMPORT_PREFIX}/lib/libdiagnostic_aggregator.dylib" )

# Import target "diagnostic_aggregator::diagnostic_aggregator_analyzers" for configuration ""
set_property(TARGET diagnostic_aggregator::diagnostic_aggregator_analyzers APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(diagnostic_aggregator::diagnostic_aggregator_analyzers PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libdiagnostic_aggregator_analyzers.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libdiagnostic_aggregator_analyzers.dylib"
  )

list(APPEND _cmake_import_check_targets diagnostic_aggregator::diagnostic_aggregator_analyzers )
list(APPEND _cmake_import_check_files_for_diagnostic_aggregator::diagnostic_aggregator_analyzers "${_IMPORT_PREFIX}/lib/libdiagnostic_aggregator_analyzers.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
