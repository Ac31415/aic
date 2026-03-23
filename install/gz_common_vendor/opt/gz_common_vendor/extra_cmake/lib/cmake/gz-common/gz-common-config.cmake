cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

find_package(gz-common6 ${gz-common_FIND_VERSION} REQUIRED COMPONENTS ${gz-common_FIND_COMPONENTS})

# Set up the core library and add it to the list of all components
add_library(gz-common::gz-common ALIAS gz-common6::gz-common6)
add_library(gz-common::core ALIAS gz-common6::gz-common6)

# Retrieve the list of components
get_target_property(components gz-common6::requested INTERFACE_LINK_LIBRARIES)

foreach(component ${components})
  # Skip the core library
  if(${component} STREQUAL gz-common6::gz-common6)
    continue()
  endif()

  # Change "gz-libN::gz-libN-component" to "component"
  string(REGEX REPLACE "gz-common6::gz-common6-" "" component_name ${component})
  add_library(gz-common::${component_name} ALIAS ${component})
endforeach()

# Add a root gz-lib alias
add_library(gz-common ALIAS gz-common6::gz-common6)
