# - Config to retrieve all components of the gz-tools2 package
#
# This should only be invoked by gz-tools2-config.cmake.
#
# To retrieve this meta-package, use:
# find_package(gz-tools2 COMPONENTS all)
#
# This creates the target gz-tools2::all which will link to all known
# components of gz-tools2, including the core library.
#
# This also creates the variable gz-tools2_ALL_LIBRARIES
#
################################################################################

cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

if(gz-tools2_ALL_CONFIG_INCLUDED)
  return()
endif()
set(gz-tools2_ALL_CONFIG_INCLUDED TRUE)

if(NOT gz-tools2-all_FIND_QUIETLY)
  message(STATUS "Looking for all libraries of gz-tools2 -- found version 2.0.3")
endif()


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was gz-all-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

# Get access to the find_dependency utility
include(CMakeFindDependencyMacro)

# Find the core library
find_dependency(gz-tools2 2.0.3 EXACT)

# Find the component libraries


if(NOT TARGET gz-tools2::gz-tools2-all)
  include("${CMAKE_CURRENT_LIST_DIR}/gz-tools2-all-targets.cmake")

  add_library(gz-tools2::all INTERFACE IMPORTED)
  set_target_properties(gz-tools2::all PROPERTIES
    INTERFACE_LINK_LIBRARIES "gz-tools2::gz-tools2-all")

endif()

# Create the "requested" target if it does not already exist
if(NOT TARGET gz-tools2::requested)
  add_library(gz-tools2::requested INTERFACE IMPORTED)
endif()

# Link the "all" target to the "requested" target
get_target_property(gz_requested_components gz-tools2::requested INTERFACE_LINK_LIBRARIES)
if(NOT gz_requested_components)
  set_target_properties(gz-tools2::requested PROPERTIES
    INTERFACE_LINK_LIBRARIES "gz-tools2::gz-tools2-all")
else()
  set_target_properties(gz-tools2::requested PROPERTIES
    INTERFACE_LINK_LIBRARIES "${gz_requested_components};gz-tools2::gz-tools2-all")
endif()

set(gz-tools2_ALL_LIBRARIES gz-tools2::gz-tools2-all)
