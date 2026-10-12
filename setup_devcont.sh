echo "Sourcing setup_devcont.sh ..."

export ROS_MASTER_URI=http://localhost:11311
export ROS_IP=127.0.0.1

if [ -f "$SCRIPT_DIR/devel/setup.bash" ] ; then
    . "$SCRIPT_DIR/devel/setup.bash"
else
    . /opt/ros/$ROS_DISTRO/setup.bash
fi

source $CONT_PWD/install/setup.bash
