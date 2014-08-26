cmake_minimum_required(VERSION 2.8.3)
project(husky_rtkgps_serialbridge)

find_package(catkin REQUIRED)

catkin_package()

install(
  DIRECTORY launch scripts
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

