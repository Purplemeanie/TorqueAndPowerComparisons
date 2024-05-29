# Compare Torques
import pprint
import csv
import numpy as np
import matplotlib.pyplot as plt

WheelCircumference = 2.0

km_per_mi = 1.60934
mi_per_km = 1 / km_per_mi

Results = {}

DriveTrains = [
	{
		# https://www.automobile-catalog.com/curve/2017/2515235/caterham_seven_420.html			
		"Name": "Duratec 420 5-speed", 
		"FinalDrive": 3.9, 
		"MaxPowerAt": 7600, 
		"Gearbox": [3.14,1.89,1.33,1.0,0.81],
		"DynoData": {
			1000: [89.70,9.40],
			1100: [102.00,11.70],
			1200: [112.20,14.10],
			1300: [120.80,16.40],
			1400: [128.20,18.80],
			1500: [134.60,21.10],
			1600: [140.20,23.50],
			1700: [145.20,25.80],
			1800: [149.60,28.20],
			1900: [153.50,30.50],
			2000: [157.10,32.90],
			2100: [160.30,35.30],
			2200: [163.20,37.60],
			2300: [165.80,39.90],
			2400: [168.30,42.30],
			2500: [170.50,44.60],
			2600: [172.60,47.00],
			2700: [174.50,49.30],
			2800: [176.30,51.70],
			2900: [177.90,54.00],
			3000: [179.50,56.40],
			3100: [180.90,58.70],
			3200: [182.30,61.10],
			3300: [183.60,63.40],
			3400: [184.80,65.80],
			3500: [185.90,68.10],
			3600: [187.00,70.50],
			3700: [188.00,72.80],
			3800: [188.90,75.20],
			3900: [189.90,77.60],
			4000: [190.70,79.90],
			4100: [191.50,82.20],
			4200: [192.30,84.60],
			4300: [193.10,87.00],
			4400: [193.80,89.30],
			4500: [194.50,91.70],
			4600: [195.10,94.00],
			4700: [195.70,96.30],
			4800: [196.30,98.70],
			4900: [196.90,101.00],
			5000: [197.40,103.40],
			5100: [198.00,105.70],
			5200: [198.50,108.10],
			5300: [199.00,110.50],
			5400: [199.40,112.80],
			5500: [199.90,115.10],
			5600: [200.30,117.50],
			5700: [200.80,119.90],
			5800: [201.20,122.20],
			5900: [201.60,124.60],
			6000: [201.90,126.90],
			6100: [202.30,129.20],
			6200: [202.70,131.60],
			6300: [203.00,133.90],
			6400: [203.00,136.10],
			6500: [202.80,138.00],
			6600: [202.70,140.10],
			6700: [202.40,142.00],
			6800: [202.10,143.90],
			6900: [201.60,145.70],
			7000: [201.20,147.50],
			7100: [200.60,149.20],
			7200: [199.90,150.70],
			7300: [199.20,152.30],
			7400: [198.40,153.80],
			7500: [197.60,155.20],
			7600: [196.60,156.50],
			7700: [193.30,155.90],
			7800: [188.50,154.00],
			7900: [182.40,150.90],
			8000: [174.80,146.40],
			8100: [166.00,140.80],	
		}
	},
	{
		"Name": "Helix SPX177 400A", 
		"FinalDrive": 3.6, 
		"MaxPowerAt": 18000, 
		"Gearbox": [3.0],
		# 4000A Max AC RMS Current
		"DynoData": {
			0:[145, 0],
			12000:[145, 150],
			18000:[73, 150],
		}
	},
	{
		"Name": "Helix SPX177 550A", 
		"FinalDrive": 3.6, 
		"MaxPowerAt": 18000, 
		"Gearbox": [2.5],
		# 550A Max AC RMS Current
		"DynoData": {
			0:[200, 0],
			12000:[200, 150],
			18000:[100, 150],
		}
	},
]

def main():
	range_low = 0
	range_end = 165
	range_step = 2

	X = np.arange(range_low, range_end, range_step)

	for dt in DriveTrains:
		torque_in_gears_vs_speed = []
		Results[dt["Name"]] = {}
		print(f"DriveTrain: {dt["Name"]}")
		
		# Calculate the gear change speeds, at max power
		mph_at_max_power = []
		for gear in dt["Gearbox"]:
			print(f"Working with Gear Ratio: {gear}")
			wheel_rpm = dt["MaxPowerAt"] / (dt["FinalDrive"] * gear)
			#print(f"Wheel RPM: {wheel_rpm:.3f}")
			meters_per_minute = wheel_rpm * WheelCircumference
			meters_per_hour = meters_per_minute * 60
			mph_at_max_power.append(meters_per_hour * km_per_mi / (1000))
			#print(f"Miles Per Hour: {mph_at_max_power[-1]:.3f}")
		pprint.pp(mph_at_max_power)

		min_rpm = 100000
		max_rpm = 0
		max_torque = 0
		max_torque_rpm = 0
		max_power = 0
		max_power_rpm = 0
		# Find max torque
		for rpm,dyno in dt["DynoData"].items():
			torque = dyno[0]
			power = dyno[1]
			if torque > max_torque:
				max_torque = torque
				max_torque_rpm = rpm
			if (power > max_power):
				max_power = power
				max_power_rpm = rpm
			if (rpm > max_rpm):
				max_rpm = rpm
			if (rpm < min_rpm):
				min_rpm = rpm
		print(f"Max Torque is: {max_torque} at {max_torque_rpm}RPM")

		# Calculate the gear change speeds to hit max torque
		mph_for_max_torque_change = []
		for index, gear in enumerate(dt["Gearbox"]):
			#print(f"Working with Gear Ratio: {gear}")
			if (index < len(dt["Gearbox"]) - 1):
				this_gear = dt["Gearbox"][index]
				next_gear = dt["Gearbox"][index+1]
				wheel_rpm = max_torque_rpm / (dt["FinalDrive"] * next_gear)
				#wheel_rpm = dt["MaxPowerAt"] / (dt["FinalDrive"] * gear)
				print(f"Wheel RPM: {wheel_rpm:.3f}, FinalDrive: {dt["FinalDrive"]}, NextGear: {next_gear}")
				meters_per_minute = wheel_rpm * WheelCircumference
				meters_per_hour = meters_per_minute * 60

				mph_for_max_torque_change.append(meters_per_hour * mi_per_km / (1000))

				# Workd out engine_rpm for current gear (just for testing)
				engine_rpm = wheel_rpm * dt["FinalDrive"] * this_gear
				print(f"Engine RPM: {engine_rpm}")
			else:
				mph_for_max_torque_change.append(None)
			
			if mph_for_max_torque_change[-1] != None:
				print(f"Miles Per Hour for [{index+1}->({gear:.2f})]: {mph_for_max_torque_change[-1]:.3f}")
			else:
				print(f"Miles Per Hour for [{index+1}->({gear:.2f})]: None")

		#pprint.pp(mph_for_max_torque_change)

		# Run across our speed range
		wheel_torques = {}
		for speed in range(range_low, range_end, range_step):
			# Get Gear at this speed
			gear = 1
			while (gear < len(mph_at_max_power) and mph_at_max_power[gear-1] < speed):
				gear += 1

			# Find RPM for this speed and gear
			rpm = 0
			gear_ratio = dt["Gearbox"][gear-1]
			diff_ratio = dt["FinalDrive"]
			meters_per_minute = speed * gear_ratio * diff_ratio * 1000.0 * km_per_mi / (60.0)
			rpm = meters_per_minute / WheelCircumference

			# Get Torque at this RPM
			torque = 0
			low_rpm = 0
			high_rpm = 100000
			low_torque = 0
			high_torque = 0
			for dyno_rpm,dyno in dt["DynoData"].items():
				dyno_torque = dyno[0]
				dyno_power = dyno[1]
				if (dyno_rpm <= rpm and dyno_rpm >= low_rpm):
					low_rpm = dyno_rpm
					low_torque = dyno_torque
				if (dyno_rpm >= rpm and dyno_rpm < high_rpm):
					high_rpm = dyno_rpm
					high_torque = dyno_torque
			
			#We should now have rpm and torque numbers either side of our rpm
			#Now do a linear estimation of the torque for the RPM we've calculated at this speed
			if (rpm == low_rpm):
				engine_torque = low_torque
			else:
				rpm_diff = rpm - low_rpm
				rpm_band = high_rpm - low_rpm
				multiplier = rpm_diff / rpm_band
				torque_band = high_torque - low_torque
				torque_delta = torque_band * multiplier
				engine_torque = low_torque + torque_delta

			wheel_torque = engine_torque * gear_ratio * diff_ratio / 2

			print(f"Speed: {speed:.2f}, Gear: {gear}, GearRatio: {gear_ratio:.2f}, RPM: {rpm:.2f}, Engine Torque: {engine_torque:.2f}, Wheel Torque: {wheel_torque:.2f} [LR:{low_rpm}, HR:{high_rpm}, LT:{low_torque}, HT:{high_torque}]")

			# Now run through each gear working out torque in that gear
			diff_ratio = dt["FinalDrive"]
			#torque_in_gears_vs_speed[speed] = []
			for gear, gear_ratio in enumerate(dt["Gearbox"]):

				meters_per_minute = speed * gear_ratio * diff_ratio * 1000.0 * km_per_mi / (60.0)
				rpm = meters_per_minute / WheelCircumference

				if (rpm > min_rpm and rpm < max_rpm):
					# Get Torque at this RPM
					torque = 0
					low_rpm = 0
					high_rpm = 100000
					low_torque = 0
					high_torque = 0
					for dyno_rpm,dyno in dt["DynoData"].items():
						dyno_torque = dyno[0]
						dyno_power = dyno[1]
						if (dyno_rpm <= rpm and dyno_rpm >= low_rpm):
							low_rpm = dyno_rpm
							low_torque = dyno_torque
						if (dyno_rpm > rpm and dyno_rpm < high_rpm):
							high_rpm = dyno_rpm
							high_torque = dyno_torque
					
					#We should now have rpm and torque numbers either side of our rpm
					#Now do a linear estimation of the torque for the RPM we've calculated at this speed
					rpm_diff = rpm - low_rpm
					rpm_band = high_rpm - low_rpm
					multiplier = rpm_diff / rpm_band
					torque_band = high_torque - low_torque
					torque_delta = torque_band * multiplier
					engine_torque = low_torque + torque_delta

					wheel_torque = engine_torque * gear_ratio * diff_ratio / 2
				else:
					wheel_torque = 0

				match gear:
					case 0: gear_str = "1st"
					case 1: gear_str = "2nd"
					case 2: gear_str = "3rd"
					case 3: gear_str = "4th"
					case 4: gear_str = "5th"
					case 5: gear_str = "6th"
					case _: gear_str = "Unknown"

				# If we don't have a dict item for this gear yet, then create it
				gear_str = f"{str(gear_ratio)}"
				if gear_str not in Results[dt["Name"]]:
					Results[dt["Name"]][gear_str] = []

				Results[dt["Name"]][gear_str].append(int(wheel_torque))

	plt.figure(figsize=(12,6)) # Plot size in inches!
	for dt_name in Results:
		for key in Results[dt_name]:
			y1 = np.array(Results[dt_name][key],dtype=np.double)
			y1[ y1==0 ] = np.nan
			FinalDrive = "??"
			for dt in DriveTrains:
				if (dt["Name"] == dt_name):
					FinalDrive = dt["FinalDrive"]
			plt.plot(X, y1, label = f"{dt_name}->({FinalDrive}*{key}):1")

	values = np.arange(0, 1500, 100)
	value_increment = 1
	plt.legend()
	plt.axis((0, 160, 0, 1500))
	plt.grid(color = 'grey', linestyle = (0, (5, 10)), linewidth = 0.25)
	plt.yticks(values * value_increment, ['%d' % val for val in values])
	plt.xlabel('Speed (mph)')
	plt.ylabel('Torque (Nm)')
	plt.tight_layout(rect=[0, 0.02, 1, 0.98])
	plt.title('In-gear Torque at Wheel (E-Motor torque limited by current)')
	# Displaying the plot
	plt.show()

if __name__ == "__main__":
	main()