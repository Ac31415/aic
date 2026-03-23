#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gz-plugin3::gz-plugin3-loader" for configuration "RelWithDebInfo"
set_property(TARGET gz-plugin3::gz-plugin3-loader APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gz-plugin3::gz-plugin3-loader PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libgz-plugin3-loader.3.1.0.dylib"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libgz-plugin3-loader.3.dylib"
  )

list(APPEND _cmake_import_check_targets gz-plugin3::gz-plugin3-loader )
list(APPEND _cmake_import_check_files_for_gz-plugin3::gz-plugin3-loader "${_IMPORT_PREFIX}/lib/libgz-plugin3-loader.3.1.0.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
