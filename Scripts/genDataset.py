import os
import math
import random
import argparse
import pandas as pd

#Calculate bandwidth capacity for each user request
def calculateBWD (outDF):

	df = outDF.loc[outDF['Epsilon'] == 'INF']

	bwCapacitiesList = []

	fc = 1800
	#BS height -- value from Luiz's WD paper
	hb = 10
	#UE height -- value from Luiz's WD paper
	hm = 1.5

	listTimestamps = df['Timestamp'].unique()
	for timestampIndex in range (len(listTimestamps)):

		print ("Estimating bandwidth with Shannon's Capacity Formula for timestamp {}".format(listTimestamps[timestampIndex]))

		timestampDF = df[df.Timestamp == listTimestamps[timestampIndex]]
		listBSs = timestampDF['ClosestBS'].unique()

		bsKeys = []
		bwCapacitiesDict = {}
		bwCapacitiesPos = {}

		for bsIndex in range (len(listBSs)):

			bsC = []
			bsDF = timestampDF[timestampDF.ClosestBS == listBSs[bsIndex]]
			bsKey = bsDF.iloc[0]['ClosestBS']
			bsKeys.append (bsKey)
			
			for index in range (len (bsDF)):

				dist = float(bsDF.iloc[index]['ClosestBSdistance'])

				#Converting distance to KM
				d = dist / 1000.0

				#38 dBm = 6.31 W, 45 dBm = 31.62 W
				Pt = 31.62
				Pr = Pt

				#UE and BS at same place, only differing from height
				if (dist < (hb-hm)):
					PL = 0.0

				#Free-space pathloss
				elif (dist < 20):
					PL = 32.4 + (20.0 * (math.log10(d))) + (20.0 * (math.log10(fc)))

				#COST 231 model
				elif (dist < 5000):
					PL = 42.6 + (26.0 * (math.log10(d))) + (20.0 * (math.log10(fc)))

				else:
					Pr = 0.0

				if (Pr > 0.0):
					#Value in nanowatts
					Pr = pow(10, 9) * pow(10, (math.log10(Pt) - (PL / 10.0)))
					#Converting Pr to watts
					Pr = Pr / 1000000000.0

				### Shannon Capacity Formula ###
				### Data and Computer Communications - William Stallings - 10 Ed - Chapter 3.4 ###
				
				#B in Hz
				B = 25000000.0

				#Noise floor in nanowatts
				N = pow(10, 9) * 1.38 * B * pow(10, 6) * pow(10, -23) 	
				#Converting N to watts
				N = N / 1000000000.0

				#Signal-to-Noise Ratio
				SNR = 10 * math.log10 (Pr / N)

				#C in bps
				C = B * math.log2((1 + SNR))
				#Convert to Mbps
				C = C / 1000000.0

				bsC.append(C)
			
			if (sum(bsC) > 10000):

				proportionalFairnessCapacity = []

				for cIndex in range (len(bsC)):
					proportionalFairnessCapacity.append(float(bsC[cIndex] * 10000) / float(sum(bsC)))

				bwCapacitiesDict[bsKey] = proportionalFairnessCapacity

			else:
				bwCapacitiesDict[bsKey] = bsC

		closestBSs = list(timestampDF['ClosestBS'])
		for index in range (len(closestBSs)):
			bwCapacitiesPos[closestBSs[index]] = 0

		closestBSs = list(timestampDF['ClosestBS'])
		for index in range (len(closestBSs)):
			bwCapacitiesList.append (list(bwCapacitiesDict[closestBSs[index]])[bwCapacitiesPos[closestBSs[index]]])
			bwCapacitiesPos[closestBSs[index]] += 1

	bwdCap = []
	capIndex = 0
	for bwdIndex in range (len(outDF)):

		if (outDF['Epsilon'].iloc[bwdIndex] == 'INF'):
			bwdCap.append (bwCapacitiesList[capIndex])
			capIndex += 1

		else:
			bwdCap.append ('-')

	outDF['Bandwidth'] = bwdCap

	for bwdIndex in range (len(outDF)):

		print ("Estimating bandwidth for request {} of {}".format(bwdIndex + 1, len(outDF)))

		if (outDF['Bandwidth'].iloc[bwdIndex] == '-'):

			privDF = outDF.iloc[bwdIndex]
			outDF.loc[bwdIndex, 'Bandwidth'] = outDF[(outDF['Timestamp'] == privDF['Timestamp']) & (outDF['UserID'] == str(privDF['UserID']))].iloc[0]['Bandwidth']

	return outDF

#Select the users' applications given a file containing the percentage of each app per mobility
def selectApp (outDF, appPerMobDF):

	usersIDs = list(outDF['UserID'].unique())

	usersIDs.sort()

	random.seed(1)
	random.shuffle(usersIDs)

	videoUsers = []
	vrUsers = []
	arUsers = []

	carUsers = [i for i in usersIDs if 'Car' in i]
	random.Random(1).shuffle(carUsers)
	videoPercentage = int(appPerMobDF['Percentage'][0]) * 0.01
	arPercentage = int(appPerMobDF['Percentage'][1]) * 0.01
	vrPercentage = int(appPerMobDF['Percentage'][2]) * 0.01
	videoUsers.extend (carUsers[int(len(carUsers) * .00) : int(len(carUsers) * videoPercentage)])
	arUsers.extend (carUsers[int(len(carUsers) * videoPercentage) : int(len(carUsers) * (videoPercentage + arPercentage))])
	vrUsers.extend (carUsers[int(len(carUsers) * (videoPercentage + arPercentage)) : int(len(carUsers) * (videoPercentage + arPercentage + vrPercentage))])
	
	busUsers = [i for i in usersIDs if 'B' in i]
	random.Random(1).shuffle(busUsers)
	videoPercentage = int(appPerMobDF['Percentage'][3]) * 0.01
	arPercentage = int(appPerMobDF['Percentage'][4]) * 0.01
	vrPercentage = int(appPerMobDF['Percentage'][5]) * 0.01
	videoUsers.extend (busUsers[int(len(busUsers) * .00) : int(len(busUsers) * videoPercentage)])
	arUsers.extend (busUsers[int(len(busUsers) * videoPercentage) : int(len(busUsers) * (videoPercentage + arPercentage))])
	vrUsers.extend (busUsers[int(len(busUsers) * (videoPercentage + arPercentage)) : int(len(busUsers) * (videoPercentage + arPercentage + vrPercentage))])

	pedUsers = [i for i in usersIDs if 'Ped' in i]
	random.Random(1).shuffle(pedUsers)
	videoPercentage = int(appPerMobDF['Percentage'][6]) * 0.01
	arPercentage = int(appPerMobDF['Percentage'][7]) * 0.01
	videoUsers.extend (pedUsers[int(len(pedUsers) * .00) : int(len(pedUsers) * videoPercentage)])
	arUsers.extend (pedUsers[int(len(pedUsers) * videoPercentage) : int(len(pedUsers) * (videoPercentage + arPercentage))])

	chosenApp = []
	for appIndex in range (len (outDF)):

		if (outDF['UserID'].iloc[appIndex] in videoUsers):
			chosenApp.append ('Video')

		elif (outDF['UserID'].iloc[appIndex] in arUsers):
			chosenApp.append ('AR')

		elif (outDF['UserID'].iloc[appIndex] in vrUsers):
			chosenApp.append ('VR')

		else:
			break

	outDF['Application'] = chosenApp

	return outDF

#Function to extract mobility info from the SUMO data set
def extractFromSUMO (BSxyDF, MECxyDF, geoIndResults, epsilons):

	data = []

	closestBSList = []
	closestBSdistList = []

	for epsIndex in range (len(epsilons)):

		df = pd.read_csv ("{}/geoIndData{}.csv".format(geoIndResults, epsilons[epsIndex]))

		listUniqueTimeSteps = df['Timestamp'].unique()

		for timestepIDsIndex in range (len(listUniqueTimeSteps)):

			print ("Extracting from trace of epsilon {} for timestamp {}".format(epsilons[epsIndex], listUniqueTimeSteps[timestepIDsIndex]))

			timestepData = []
			timestepDF = df[df.Timestamp == listUniqueTimeSteps[timestepIDsIndex]]

			if (epsilons[epsIndex] == 'INF'):

				for line in range (len (timestepDF)):

					Xpos = timestepDF['X'].iloc[line]
					Ypos = timestepDF['Y'].iloc[line]

					userID = timestepDF['UserID'].iloc[line]
					timestamp = timestepDF['Timestamp'].iloc[line]
					mobility = timestepDF['Mobility'].iloc[line]

					for bsIndex in range(len(BSxyDF)):

						distance = math.sqrt(((float(Xpos) - float(BSxyDF['X'].iloc[bsIndex]))**2) + ((float(Ypos) - float(BSxyDF['Y'].iloc[bsIndex]))**2))

						if(bsIndex == 0):
							closestBS = bsIndex
							closestBSdist = distance
							
						else:
							if(distance < closestBSdist):
								closestBS = bsIndex
								closestBSdist = distance

					privBS = closestBS
					closestBSList.append (closestBS)
					closestBSdistList.append (closestBSdist)

					timestepData.append([epsilons[epsIndex], userID, Xpos, Ypos, timestamp, closestBSdist, closestBS, privBS, mobility])

			else:

				for line in range (len (timestepDF)):

					Xpos = timestepDF['X'].iloc[line]
					Ypos = timestepDF['Y'].iloc[line]

					userID = timestepDF['UserID'].iloc[line]
					timestamp = timestepDF['Timestamp'].iloc[line]
					mobility = timestepDF['Mobility'].iloc[line]

					for bsIndex in range(len(BSxyDF)):

						distance = math.sqrt(((float(Xpos) - float(BSxyDF['X'].iloc[bsIndex]))**2) + ((float(Ypos) - float(BSxyDF['Y'].iloc[bsIndex]))**2))

						if(bsIndex == 0):
							privBS = bsIndex
							privBSdist = distance
							
						else:
							if(distance < privBSdist):
								privBS = bsIndex
								privBSdist = distance

					closestBS = closestBSList[line]
					closestBSdist = closestBSdistList[line]

					timestepData.append([epsilons[epsIndex], userID, Xpos, Ypos, timestamp, closestBSdist, closestBS, privBS, mobility])

			random.shuffle(timestepData)

			data.extend (timestepData)

	outDF = pd.DataFrame(data, columns=['Epsilon', 'UserID', 'Xpos', 'Ypos', 'Timestamp', 'ClosestBSdistance', 'ClosestBS', 'PrivateBS', 'Mobility'])

	return outDF

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-grl", "--geoIndResults", help="Files generated by geo-indistinguishability.", nargs='+')
	parser.add_argument("-rl", "--resultsLoc", help="Directory where the data set is going to be saved.")
	parser.add_argument("-bs", "--BSxy", help="Base stations positions file location.")
	parser.add_argument("-mh", "--MECxy", help="MEC Hosts positions file location.")
	parser.add_argument("-appP", "--appPerc", help="Percentage of users that run each app per mobility.")
	args = parser.parse_args()

	resultsLoc = str(args.resultsLoc)

	if not (os.path.exists(resultsLoc)):
		os.makedirs(resultsLoc)

	BSxyDF = pd.read_csv (str(args.BSxy), sep=';')
	MECxyDF = pd.read_csv (str(args.MECxy), sep=';')
	appsPercentagesDF = pd.read_csv (str(args.appPerc))

	epsValues = list(args.geoIndResults)

	epsilons = []
	for epsIndex in range (len(epsValues)):
		eps = epsValues[epsIndex][epsValues[epsIndex].find('geoIndData'):]
		eps = eps.replace('geoIndData', '')
		eps = eps.replace('.csv', '')
		epsilons.append(eps)

	epsilons.sort(reverse=True)

	geoIndResultsLocation = list(args.geoIndResults)
	sep = 'geoIndData'
	geoIndResultsLocation = geoIndResultsLocation[0].split(sep, 1)[0]

	outDF = extractFromSUMO (BSxyDF, MECxyDF, str(geoIndResultsLocation), epsilons)
	outDF = selectApp (outDF, appsPercentagesDF)
	outDF = calculateBWD (outDF)

	outDF.to_csv("{}/offloadingDataSet.csv".format(resultsLoc), index=False)

if __name__ == '__main__':
	main()