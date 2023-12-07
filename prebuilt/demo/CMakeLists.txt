cmake_minimum_required(VERSION 3.15)

project(picolibc_demo LANGUAGES CXX)

find_package(prebuilt-picolibc REQUIRED)

add_executable(picolibc_demo main.cpp)
target_link_libraries(picolibc_demo picolibc)
