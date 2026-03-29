cat << 'EOF' > README.md
# ROS 2 Mapping Project

## What this project is about
This is a simple project where I worked on map building (mapping) in ROS 2 using TurtleBot3 inside Gazebo.  
The map is created using Cartographer and then saved for later use.

---

## Before you start
All commands should be run **inside the Docker container**.

To open it:
cd ~/ros2_ws
./docker_terminal.sh

---

## Requirements

Make sure you have the following installed:

- ROS 2 Humble
- Gazebo
- TurtleBot3
- Cartographer
- Navigation2

Install everything with:
sudo apt install ros-humble-gazebo-*
sudo apt install ros-humble-cartographer
sudo apt install ros-humble-cartographer-ros
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-turtlebot3-msgs
sudo apt install ros-humble-turtlebot3

---

## Build the workspace

Before running anything, build your workspace:

cd ~/ws
colcon build --symlink-install
source install/setup.bash

---

## Creating your own map

1. Start Gazebo:
gazebo

2. Inside Gazebo:
- go to Edit → Building Editor
- draw walls and rooms
- save the result as a `.world` file

3. Move the file here:
src/my_robot_controller/worlds/

---

## Launch setup

This file is used to run the simulation:
src/my_robot_controller/launch/turtlebot3_world.launch.py

Make sure it points to your correct `.world` file.

---

## Rebuild after changes

If you changed anything (world or launch files), rebuild:

colcon build
source install/setup.bash

---

## Running mapping

1. Start the world:
ros2 launch my_robot_controller turtlebot3_world.launch.py

2. Run Cartographer:
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True

3. Run mapping node:
ros2 run my_robot_controller mapping

---

## Saving the map

After the robot explores everything:

ros2 run nav2_map_server map_saver_cli -f ~/your_location/map_name

This will create:
- map_name.pgm
- map_name.yaml

---

## Project structure

src/
├── my_robot_controller/
│   ├── my_robot_controller/
│   │   └── mapping.py
│   ├── launch/
│   │   └── turtlebot3_world.launch.py
│   └── worlds/
├── MAIN_MAP.pgm
└── MAIN_MAP.yaml

---

## Notes
- Don’t save the map too early — let the robot explore properly
- If something doesn’t work, it’s usually a path issue
- Rebuild after any changes to avoid weird bugs

EOF
