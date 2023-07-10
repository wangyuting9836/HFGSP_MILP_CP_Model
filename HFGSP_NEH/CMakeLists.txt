cmake_minimum_required(VERSION 3.25)
project(HFGSP_NEH)

set(CMAKE_CXX_STANDARD 14)
file(GLOB SOURCES
        *.h
        *.cpp
        )
add_executable(HFGSP_NEH ${SOURCES})

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
if (Python3_FOUND)
    message("Python include directory: " ${Python3_INCLUDE_DIRS})
    message("Python version is: " ${Python3_VERSION})
    message("Python libs is: " ${Python3_LIBRARIES})
    include_directories(${Python3_INCLUDE_DIRS})
    target_link_libraries(HFGSP_NEH ${Python3_LIBRARIES})
endif (Python3_FOUND)

include_directories("D:/coding_net/matplotlib-cpp")
include_directories("D:/Python311/Lib/site-packages/numpy/core/include")
