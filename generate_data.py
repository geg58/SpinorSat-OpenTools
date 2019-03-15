import numpy as np
import pandas as pd
import random
import math
import argparse
import igrf12
from sklearn.preprocessing import MinMaxScaler

# ----- Constants ----- #

# Torque Parameters
voltage = 0.1 # This is the voltage across the torque coil.
B = 0.00003 # This is magnetic field of the torque coil?
I = 0.3 # This parameter is the current going through the torque coil. This current can go either direction through the coils.
D = 0.001 # This parameter is set by the length of the PCB.
A = D * D # This parameter is set by the area of the PCB.
N = 200 # This parameter is set by the number of coils on a magnetorquer.

# Board Inertia Parameters
l = .035 # This parameter is set by the inertia and CoM of the PCB.
m = 0.005 # This parameter is set by the mass of the PCB.

torque_time = 0.1

# ----- Utility functions ----- #

def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]


def dot(a, b):
    return sum([i * j for i, j in zip(a, b)])

def rescale(old_value, old_min, old_max, new_min, new_max):
	new_value = ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
	return new_value

# ----- Data Generation functions ----- #

def torque(N, I, A, B, theta):
	return N * I * A * B * np.sin(theta)

def magnetorquer_output(m_data, g_data):
	'''

	m_data : 3 element array with magnetometer data in the x,y, and z direction. 
	g_data: 3 element array with gyrometer data in the x,y, and z direction. 

	'''

	magnetorquer_properties = [100, 100, 200]
	CONTROLLER_GAIN = 1 

	unit_dir = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
	angular = [cross(mu, m_data) for mu in unit_dir]
	similarity = [dot(angular[i], g_data)*magnetorquer_properties[i]
	                  for i in range(len(angular))]

	axis = np.argmax(np.abs(similarity))
	power = similarity[axis] / CONTROLLER_GAIN

	return axis, power

def add_mag(df):
	'''

	Calculates the magnetic field using the IGRF-12 coefficients. 

	Feel free to change altitude 

	'''
	altitude = 330 

	for i, row in df.iterrows():
		latitude = df.iloc[i][1]
		longitude = df.iloc[i][2]
		mag = igrf12.igrf('2010-07-12', glat=latitude,
		                  glon=longitude, alt_km=altitude)
		df.at[i, 'mag_x'] = mag.north.values[0] / 100000 - 0.2 
		df.at[i, 'mag_y'] = mag.east.values[0] / 100000
		df.at[i, 'mag_z'] = mag.down.values[0] / 100000

	return True


def add_gyro(df):
	'''
	Generates a random initialization for gyrometer x,y,z values and
	adds it to every row of the df
	'''
	gyro_x = random.uniform(-1, 1)
	gyro_y = random.uniform(-1, 1)

	z_range_one = random.uniform(-90, -60) 
	z_range_two = random.uniform(60, 90)
	out = np.stack((z_range_one,z_range_two))
	gyro_z = np.random.choice(out)

	df['gyro_x'] = math.radians(gyro_x)
	df['gyro_y'] = math.radians(gyro_y)
	df['gyro_z'] = math.radians(gyro_z)

	return True


def add_axis_power(df):
	axisLst = []
	powerLst = []
	for i, row in df.iterrows():
		x_i = df.iloc[i][3:9]
		mag_data = [x_i[0], x_i[1], x_i[2]]
		gyro_data = [x_i[3], x_i[4], x_i[5]]
		axis, power = magnetorquer_output(mag_data, gyro_data)

		axisLst.append(int(axis))
		powerLst.append(power)

	df['axis'] = axisLst
	df['power'] = powerLst

	scaler = MinMaxScaler()
	df['power_norm'] = scaler.fit_transform(df['power'].values.reshape(-1, 1))
	df['power_norm'] = df['power_norm'].apply(lambda x: x*100)


def update_gyro(df):
	g_data_arr = [[df.loc[0, 'gyro_x'], df.loc[0, 'gyro_y'], df.loc[0, 'gyro_z']]]
	for index, row in df.iterrows():
		m_data = [row['mag_x'], row['mag_y'], row['mag_z']]
		g_data = g_data_arr[index].copy()
		axis, power = magnetorquer_output(m_data, g_data)

		new_I = rescale(power, -15, 20, 0.1, 0.3)
		Is = I ** 4 / 3 * m

		angular_acc = torque(N, new_I, A, B, 1) / Is
		change_in_rot = angular_acc * torque_time
		g_data[axis] = g_data[axis] - change_in_rot
		g_data_arr.append(g_data)

	return g_data_arr



if __name__ == "__main__":
	'''
	python3 generate_data.py -f raw_data.csv
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-f','--file', help='Dataset containing mag data, gyro data, axis and power', required=True)
	args = vars(parser.parse_args())
	file_name = args['file']

	df = pd.read_csv(file_name)
	add_mag(df)
	add_gyro(df)
	add_axis_power(df)
	g_data_arr = update_gyro(df)
	g_data_arr = g_data_arr[:len(g_data_arr) - 1]
	df['gyro_x'] = np.array(g_data_arr).T[0]
	df['gyro_y'] = np.array(g_data_arr).T[1]
	df['gyro_z'] = np.array(g_data_arr).T[2]
	output_file_name = "final_{}".format(file_name)
	df.to_csv(output_file_name, index=False)

