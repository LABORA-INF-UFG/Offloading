import os
import math
import argparse
import pandas as pd

#Calculate the latency between each BS and each MH
#Calculate the closest MH to each BS
def calculateBSsMHsDelay (BSxyDF, MECxyDF, distMS):

	dictDelayBSsMHs = {}
	dictClosestMHtoBS = {}
	for bsIndex in range (len(BSxyDF)):

		bsID = BSxyDF['Node ID'].iloc[bsIndex]

		closestMHdist = 999999999
		closestMHid = -1

		for mecIndex in range (len(MECxyDF)):

			mecID = MECxyDF['Node ID'].iloc[mecIndex]

			distance = math.sqrt(((float(BSxyDF['X'].iloc[bsIndex]) - float(MECxyDF['X'].iloc[mecIndex]))**2) + ((float(BSxyDF['Y'].iloc[bsIndex]) - float(MECxyDF['Y'].iloc[mecIndex]))**2))
			
			if (distance < closestMHdist):
				closestMHid = mecID
				closestMHdist = distance

			dictDelayBSsMHs["delayBS{}toMH{}".format(bsID, mecID)] = (distMS * distance) / 1000.0

		dictClosestMHtoBS["closestMHtoBS{}".format(bsID)] = closestMHid

	return dictDelayBSsMHs, dictClosestMHtoBS

#Offloading simulator itself
def offloadingSimulator (df, appsProfsDF, dictDelayBSsMHs, dictClosestMHtoBS, epsilons):

	#Users were able or not to Offload
	offloadingSimulationResults = []

	for epsIndex in range (len(epsilons)):

		epsDF = df.loc[df['Epsilon'] == float(epsilons[epsIndex])]

		listUniqueTimestamps = list(epsDF['Timestamp'].unique())

		for timestampIndex in range (len(listUniqueTimestamps)):

			timestamp = listUniqueTimestamps[timestampIndex]
			
			print ("Running offloading simulation for epsilon {} timestamp {}".format(epsilons[epsIndex], timestamp))

			mhULbwd = [10410] * 95

			timestampDF = epsDF[epsDF.Timestamp == listUniqueTimestamps[timestampIndex]]

			userIDs = list(timestampDF['UserID'])
			mobilities = list(timestampDF['Mobility'])
			applications = list(timestampDF['Application'])
			closestBSs = list(timestampDF['ClosestBS'])
			privateClosestBSs = list(timestampDF['PrivateBS'])
			bandwidths = list(timestampDF['Bandwidth'])

			for userIndex in range (len(userIDs)):

				#User
				userID = userIDs[userIndex]
				userBS = closestBSs[userIndex]
				userPrivBS = privateClosestBSs[userIndex]
				userMob = mobilities[userIndex]
				userApp = applications[userIndex]
				userBwd = bandwidths[userIndex]

				#MH
				userMH = dictClosestMHtoBS["closestMHtoBS{}".format(userBS)]
				userLat = dictDelayBSsMHs["delayBS{}toMH{}".format(userBS, userMH)]
				userPrivMH = dictClosestMHtoBS["closestMHtoBS{}".format(userPrivBS)]
				userPrivLat = dictDelayBSsMHs["delayBS{}toMH{}".format(userBS, userPrivMH)]

				#App
				if (userApp == "Video"):
					appBwd = float(appsProfsDF.loc[appsProfsDF['Application'] == "Video", 'Bandwidth'].iloc[0])
					appLat = float(appsProfsDF.loc[appsProfsDF['Application'] == "Video", 'Latency'].iloc[0])
				elif (userApp == "AR"):
					appBwd = float(appsProfsDF.loc[appsProfsDF['Application'] == "AR", 'Bandwidth'].iloc[0])
					appLat = float(appsProfsDF.loc[appsProfsDF['Application'] == "AR", 'Latency'].iloc[0])
				elif (userApp == "VR"):
					appBwd = float(appsProfsDF.loc[appsProfsDF['Application'] == "VR", 'Bandwidth'].iloc[0])
					appLat = float(appsProfsDF.loc[appsProfsDF['Application'] == "VR", 'Latency'].iloc[0])

				###Offload###
				#unato -> User Not Able to Offload
				unatoLackUEbwd = 0
				unatoLat = 0
				unatoLackMHbwd = 0
				#uato -> User Able to Offload
				uato = 0
				#Test user bandwidth
				if (userBwd >= appBwd):

					#Test user latency
					if (userPrivLat <= appLat):
						
						#Test if there are enough UL resources in the selected MH
						if (mhULbwd[userPrivMH] >= appBwd):
							#User if able to Offload
							#Reduce the UL bandwidth on the MH
							mhULbwd[userPrivMH] -= appBwd
							uato = 1

						#Not enough UL resources in the selected MH
						else:
							unatoLackMHbwd = 1

					#Latency between the BS the user is connect and selected MH too high
					else:
						unatoLat = 1

						#Not enough UL resources in the selected MH
						if (mhULbwd[userPrivMH] < appBwd):
							unatoLackMHbwd = 1

				#Lack of bandwidth in the user's equipment
				else:
					unatoLackUEbwd = 1

					#Test user latency
					if (userPrivLat > appLat):
						unatoLat = 1

					#Not enough UL resources in the selected MH
					if (mhULbwd[userPrivMH] < appBwd):
						unatoLackMHbwd = 1

				offloadingSimulationResults.append ([str(epsilons[epsIndex]).upper(), timestamp, uato, unatoLackUEbwd, unatoLat, unatoLackMHbwd, userID, userBS, userPrivBS, userMH, userPrivMH, userLat, userPrivLat, appLat, userBwd, appBwd, userApp, userMob])

	resultsDF = pd.DataFrame(offloadingSimulationResults, columns=[	'epsilon', 'timestamp', 'uato', 'unatoLackUEbwd',
																	'unatoLat', 'unatoLackMHbwd', 'userID', 'userBS',
																	'userPrivBS', 'userMH', 'userPrivMH', 'userLat',
																	'userPrivLat', 'appLat', 'userBwd', 'appBwd',
																	'userApp', 'userMob'])

	return resultsDF

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-drl", "--dataset", help="Data set file location.")
	parser.add_argument("-rl", "--resultsLoc", help="Directory where the offloading simulation results will be saved.")
	parser.add_argument("-bs", "--BSxy", help="Base stations positions file location.")
	parser.add_argument("-mh", "--MECxy", help="MEC Hosts positions file location.")
	parser.add_argument("-appP", "--appProf", help="Profiles for each application.")
	parser.add_argument("-dms", "--distMS", help="Latency estimation per kilometer in milliseconds.")
	args = parser.parse_args()

	resultsLoc = str(args.resultsLoc)

	if not (os.path.exists(resultsLoc)):
		os.makedirs(resultsLoc)

	BSxyDF = pd.read_csv (str(args.BSxy), sep=';')
	MECxyDF = pd.read_csv (str(args.MECxy), sep=';')
	appsProfsDF = pd.read_csv (str(args.appProf))

	dictDelayBSsMHs, dictClosestMHtoBS = calculateBSsMHsDelay (BSxyDF, MECxyDF, float(args.distMS))

	datasetDF = pd.read_csv ("{}".format(str(args.dataset)))

	uniEps = list(datasetDF['Epsilon'].unique())
	epsilons = []
	for epsIndex in range (len(uniEps)):
		epsilons.append (str(uniEps[epsIndex]).upper())

	offloadingSimulationResults = offloadingSimulator (datasetDF, appsProfsDF, dictDelayBSsMHs, dictClosestMHtoBS, epsilons)

	offloadingSimulationResults.to_csv("{}/offloadingSimuResults.csv".format(resultsLoc), index=False)

if __name__ == '__main__':
	main()