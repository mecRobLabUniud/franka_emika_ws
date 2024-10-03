# Instructions to get ready with minimum time-jerk trajectory tests

## Steup
* **Windows PC** with orange label (password written on it)
* **This PC** with pink label (password written on it)
* **National Instruments sensors and modules** all inside the box
* **Panda Robot**

## Initialize the robot
Switch on the robot controller manually.
Set Ethernet(enp4s0) on the top-right corner of the screen to "Right robot".
On Chrome, search the Desk page by digiting ip "172.16.0.2" in the URL search bar.
Click the "Unlock" icon under the section "Joints" in the right side of the page.
If the robot light is blue, robot is ready to work.
If the robot light is white, robot is in free-ride mode, and you got to unlock the change mode button on the desk.
To move robot in free-ride mode you got to grab the end effector and press at the same time the two buttons placed on it.
Then you can move the robot as yuo want by pulling and pushing it.


## Connection between PCs
Connect one side of the ethernet cable to the port on the Windows PC and the other side to the lower port on this PC.
On this PC, set Ethernet(enp3s0) on the top-right corner of the screen to "UDP connection".
On this PC, to check the connection, write on terminal:
```shell script
ping 172.16.1.1
```

# Minimum time-jerk trajectories tests

Make sure that the National Instrument modules are connected to the Windows PC through the USB cable and to the electric line.
Connect also keyboard and mouse if not already connected to Windows PC.
Both on Windows and this PC, add your trajectory files in the "Desktop/Data_Ottimizzatore/Histrogram/CUSTOM_TRAJ" folder.
Trajectory data must be organized in a certain way, otherwise programs will not find the correct path.
On the Windows PC launch "MAIN.vi" program from desktop with double click.
Select the trajectory you want to perform and all the other setups in the Front Panel, by means of the buttons.
On this PC, to obtain super user permissions, write on terminal:
```shell script
sudo -s
```
On this PC, to launch the control program, write on terminal:
```shell script
roslaunch path_planning start_test.launch
```
On Windows PC, to start the tests, press Run button on the top-left corner of the Front Panel.