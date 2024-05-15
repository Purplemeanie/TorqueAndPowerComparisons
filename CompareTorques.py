# Compare Torques
import pprint

WheelCircumference = 2.0


DriveTrains = [
	{
		"Name": "Duratec + Mazda", 
		"FinalDrive": 3.6, 
		"MaxPowerAt": 7250, 
		"Gearbox": [3.5,1.89,1.02,0.89],
		"TorqueCurve": {
			0:0,
			1000:10,
			2000:20,
			3000:30,
			4000:40,
			5000:50,
			6000:60,
			7000:70
		}
	},
	{
		"Name": "Helix SPX177", 
		"FinalDrive": 3.6, 
		"MaxPowerAt": 12000, 
		"Gearbox": [1.89],
		"TorqueCurve": {
			0:200,
			12000:200,
		}
	},
]

def main():
	for dt in DriveTrains:
		print(f"DriveTrain: {dt["Name"]}")
		
		# Calculate the gear change speeds, at max power
		miles_per_hour = []
		for gear in dt["Gearbox"]:
			print(f"Working with Gear Ratio: {gear}")
			wheel_rpm = dt["MaxPowerAt"] / (dt["FinalDrive"] * gear)
			print(f"Wheel RPM: {wheel_rpm:.3f}")
			meters_per_minute = wheel_rpm * WheelCircumference
			meters_per_hour = meters_per_minute * 60
			miles_per_hour.append(meters_per_hour * 5 / (8 * 1000))
			print(f"Miles Per Hour: {miles_per_hour[-1]:.3f}")
		pprint.pp(miles_per_hour)

		# Run across our speed range
		for speed in range(0,160,10):
			# Get RPM at this speed
			gear = 1
			while (gear - 1 < len(miles_per_hour) and miles_per_hour[gear-1] < speed):
				gear += 1
			rpm = 0

			# Get Torque at this RPM
			torque = 0

			print(f"Speed: {speed}, Gear: {gear}, RPM: {rpm}, Torque: {torque}")

if __name__ == "__main__":
	main()