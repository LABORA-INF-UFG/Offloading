# Environment created for the paper: "Impact of User Privacy and Mobility on Edge Offloading"

The environment was tested in Ubuntu 18.04 LTS and Ubuntu 20.04 LTS. Although it may work on some other Debian-based Linux distributions, we do not guarantee that all features will work well.

- [Getting started](#getting-started)
	- [Installing the prerequisites](#installing-the-prerequisites)
	- [Cloning the repository](#cloning-the-repository)
- [Environment](#environment)
	- [Generating mobility traces with SUMO](#generating-mobility-traces-with-sumo)
	- [Generating nodes positions](#generating-nodes-positions)
	- [Protecting users' positions](#protecting-users-positions)
	- [Generating the data set](#generating-the-data-set)
	- [Running the offloading simulation](#running-the-offloading-simulation)
- [IEEE PIMRC 2023 paper](#ieee-pimrc-2023-paper)
	- [Paper data sets](#paper-data-sets)
	- [Citation](#citation)
- [Contact us](#contact-us)

## Getting started

These instructions will guide you to get the environment up and running.

### Installing the prerequisites

```
sudo apt update
sudo apt install python python3 python3-pip git
pip3 install --upgrade pip
python3 -m pip install argparse numpy scipy qif pandas gdown
```

**It is also necessary to install [SUMO](https://eclipse.dev/sumo/):**
1. Please refer to the official SUMO documentation on [how to install it](https://sumo.dlr.de/docs/Installing/#linux), we recommend the separate PPA version.
2. Run the [SUMO Linux build](https://sumo.dlr.de/docs/Installing/Linux_Build.html).

### Cloning the repository

```
git clone https://github.com/LABORA-INF-UFG/Offloading.git
```

## Environment

Here we detail our environment. Please enter the [Scripts/](Scripts/) directory before running each script.

### Generating mobility traces with SUMO

The script we created provide a plethora of options in order to generate the mobility traces that best fit your scenarios.

You can create the mobility traces by running the following script combined with the arguments:

```
python3 genSUMOtraces.py -c -b -p -sh sumoHomeLocation -st sumoToolsLocation -rl resultsLocation -ng numberOfGrids -gl gridLength -sd simulationDururation -step simulationStep -nc numberOfCars -nb numberOfBuses -np numberOfPedestrians -s seed
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -c (flag) – A flag that indicates that you want to simulate cars.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -b (flag) – A flag that indicates that you want to simulate buses.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -p (flag) – A flag that indicates that you want to simulate pedestrians.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -sh (directory) – SUMO home location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -st (directory) – SUMO tools location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -rl (directory) – Directory where the results are going to be saved.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -ng (int) – Number of junctions in both dirs.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -gl (int) – The length of streets in both dirs.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -sd (int) – Simulation duration in seconds.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -step (int) – Simulation step (granularity) in seconds.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -nc (int) – Number of cars.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -nb (int) – Number of buses.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -np (int) – Number of pedestrians.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -s (int) – Seed for the simulation.

Here is an example:

```
python3 genSUMOtraces.py -c -b -p -sh /home/$USER/sumo -st /home/$USER/sumo/tools -rl /home/$USER/offloadingResults/mobTraces -ng 11 -gl 200 -sd 10 -step 1 -nc 40 -nb 4 -np 45 -s 1
```

Notes:

1. The SUMO home and tools locations are the same ones you used to build SUMO.
2. You can choose to generate the traces without specifying a seed. In that case, a [random seed](https://sumo.dlr.de/docs/Simulation/Randomness.html) will be chosen by SUMO. For that, simply run the same command without the "-s" argument.

### Generating nodes positions

In this work we used Homogeneous Poisson Point Process (HPPP) to generate the nodes (Base stations and MEC hosts) positions.

You can create your own nodes positions with HPPP by running the following script combined with the arguments:

```
python3 genNodesPositions.py -x areaSizeHorizontally -y areaSizeVertically -n numberOfNodes
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -x (float) – Area size horizontally in meters.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -y (float) – Area size vertically in meters.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -n (int) – Number of nodes.

Here is an example:

```
python3 genNodesPositions.py -x 2000 -y 2000 -n 475
```

A file named "nodesPositions.csv" will be generated with a position for each node.

You can find the positions we created for the paper in [Data/](Data/). The file "bsHPPP.csv" has the Base Stations (BSs) positions and file "mecHPPP.csv" the MEC Hosts (MHs) positions we used.

### Protecting users' positions

In this work we used [geo-indistinguishability](https://dl.acm.org/doi/10.1145/2508859.2516735), a state-of-the-art technique based on differential privacy, to provide location privacy for the user by producing a new (fake) position.

You can apply geo-indistinguishability to the mobility traces you generated with SUMO by running the following script combined with the arguments:

```
python3 geoIndPositions.py -mrl sumoResultsLocation -rl geoIndResultsLocation -x areaSizeHorizontally -y areaSizeVertically -e epsilonValue -nbp numberOfBusPassengers
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -mrl (directory) – Directory where the mobility traces results were saved.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -rl (directory) – Directory where the geo-indistinguishability results are going to be saved.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -x (float) – Area size horizontally in meters.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -y (float) – Area size vertically in meters.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -e (float) – Epsilon value.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -nbp (int) – Number of passengers on each bus.

Here is an example without privacy (𝜀 = ∞):

```
python3 geoIndPositions.py -mrl /home/$USER/offloadingResults/mobTraces -rl /home/$USER/offloadingResults/geoInd -x 2000 -y 2000 -nbp 10
```

Here is an example with a level of privacy (𝜀 = 0.1):

```
python3 geoIndPositions.py -mrl /home/$USER/offloadingResults/mobTraces -rl /home/$USER/offloadingResults/geoInd -x 2000 -y 2000 -e 0.1 -nbp 10
```

Notes:

1. Do not forget to use the same directory where the mobility traces results were saved.
2. You can choose to run this script without specifying a value for epsilon. In that case, no privacy will be applied, i.e., 𝜀 = ∞. For that, simply run the same command without the "-e" argument.
3. It is necessary to inform the area size because the new (fake) position has to be inside the area, and truncation will be applied if that is not the case.
4. Here you can define how many passengers you want on each bus. We used 10 passengers per bus in the paper.

A file named "geoIndData*EPSILONVALUE*.csv" will be generated with geo-indistinguishability applied for each position.

### Generating the data set

Here we detail how to generate the complete data set.

You can create the data set by running the following script combined with the arguments:

```
python3 genDataset.py -grl geoIndFile1 geoIndFile2 geoIndFileN -rl datasetLocation -bs bsNodesPositions -mh mhsNodesPositions -appP appsPercentages
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -grl (files) – Files generated by geo-indistinguishability.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -rl (directory) – Directory where the data set is going to be saved.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -bs (file) – Base stations positions file location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -mh (file) – MEC Hosts positions file location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -appP (file) – Percentage of users that run each app per mobility.

Here is an example:

```
python3 genDataset.py -grl /home/$USER/offloadingResults/geoInd/geoIndDataINF.csv /home/$USER/offloadingResults/geoInd/geoIndData0.1.csv -rl /home/$USER/offloadingResults/dataset -bs ../Data/bsHPPP.csv -mh ../Data/mecHPPP.csv -appP ../Data/appsPercentages.csv
```

Notes:

1. The "Base stations" and "MEC Hosts" positions files are the ones you generated [previously](#generating-nodes-positions).
2. The script will get the values of epsilon from the geo-indistinguishability file names. For example, if files "geoIndDataINF.csv", "geoIndData0.1.csv" and "geoIndData0.01.csv" are used as arguments, the script will run for the values [∞, 0.1 and 0.01].
3. It is **necessary** to have the "geoIndDataINF.csv" file, i.e., geo-indistinguishability applied for 𝜀 = ∞. This is because it is necessary to know the users' real position in order to estimate the User Equipment (UEs) bandwidth.
4. If you face an error like "ValueError: math domain error", there are too few BSs in the area and you need to increase the number of BSs in order to properly serve the users.
5. The file appsPercentages.csv indicates the percentage of users that are going to use an application per mobility type. You can find the file we created for the paper in [Data/](Data/), and modify it as you like.

### Running the offloading simulation

Now we detail how to run the offloading simulation.

You can run the offloading simulation by running the following script combined with the arguments:

```
python3 offloadingSimulation.py -drl datasetLocation -rl simulationResultsLocation -bs bsNodesPositions -mh mhsNodesPositions -appP appsProfiles -dms latencyConversion
```

Where:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -drl (file) – Data set file location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -rl (directory) – Directory where the offloading simulation results will be saved.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -bs (file) – Base stations positions file location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -mh (file) – MEC Hosts positions file location.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -appP (file) – Profiles for each application.\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -dms (float) – Latency estimation per kilometer in milliseconds.

Here is an example:

```
python3 offloadingSimulation.py -drl /home/$USER/offloadingResults/dataset/offloadingDataSet.csv -rl /home/$USER/offloadingResults/simuResults -bs ../Data/bsHPPP.csv -mh ../Data/mecHPPP.csv -appP ../Data/appsProfiles.csv -dms 50
```

Here is the meaning of each column in the results file:
* epsilon: User request epsilon value.
* timestamp: User request timestamp.
* uato: User request was offloaded.
* unatoLackUEbwd: User request was not offloaded because the throughput between the UE and the BS it is associated with is not enough to meet the application throughput requirement.
* unatoLat: User request was not offloaded because the latency between
the BS the UE is associated with and the selected MH by the system is too high to meet the application latency requirement.
* unatoLackMHbwd: User request was not offloaded because there are not enough network resources (bandwidth) on the selected MH.
* userID: An identifier for the user.
* userBS: The BS the user is connected.
* userPrivBS: The BS the user WOULD be connected if he was in the private position.
* userMH: The selected MH (closest to userBS) in a no-privacy scenario, i.e., using userBS as reference.
* userPrivMH: The selected MH (closest to userPrivBS) if the user was connected to userPrivBS.
* userLat: The latency between userBS (BS the user is really connected) and userMH (MH of choice if the user position is not disturbed).
* userPrivLat: The latency between userBS (BS the user is really connected) and userPrivMH (MH of choice if the user was connected to userPrivBS).
* appLat: Application latency requirement.
* userBwd: The throughput capacity between the UE and the BS it is connected to (userBS).
* appBwd: Application throughput requirement.
* userApp: Application the user intends to use.
* userMob: User’s mobility.

Notes:

1. The data set is the one you generated [previously](#generating-the-data-set).
2. The "Base stations" and "MEC Hosts" positions files are the ones you generated [previously](#generating-nodes-positions).
3. The file appsProfiles.csv indicates the profiles for each application. You can find the file we created for the paper in [Data/](Data/), and modify it as you like.
4. A user request can be denied by multiple factors, e.g., both "unatoLackUEbwd" and "unatoLat" equal to 1 means that neither throughput nor latency requirements were met.

## IEEE PIMRC 2023 paper

For more information, read the [IEEE PIMRC 2023 paper](https://arxiv.org/abs/2306.15740).

### Paper data sets

The data sets we generated for the IEEE PIMRC 2023 paper are publicly available.

You can download the data sets by running the following script:

```
python3 datasetDownloader.py
```

The data we simulated (which includes ∼405 million user requests on different privacy and mobility scenarios) contains 30 different files, as detailed on the paper.

The script will download a ZIP file with the 30 files compressed, the size of the ZIP file is 11.7 GB. When unzipped, each file has 1.3 GB, and the complete data set 38.1 GB.

Feel free to use the data sets and the environment! Please do not forget to cite our paper! :)

### Citation

```
@misc{esper2023impact,
      title={Impact of User Privacy and Mobility on Edge Offloading}, 
      author={João Paulo Esper and Nadjib Achir and Kleber Vieira Cardoso and Jussara M. Almeida},
      year={2023},
      eprint={2306.15740},
      archivePrefix={arXiv},
      primaryClass={cs.NI}
}
```

## Contact us

If you would like to contact us to contribute to this project, ask questions or suggest improvements, feel free to e-mail us at: joaopauloesper@dcc.ufmg.br