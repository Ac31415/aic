#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gz-utils3::gz-utils3" for configuration "RelWithDebInfo"
set_property(TARGET gz-utils3::gz-utils3 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gz-utils3::gz-utils3 PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libgz-utils3.3.1.1.dylib"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libgz-utils3.3.dylib"
  )

list(APPEND _cmake_import_check_targets gz-utils3::gz-utils3 )
list(APPEND _cmake_import_check_files_for_gz-utils3::gz-utils3 "${_IMPORT_PREFIX}/lib/libgz-utils3.3.1.1.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
