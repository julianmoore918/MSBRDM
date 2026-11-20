# Requirements & Dependencies – MSBRDM Workspace

Setup guide for a fresh **native Ubuntu (dual boot)** install, replacing the previous WSL2 setup.
Everything below reproduces the environment this workspace was developed and tested in.

| Component | Version |
|---|---|
| OS | **Ubuntu 24.04 LTS** (Noble) – required for ROS 2 Jazzy |
| ROS 2 | **Jazzy Jalisco** |
| Python | 3.12 (Ubuntu default) |
| Build tool | colcon |

---

## 1. Base system

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential cmake git curl wget gnupg lsb-release \
                    software-properties-common locales
```

Locale (UTF-8 is required by ROS 2):
```bash
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

## 2. ROS 2 Jazzy

Enable the `universe` repository and add the ROS 2 apt source:
```bash
sudo add-apt-repository universe
sudo apt update && sudo apt install -y curl
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update && sudo apt upgrade -y
```
> If this step changes, follow the official guide: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

Install the full desktop variant (includes `rclpy`, `rviz2`, `tf2_ros`, `launch`, message packages, …):
```bash
sudo apt install -y ros-jazzy-desktop ros-dev-tools
```

## 3. ROS 2 packages used by the tutorials

```bash
sudo apt install -y \
  ros-jazzy-xacro \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-rviz2 \
  ros-jazzy-sensor-msgs-py \
  ros-jazzy-tf2-ros \
  ros-jazzy-tf2-tools \
  ros-jazzy-tf-transformations \
  ros-jazzy-plotjuggler-ros
```

| Package | Used for |
|---|---|
| `xacro` | building the UR10 / RPPR URDFs in the launch files |
| `robot_state_publisher` | TF tree + robot model in RViz |
| `joint_state_publisher(_gui)` | URDF tutorials, `ursa_apps` bringup |
| `rviz2` | visualisation (T2–T4) |
| `sensor_msgs_py` | point clouds in T4 (`yoshikawa_workspaces.py`) |
| `tf2_ros`, `tf2_tools` | TF broadcasting, `tf2_echo`, `view_frames` |
| `tf_transformations` | listed in some `package.xml` files (`ur_robot`, `msbrdm_libs`) |
| `plotjuggler-ros` | velocity plots in T3 |

## 4. Python packages (via apt, not pip)

```bash
sudo apt install -y \
  python3-numpy \
  python3-scipy \
  python3-sympy \
  python3-pandas \
  python3-matplotlib \
  python3-colorcet \
  python3-pytest \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  python3-argcomplete
```

| Package | Version tested | Used for |
|---|---|---|
| numpy | 1.26.4 | everywhere |
| scipy | 1.11.4 | quaternions (`scipy.spatial.transform.Rotation`) |
| sympy | 1.12 | symbolic kinematics / Jacobians (`*_model.py`, `msbrdm_libs`) |
| pandas | 2.1.4 | workspace samples in T4 |
| matplotlib | – | plots in T1 |
| colorcet | 3.0.1 | colour map in T4 |

> Use the `python3-*` apt packages. `pip install` into the system Python is blocked on Ubuntu 24.04
> (PEP 668), and the apt versions match what ROS 2 Jazzy is built against.

## 5. rosdep

```bash
sudo rosdep init
rosdep update
```

## 6. Shell setup (`~/.bashrc`)

```bash
echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
echo '[ -f ~/MSBRDM/Tutorial/julian_moore_ws/install/setup.bash ] && source ~/MSBRDM/Tutorial/julian_moore_ws/install/setup.bash' >> ~/.bashrc
echo "alias srcsetup='source install/setup.bash'" >> ~/.bashrc
echo "alias update_bash='source ~/.bashrc'" >> ~/.bashrc
source ~/.bashrc
```

## 7. Git & SSH

```bash
git config --global user.name  "Julian Moore"
git config --global user.email "<your email>"

ssh-keygen -t ed25519 -C "<your email>"
cat ~/.ssh/id_ed25519.pub        # add to GitLab (LRZ) and GitHub → Settings → SSH keys
```

`~/.ssh/config` – the LRZ GitLab needs this key-exchange setting (otherwise push/pull hangs):
```
Host gitlab.lrz.de
    KexAlgorithms curve25519-sha256
```
```bash
chmod 600 ~/.ssh/config
ssh -T git@gitlab.lrz.de
ssh -T git@github.com
```

## 8. Get and build the workspace

```bash
mkdir -p ~/MSBRDM/Tutorial && cd ~/MSBRDM/Tutorial
git clone git@gitlab.lrz.de:msbrdm/student-workspaces-2026/julian_moore_ws.git
cd julian_moore_ws

# remotes
git remote add upstream git@gitlab.lrz.de:msbrdm/msbrdm-lecture-2026.git
git remote add github   git@github.com:julianmoore918/MSBRDM.git

# missing system dependencies declared in the package.xml files
rosdep install --from-paths src --ignore-src -r -y

# build
colcon build --symlink-install
source install/setup.bash
```

Notes:
- `rosdep` will report a few keys it cannot resolve (`robo_state_publisher`, `rviz`, `tf_conversions`
  are typos / ROS 1 names in some template `package.xml` files). They can be ignored – `-r` continues anyway.
- After adding **new** launch/rviz files or changing `setup.py` / `package.xml`, rebuild the package:
  `colcon build --symlink-install --packages-select <pkg>`.

## 9. Editor (optional)

- **VS Code**: `sudo snap install code --classic`
  Extensions: Python, Pylance, ROS (ms-iot), XML, YAML.
- Pylance import paths for the workspace packages – `.vscode/settings.json`:
  ```json
  {
      "python.analysis.extraPaths": [
          "/opt/ros/jazzy/lib/python3.12/site-packages",
          "${workspaceFolder}/src/msbrdm_libs",
          "${workspaceFolder}/src/robot_models/ur_model",
          "${workspaceFolder}/src/robot_models/rppr_model",
          "${workspaceFolder}/src/simulated_robots/ur_robot",
          "${workspaceFolder}/src/simulated_robots/rppr_robot",
          "${workspaceFolder}/src/robot_controllers/ur_controllers/src"
      ]
  }
  ```

## 10. Smoke test

```bash
ros2 doctor --report | head -20
ros2 launch tutorial_3 ur10_node.launch.py                  # UR10 moving in RViz
ros2 launch tutorial_4 yoshikawa_workspaces.launch.py       # workspace point clouds
ros2 launch tutorial_4 ur10_kinematic_control_node.launch.py
ros2 run plotjuggler plotjuggler                            # opens the plot GUI
```

Differences to WSL: RViz / PlotJuggler run natively (no WSLg), so drag-and-drop in PlotJuggler works,
and GPU acceleration is available if the graphics driver is installed
(`sudo ubuntu-drivers autoinstall` for NVIDIA).
