cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

find_package(gz-utils3 ${gz-utils_FIND_VERSION} REQUIRED COMPONENTS ${gz-utils_FIND_COMPONENTS})

# Set up the core library and add it to the list of all components
add_library(gz-utils::gz-utils ALIAS gz-utils3::gz-utils3)
add_library(gz-utils::core ALIAS gz-utils3::gz-utils3)

# Retrieve the list of components
get_target_property(components gz-utils3::requested INTERFACE_LINK_LIBRARIES)

foreach(component ${components})
  # Skip the core library
  if(${component} STREQUAL gz-utils3::gz-utils3)
    continue()
  endif()

  # Change "gz-libN::gz-libN-component" to "component"
  string(REGEX REPLACE "gz-utils3::gz-utils3-" "" component_name ${component})
  add_library(gz-utils::${component_name} ALIAS ${component})
endforeach()

# Add a root gz-lib alias
add_library(gz-utils ALIAS gz-utils3::gz-utils3)
