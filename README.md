# SpinorSat-OpenTools

*What this repo includes:*

- A walkthrough of how to use datasets within repo
- A walkthrough on ML/AI approaches to specific problems
- Potential projects to work on



Please visit the resources_docs folder for more useful info! 



This ReadMe is useful for torquing and controlling the PCBSat you are developing. This utilizes magnetorquers in order to despin the initial spin of the PCBSat. 

![](/Images/gyro_torque_control.png)



Dependencies: igrf12 (https://github.com/scivision/igrf12)

Run ``python3 pull_iss_locdata.py``. This will collect (timestamp, latitude,longitude) data of the ISS for 9 hours at 10 second increments. This will create an output file in the current directory titled ``iss_loc_data_{timestamp}.csv``. You may edit the code to pull the data at a faster/slower rate.

Here is an example of the magnetic data from the ISS in X,Y,Z. Pretty neat! The units are Time vs Gauss.

![](/Images/Mag_data_ISS.jpg)

Run ``python3 data_gen.py -f iss_loc_data_{timestamp}.csv`` where timestamp corresponds to the file created in the previous step. This will create an output file in the current directory that contains magnetometer data (x,y,z), gyrometer data (x,y,z), and the expected axis and power that the PCBSat should rotate along in addition to the file's previous contents. This output file will be titled ``full_{timestamp}.csv``. The units for the magnetometer data are Gauss and the units for the gyrometer data are radians/second.  The units for power are a value between 0 to +/- 100 where 100 is the max current allowed through the magnetorquer.



Physics based controls:

![control_code_viz](/Images/control_code_viz.png)





We also have a mechanism for doing an ML approach for predicting the power to torque and orient the magnetorquer. We utilize Kernel Ridge Regression in order to translate the data into a learned space and then linearalize it within that space and generate a look up table of values that are now optimal for matching a perioidic input. With this method we were able to emulate our physics based conrtrol code with an accuracy of 98.9%. This example is shown in our python notebook. 

![](/Images/Kernal_Ridge_Regression_SpinorSat.png)



Resources for ChipSat Hackathon 3/15/2019

- [ ] Potentially Make DevPost
- [ ] Make a Demo Ipython Notebook

