ROS 2 Humble Workspace (Docker-Based Setup)
---
This repository provides a Docker-based development environment for working with ROS 2 Humble.  
It is configured for TurtleBot3 simulation, mapping, and autonomous navigation.
The setup allows you to run a fully isolated ROS 2 environment without manual dependency management.

📦 Project Structure
---
`Dockerfile_current` — builds the ROS 2 environment with required packages

`docker-compose.yml` — container configuration and networking

`docker_terminal.sh` — script for launching and accessing the container

`ros2_ws/` — main ROS 2 workspace

Inside the workspace:

-`src/my_robot_controller/` — main ROS 2 package

-`worlds/` — custom Gazebo world

-`map/` — saved map files

-`launch/` — launch files for simulation and navigation

🚀 Getting Started
Requirements
---
Docker

Docker Compose

Run the Environment
```bash
chmod +x docker_terminal.sh
./docker_terminal.sh
```

Build the Workspace
Inside the container:
```bash
cd ~/ros2_ws  
colcon build --symlink-install  
source install/setup.bash  
```
---
⚙️ Environment Configuration
---
Preconfigured variables:

User: `student`

ROS_DOMAIN_ID: 30

TURTLEBOT3_MODEL: burger

ROS_LOCALHOST_ONLY: 1


🗺 Mapping (Task 1)
---
A custom environment is mapped using TurtleBot3 and Cartographer.
World file:
```bash
src/my_robot_controller/worlds/world.world
```
---
Run Mapping
---
Start simulation:
```bash
ros2 launch my_robot_controller turtlebot3_world.launch.py
```
Run SLAM:
```bash
ros2 launch turtlebot3_cartographer cartographer.launch.py
```
Run mapping node:
```bash
ros2 run my_robot_controller mapping
```
---
Save Map
```bash
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/my_robot_controller/map/my_map1
```
Generated files:
---
`my_map1.yaml`
`my_map1.pgm`

🧭 Autonomous Navigation (TASK 2)
---
Autonomous navigation is implemented using Navigation2.

Key Files
```bash
src/my_robot_controller/my_robot_controller/navigation.py
src/my_robot_controller/launch/run_navigation.launch.py
src/my_robot_controller/map/my_map1.yaml
```
---
Run Navigation
```bash
ros2 launch my_robot_controller run_navigation.launch.py
```
This command:
launches Gazebo

starts Navigation2

loads the saved map

runs the navigation script

🎮 Manual Navigation
---
Start simulation:
```bash
ros2 launch my_robot_controller turtlebot3_world.launch.py
```
Run Navigation2:
```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/ros2_ws/src/my_robot_controller/map/my_map1.yaml
```
In RViz:

use 2D Pose Estimate to set the start position

use Nav2 Goal to send goals

🎯 Project Overview
-
This project demonstrates:
working with ROS 2 in Docker

building maps using SLAM (Cartographer)

autonomous navigation using Navigation2

integration of Gazebo simulation with ROS 2


ROS2 Autoware Autonomous Navigation (Task 3)
--
Overview
This task demonstrates autonomous navigation using ROS 2 Humble and Autoware. A prebuilt map is used for localization, and the vehicle navigates to goal positions using Autoware’s planning and control stack. A custom controller (aw_navigation.py) is used to interact with the system.

Required packages
sudo apt install ros-humble-autoware

Workspace Setup
Clone the repository: git clone https://github.com/YOUR_USERNAME/ros2_ws.git

Navigate to workspace: cd ~/ros2_ws
. /autoware_terminal.sh
Build workspace: . /build_ws.sh


Running Custom Navigation with the custom launch file:
ros2 launch my_robot_controller car_nav.launch.py

Important Change (Terminal Usage)

In this task,we use: . /autoware_terminal.sh
instead of: ./docker_terminal.sh
This opens a terminal with Autoware environment already sourced.

Also important!
In the file explorer home library there has to be the map file (for example home/autoware_map/sample_map_planning/). It can be found in my github repository 


Navigation Behavior
* The vehicle waits for an initial pose
* Localization is handled by Autoware
* A goal is set in RViz
* Autoware plans and executes the path
* The vehicle reaches the goal while avoiding obstacles
