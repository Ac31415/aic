#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gz-common6::gz-common6-geospatial" for configuration "RelWithDebInfo"
set_property(TARGET gz-common6::gz-common6-geospatial APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gz-common6::gz-common6-geospatial PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/libgz-common6-geospatial.6.2.1.dylib"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/libgz-common6-geospatial.6.dylib"
  )

list(APPEND _cmake_import_check_targets gz-common6::gz-common6-geospatial )
list(APPEND _cmake_import_check_files_for_gz-common6::gz-common6-geospatial "${_IMPORT_PREFIX}/lib/libgz-common6-geospatial.6.2.1.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
