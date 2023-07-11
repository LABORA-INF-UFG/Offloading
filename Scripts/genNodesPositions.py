import argparse
import numpy as np
import scipy.stats
import scipy.spatial.distance as ssd

def generateHPPP(X, Y, n):
    
    #Intensity (i.e., mean density) of the Poisson process
    lambda0 = (1. * n) / (X * Y)
    
    #We did not yet find the array of points
    findNP = False
    while (findNP == False):

        #Simulate Poisson Point Process
        numberOfPoints = scipy.stats.poisson(lambda0*(X * Y)).rvs() #Poisson number of points

        if (numberOfPoints == n):

            #X coordinates of Poisson points
            xx = X*scipy.stats.uniform.rvs(0,1,((numberOfPoints,1)))
            #Y coordinates of Poisson points
            yy = Y*scipy.stats.uniform.rvs(0,1,((numberOfPoints,1)))
            
            #Generate the list of the points from X and Y arrays
            points = np.column_stack((np.array(xx),np.array(yy)))
            
            #Compute the distances between all pairs of points and store it into a matrix
            distances = ssd.cdist(points,points)
            #Flat that matrix
            distances = distances.flatten()
            #Keep only the non zero values
            distances = distances[np.nonzero(distances)]

            findNP = True

    return points

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xaxis", help="Area size horizontally in meters.")
    parser.add_argument("-y", "--yaxis", help="Area size vertically in meters.")
    parser.add_argument("-n", "--nodes", help="Number of nodes.")
    args = parser.parse_args()

    result = generateHPPP(float(args.xaxis), float(args.yaxis), int(args.nodes))

    fileName = 'nodesPositions.csv'

    with open(fileName,'a') as resultsFile:
        resultsFile.write('Node ID;X;Y\n')

    for index in range(len(result)):

    	with open(fileName,'a') as resultsFile:
    		resultsFile.write('{};{};{}\n'.format(index, float(result[index][0]), float(result[index][1])))

    	resultsFile.close()

if __name__ == '__main__':
    main()