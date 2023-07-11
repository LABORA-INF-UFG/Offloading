import os
import argparse

def simulate (resultsLoc, sumoTools, topFileName, cars, buses, pedestrians, nOfCars, nOfBuses, nOfPedestrians, simDur, simStep, seed):

	flowsFileCars = "{}/flowsFileCars.xml".format(resultsLoc)
	flowsFileBuses = "{}/flowsFileBuses.xml".format(resultsLoc)
	flowsFilePedestrians = "{}/flowsFilePedestrians.xml".format(resultsLoc)
	rerouterFile = "{}/rerouterFile.xml".format(resultsLoc)

	if (cars and buses and pedestrians):

		traceFile = "{}/traceFileAll.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileAll.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {},{},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileCars, flowsFileBuses, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {},{},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileCars, flowsFileBuses, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (cars and buses and not pedestrians):

		traceFile = "{}/traceFileCarsAndBuses.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileCarsAndBuses.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileCars, flowsFileBuses, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileCars, flowsFileBuses, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (cars and not buses and pedestrians):

		traceFile = "{}/traceFileCarsAndPedestrians.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileCarsAndPedestrians.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileCars, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileCars, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (not cars and buses and pedestrians):

		traceFile = "{}/traceFileBusesAndPedestrians.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileBusesAndPedestrians.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileBuses, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {},{} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileBuses, flowsFilePedestrians, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (cars and not buses and not pedestrians):

		traceFile = "{}/traceFileCars.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileCars.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileCars, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileCars, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (not cars and buses and not pedestrians):

		traceFile = "{}/traceFileBuses.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFileBuses.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFileBuses, rerouterFile, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {} --additional-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFileBuses, rerouterFile, simStep, simDur, traceFile, cfgFileName))

	elif (not cars and not buses and pedestrians):

		traceFile = "{}/traceFilePedestrians.xml".format(resultsLoc)
		cfgFileName = "{}/cfgFilePedestrians.sumocfg".format(resultsLoc)

		if (seed == 'random'):
			os.system ("sumo --random=true --net-file {} --route-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (topFileName, flowsFilePedestrians, simStep, simDur, traceFile, cfgFileName))

		else:
			os.system ("sumo --seed={} --net-file {} --route-files {} --step-length {} --begin 0 --end {} --fcd-output {} --save-configuration {} --no-warnings"
					.format (seed, topFileName, flowsFilePedestrians, simStep, simDur, traceFile, cfgFileName))

	#Finally, we run the simultation
	if (seed == 'random'):
		os.system ("sumo --random=true -c {}".format(cfgFileName))

	else:
		os.system ("sumo --seed={} -c {}".format(seed, cfgFileName))

	#Convert the XML result to CSV
	os.system ("python {}/xml/xml2csv.py {}".format(sumoTools, traceFile))

def genFlows (resultsLoc, sumoTools, topFileName, cars, buses, pedestrians, nOfCars, nOfBuses, nOfPedestrians, simDur, seed):

	#If we have cars or buses, we need to generate continuous re-routers using the "generateContinuousRerouters.py," available in SUMO.
	if (cars or buses):

		rerouterFile = "{}/rerouterFile.xml".format(resultsLoc)
		os.system ("python {}/generateContinuousRerouters.py -n {} -o {}".format(sumoTools, topFileName, rerouterFile))

	if (cars):

		flowsFileCars = "{}/flowsFileCars.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("python {}/randomTrips.py -n {} -o {} --vehicle-class passenger --begin 0 --end 1 --flows {} --jtrrouter --trip-attributes \"departPos='random' departSpeed='max'\" --intermediate=10"
					.format(sumoTools, topFileName, flowsFileCars, nOfCars))

		else:
			os.system ("python {}/randomTrips.py -n {} -o {} --seed={} --vehicle-class passenger --begin 0 --end 1 --flows {} --jtrrouter --trip-attributes \"departPos='random' departSpeed='max'\" --intermediate=10"
					.format(sumoTools, topFileName, flowsFileCars, seed, nOfCars))

	if (buses):

		flowsFileBuses = "{}/flowsFileBuses.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("python {}/randomTrips.py -n {} -o {} --vehicle-class bus --begin 0 --end 1 --flows {} --jtrrouter --trip-attributes \"departPos='random' departSpeed='max'\" --intermediate=10"
					.format(sumoTools, topFileName, flowsFileBuses, nOfBuses))

		else:
			os.system ("python {}/randomTrips.py -n {} -o {} --seed={} --vehicle-class bus --begin 0 --end 1 --flows {} --jtrrouter --trip-attributes \"departPos='random' departSpeed='max'\" --intermediate=10"
					.format(sumoTools, topFileName, flowsFileBuses, seed, nOfBuses))

	if (pedestrians):

		flowsFilePedestrians = "{}/flowsFilePedestrians.xml".format(resultsLoc)
		#https://sumo.dlr.de/docs/Tools/Trip.html#traffic_volume_arrival_rate
		pedestriansRate = float(1 / nOfPedestrians)

		if (seed == 'random'):
			os.system ("python {}/randomTrips.py --pedestrians --persontrips -n {} --begin 0 --end 1 -p {} -o {} --intermediate=10"
					.format(sumoTools, topFileName, pedestriansRate, flowsFilePedestrians))

		else:
			os.system ("python {}/randomTrips.py --pedestrians --persontrips -n {} --begin 0 --end 1 -p {} -o {} --seed={} --intermediate=10"
					.format(sumoTools, topFileName, pedestriansRate, flowsFilePedestrians, seed))

	#If we will simulate cars and buses, we need to renames buses IDs in order to avoid conflicts
	if (cars and buses):

		with open(flowsFileBuses) as f:
			newID = f.read().replace('" begin', 'B" begin')

		with open(flowsFileBuses, "w") as f:
			f.write(newID)

def genNet (resultsLoc, cars, buses, pedestrians, nOfGrids, gridLength, seed):

	#Check whether the results path exists or not
	resultsExist = os.path.exists(resultsLoc)
	if not resultsExist:
		os.makedirs(resultsLoc)

	#Check mobility types called, define the output topology and create the manhattan topology
	#Network file for Manhattan created using the "netgenerate" SUMO command
	if (cars and buses and pedestrians):
		
		topologyFile = "{}/topFileAll.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (cars and buses and not pedestrians):
		
		topologyFile = "{}/topFileCarsAndBuses.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (cars and not buses and pedestrians):

		topologyFile = "{}/topFileCarsAndPedestrians.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (not cars and buses and pedestrians):

		topologyFile = "{}/topFileBusesAndPedestrians.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (cars and not buses and not pedestrians):

		topologyFile = "{}/topFileCars.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (not cars and buses and not pedestrians):

		topologyFile = "{}/topFileBuses.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	elif (not cars and not buses and pedestrians):

		topologyFile = "{}/topFilePedestrians.xml".format(resultsLoc)

		if (seed == 'random'):
			os.system ("netgenerate --random=true --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(nOfGrids, gridLength, topologyFile))

		else:
			os.system ("netgenerate --seed={} --grid --grid.number {} --grid.length {} --no-turnarounds --sidewalks.guess -o {}"
					.format(seed, nOfGrids, gridLength, topologyFile))

	return topologyFile

def emulateCars (sumoHome, sumoTools, resultsLoc, nOfGrids, gridLength, simDur, simStep, nOfCars, seed):

	topFileName = genNet (resultsLoc, True, False, False, nOfGrids, gridLength, seed)
	genFlows (resultsLoc, sumoTools, topFileName, True, False, False, nOfCars, 0, 0, simDur, seed)
	simulate (resultsLoc, sumoTools, topFileName, True, False, False, nOfCars, 0, 0, simDur, simStep, seed)

def emulateBuses (sumoHome, sumoTools, resultsLoc, nOfGrids, gridLength, simDur, simStep, nOfBuses, seed):

	topFileName = genNet (resultsLoc, False, True, False, nOfGrids, gridLength, seed)
	genFlows (resultsLoc, sumoTools, topFileName, False, True, False, 0, nOfBuses, 0, simDur, seed)
	simulate (resultsLoc, sumoTools, topFileName, False, True, False, 0, nOfBuses, 0, simDur, simStep, seed)

def emulatePedestrians (sumoHome, sumoTools, resultsLoc, nOfGrids, gridLength, simDur, simStep, nOfPedestrians, seed):

	topFileName = genNet (resultsLoc, False, False, True, nOfGrids, gridLength, seed)
	genFlows (resultsLoc, sumoTools, topFileName, False, False, True, 0, 0, nOfPedestrians, simDur, seed)
	simulate (resultsLoc, sumoTools, topFileName, False, False, True, 0, 0, nOfPedestrians, simDur, simStep, seed)

def emulateTwo (mobOne, mobTwo, sumoHome, sumoTools, resultsLoc, nOfGrids, gridLength, simDur, simStep, nOfMobOne, nOfMobTwo, seed):

	if (mobOne == 'car' and mobTwo == 'bus'):

		topFileName = genNet (resultsLoc, True, True, False, nOfGrids, gridLength, seed)

		nOfCars = nOfMobOne
		nOfBuses = nOfMobTwo
		genFlows (resultsLoc, sumoTools, topFileName, True, True, False, nOfCars, nOfBuses, 0, simDur, seed)
		simulate (resultsLoc, sumoTools, topFileName, True, True, False, nOfCars, nOfBuses, 0, simDur, simStep, seed)

	elif (mobOne == 'car' and mobTwo == 'pedestrian'):

		topFileName = genNet (resultsLoc, True, False, True, nOfGrids, gridLength, seed)

		nOfCars = nOfMobOne
		nOfPedestrians = nOfMobTwo
		genFlows (resultsLoc, sumoTools, topFileName, True, False, True, nOfCars, 0, nOfPedestrians, simDur, seed)
		simulate (resultsLoc, sumoTools, topFileName, True, False, True, nOfCars, 0, nOfPedestrians, simDur, simStep, seed)

	elif (mobOne == 'bus' and mobTwo == 'pedestrian'):

		topFileName = genNet (resultsLoc, False, True, True, nOfGrids, gridLength, seed)

		nOfBuses = nOfMobOne
		nOfPedestrians = nOfMobTwo
		genFlows (resultsLoc, sumoTools, topFileName, False, True, True, 0, nOfBuses, nOfPedestrians, simDur, seed)
		simulate (resultsLoc, sumoTools, topFileName, False, True, True, 0, nOfBuses, nOfPedestrians, simDur, simStep, seed)

def emulateAll (sumoHome, sumoTools, resultsLoc, nOfGrids, gridLength, simDur, simStep, nOfCars, nOfBuses, nOfPedestrians, seed):

	topFileName = genNet (resultsLoc, True, True, True, nOfGrids, gridLength, seed)
	genFlows (resultsLoc, sumoTools, topFileName, True, True, True, nOfCars, nOfBuses, nOfPedestrians, simDur, seed)
	simulate (resultsLoc, sumoTools, topFileName, True, True, True, nOfCars, nOfBuses, nOfPedestrians, simDur, simStep, seed)

def main ():

	parser = argparse.ArgumentParser()

	#Mobility types
	parser.add_argument("-c", "--cars", help="A flag that indicates that you want to simulate cars.", action='store_true')
	parser.add_argument("-b", "--buses", help="A flag that indicates that you want to simulate buses.", action='store_true')
	parser.add_argument("-p", "--pedestrians", help="A flag that indicates that you want to simulate pedestrians.", action='store_true')

	#Paths scripts
	parser.add_argument("-sh", "--sumoHome", help="SUMO home location.")
	parser.add_argument("-st", "--sumoTools", help="SUMO tools location.")
	parser.add_argument("-rl", "--resultsLoc", help="Directory where the results are going to be saved.")

	#Variables
	#Grid
	parser.add_argument("-ng", "--nOfGrids", help="Number of junctions in both dirs.")
	parser.add_argument("-gl", "--gridLength", help="The length of streets in both dirs.")
	#Duration
	parser.add_argument("-sd", "--simDur", help="Simulation duration in seconds.")
	parser.add_argument("-step", "--simStep", help="Simulation step (granularity) in seconds.")
	#Number of users
	parser.add_argument("-nc", "--nOfCars", help="Number of cars.")
	parser.add_argument("-nb", "--nOfBuses", help="Number of buses.")
	parser.add_argument("-np", "--nOfPedestrians", help="Number of pedestrians.")

	#Seed options
	parser.add_argument("-s", "--seed", help="Seed for the simulation.")

	args = parser.parse_args()

	checkSUMOInstallation = os.system ("sumo >/dev/null 2>&1")

	if (checkSUMOInstallation == 32512):
		print ("Please install SUMO before running this script")

	else:

		#Converting types
		args.nOfGrids = int(args.nOfGrids)
		args.gridLength = float(args.gridLength)
		args.simDur = float(args.simDur)
		args.simStep = float (args.simStep)
		#Defining seed
		if (args.seed != None):
			seed = int (args.seed)
		else:
			seed = 'random'

		#Emulate only cars
		if (args.cars and not args.buses and not args.pedestrians):

			args.nOfCars = int (args.nOfCars)

			emulateCars (args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength, args.simDur,
						args.simStep, args.nOfCars, seed)

		#Emulate only buses
		elif (args.buses and not args.cars and not args.pedestrians):

			args.nOfBuses = int (args.nOfBuses)

			emulateBuses (args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength, args.simDur,
						args.simStep, args.nOfBuses, seed)

		#Emulate only pedestrians
		elif (args.pedestrians and not args.cars and not args.buses):

			args.nOfPedestrians = int (args.nOfPedestrians)

			emulatePedestrians (args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength, args.simDur,
						args.simStep, args.nOfPedestrians, seed)

		#Emulate cars and buses
		elif (args.cars and args.buses and not args.pedestrians):

			args.nOfCars = int (args.nOfCars)
			args.nOfBuses = int (args.nOfBuses)

			emulateTwo ('car', 'bus', args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength,
						args.simDur, args.simStep, args.nOfCars, args.nOfBuses, seed)

		#Emulate cars and pedestrians
		elif (args.cars and args.pedestrians and not args.buses):

			args.nOfCars = int (args.nOfCars)
			args.nOfPedestrians = int (args.nOfPedestrians)

			emulateTwo ('car', 'pedestrian', args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength,
						args.simDur, args.simStep, args.nOfCars, args.nOfPedestrians, seed)

		#Emulate buses and pedestrians
		elif (args.buses and args.pedestrians and not args.cars):

			args.nOfBuses = int (args.nOfBuses)
			args.nOfPedestrians = int (args.nOfPedestrians)

			emulateTwo ('bus', 'pedestrian', args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength,
						args.simDur, args.simStep, args.nOfBuses, args.nOfPedestrians, seed)

		#Emulate cars, buses and pedestrians
		elif (args.cars and args.buses and args.pedestrians):

			args.nOfCars = int (args.nOfCars)
			args.nOfBuses = int (args.nOfBuses)
			args.nOfPedestrians = int (args.nOfPedestrians)

			emulateAll (args.sumoHome, args.sumoTools, args.resultsLoc, args.nOfGrids, args.gridLength, args.simDur,
						args.simStep, args.nOfCars, args.nOfBuses, args.nOfPedestrians, seed)

		else:
			print ("No mobility chosen.")

if __name__ == '__main__':
	main()