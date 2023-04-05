cmake_minimum_required(VERSION 3.0.2)
project(ai_kubeflow_demo)

find_package(catkin REQUIRED COMPONENTS std_msgs sensor_msgs cv_bridge)

catkin_package()

catkin_python_setup()

catkin_install_python(PROGRAMS
  src/ai_kubeflow_demo/ai_kubeflow_demo.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(FILES
  launch/demo.launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
