cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

find_package(gz-tools2 ${gz-tools_FIND_VERSION} REQUIRED COMPONENTS ${gz-tools_FIND_COMPONENTS})

# Set up the core library and add it to the list of all components
add_library(gz-tools::gz-tools ALIAS gz-tools2::gz-tools2)
add_library(gz-tools::core ALIAS gz-tools2::gz-tools2)

# Retrieve the list of components
get_target_property(components gz-tools2::requested INTERFACE_LINK_LIBRARIES)

foreach(component ${components})
  # Skip the core library
  if(${component} STREQUAL gz-tools2::gz-tools2)
    continue()
  endif()

  # Change "gz-libN::gz-libN-component" to "component"
  string(REGEX REPLACE "gz-tools2::gz-tools2-" "" component_name ${component})
  add_library(gz-tools::${component_name} ALIAS ${component})
endforeach()

# Add a root gz-lib alias
add_library(gz-tools ALIAS gz-tools2::gz-tools2)
