# cmake needs this line
cmake_minimum_required(VERSION 2.8)
project( latency )

# Enable C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
SET(CMAKE_CXX_FLAGS "-std=c++11 -O2 -mcpu=cortex-a53")

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )

include_directories( ./include )
aux_source_directory(./src DIR_SRCS)
add_executable( latency ${DIR_SRCS} )

target_link_libraries(latency ${OpenCV_LIBS} yaml-cpp)
target_link_libraries(latency pthread hineon n2cube)
