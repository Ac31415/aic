cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

find_package(gz-plugin3 ${gz-plugin_FIND_VERSION} REQUIRED COMPONENTS ${gz-plugin_FIND_COMPONENTS})

# Set up the core library and add it to the list of all components
add_library(gz-plugin::gz-plugin ALIAS gz-plugin3::gz-plugin3)
add_library(gz-plugin::core ALIAS gz-plugin3::gz-plugin3)

# Retrieve the list of components
get_target_property(components gz-plugin3::requested INTERFACE_LINK_LIBRARIES)

foreach(component ${components})
  # Skip the core library
  if(${component} STREQUAL gz-plugin3::gz-plugin3)
    continue()
  endif()

  # Change "gz-libN::gz-libN-component" to "component"
  string(REGEX REPLACE "gz-plugin3::gz-plugin3-" "" component_name ${component})
  add_library(gz-plugin::${component_name} ALIAS ${component})
endforeach()

# Add a root gz-lib alias
add_library(gz-plugin ALIAS gz-plugin3::gz-plugin3)
