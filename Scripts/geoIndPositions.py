import os
import qif
import argparse
import pandas as pd

#Function just to check if is NaN
def isNaN(num):
	return num == num

#Function to process the data created by SUMO and apply the planar Laplace mechanism in qif
def processDF (sumoDF, xArea, yArea, epsilon, nbp):

	data = []

	listUniqueTimeSteps = sumoDF['timestep_time'].unique()
	for timestepIDsIndex in range (len(listUniqueTimeSteps)):

		print ("Applying Geo-indistinguishability with epsilon {} for positions on timestamp {}".format(epsilon, timestepIDsIndex))

		timestepIDdf = sumoDF[sumoDF.timestep_time == listUniqueTimeSteps[timestepIDsIndex]]

		for line in range (len (timestepIDdf)):

			if (isNaN(timestepIDdf['vehicle_id'].iloc[line])):

				X = timestepIDdf['vehicle_x'].iloc[line]
				Y = timestepIDdf['vehicle_y'].iloc[line]

				if (timestepIDdf['vehicle_type'].iloc[line] == 'passenger'):
					userID = str('Car') + str(int(float(timestepIDdf['vehicle_id'].iloc[line])))
					mobility = 'Car'

				else:
					userID = str('B') + str(timestepIDdf['vehicle_id'].iloc[line].split('B')[0])
					mobility = 'Bus'
				
			else:

				X = timestepIDdf['person_x'].iloc[line]
				Y = timestepIDdf['person_y'].iloc[line]

				userID = str('Ped') + str(int(float(timestepIDdf['person_id'].iloc[line])))
				mobility = 'Pedestrian'

			#Convert user's position if he is outside the area
			if (X > xArea):
				X = xArea
			if (Y > yArea):
				Y = yArea
			if (X < 0.0):
				X = 0.0
			if (Y < 0.0):
				Y = 0.0

			#Apply the planar Laplace mechanism in qif
			if (epsilon != "INF"):

				epsilon = float(epsilon)

				noise = list(str(qif.mechanism.geo_ind.planar_laplace_sample(epsilon)).replace("(", "").replace(")", "").split(", "))

				X += float(noise[0])
				Y += float(noise[1])

				#Convert user's position if he is outside the area
				if (X > xArea):
					X = xArea
				if (Y > yArea):
					Y = yArea
				if (X < 0.0):
					X = 0.0
				if (Y < 0.0):
					Y = 0.0

			timestamp = timestepIDdf['timestep_time'].iloc[line]

			if (mobility != 'Bus'):
				data.append([timestamp, userID, X, Y, mobility])

			else:
				for busIndex in range (nbp):
					buserID = userID + str('P') + str(busIndex + 1)
					data.append([timestamp, buserID, X, Y, mobility])

	outDF = pd.DataFrame(data, columns=['Timestamp', 'UserID', 'X', 'Y', 'Mobility'])

	return outDF

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-mrl", "--sumoDataSet", help="Directory where the mobility traces results were saved.")
	parser.add_argument("-rl", "--resultsLoc", help="Directory where the geo-indistinguishability results are going to be saved.")
	parser.add_argument("-x", "--xaxis", help="Area size horizontally in meters.")
	parser.add_argument("-y", "--yaxis", help="Area size vertically in meters.")
	parser.add_argument("-e", "--epsilon", help="Epsilon value.")
	parser.add_argument("-nbp", "--nOfBusPassengers", help="Number of passengers on each bus.")
	args = parser.parse_args()

	resultsLoc = str(args.resultsLoc)

	if not (os.path.exists(resultsLoc)):
		os.makedirs(resultsLoc)

	if (args.epsilon == None):
		epsilon = "INF"

	else:
		epsilon = float(args.epsilon)

	trace = "{}/traceFileAll.csv".format(args.sumoDataSet)
	
	sumoDF = pd.read_csv (trace, sep=';')
	outDF = processDF (sumoDF, float(args.xaxis), float(args.yaxis), str(epsilon), int(args.nOfBusPassengers))

	outDF.to_csv("{}/geoIndData{}.csv".format(resultsLoc, (str(epsilon)).upper()), index=False)

if __name__ == '__main__':
	main()