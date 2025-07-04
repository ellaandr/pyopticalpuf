import sys
import os
from typing import List

from matplotlib import pyplot as plt
import numpy as np
OPUF_DIR = ""
sys.path.append(os.path.dirname(OPUF_DIR))

from pyOpticalPUF.Utility import ImageHelper
from itertools import product
from pyOpticalPUF.HammingDistanceCalculators import HammingDistanceCalculator
from pyOpticalPUF.Distributions import GuassianDistribution
from pyOpticalPUF.Display import DistributionDisplay, OverTimeTestingDispaly

def calculateHammingDistance(intraFingerprints: List[np.ndarray], interFingerprints: List[np.ndarray]):
    #1. Create every combination of intras (ignoring comparing the same image twice) and inters 
    allIntraCombinations = [(intraOne, intraTwo) for intraOne, intraTwo in product(intraFingerprints, intraFingerprints) if intraOne is not intraTwo]
    allIntraInterCombinations = product(intraFingerprints, interFingerprints)

    #2. Calculate hamming distance
    intraHammingDistances = [HammingDistanceCalculator.calculateHammingDistance(intraOne, intraTwo).hammingDistance for intraOne, intraTwo in allIntraCombinations]
    intersHammingDistances = [HammingDistanceCalculator.calculateHammingDistance(intra, inter).hammingDistance for intra, inter in allIntraInterCombinations]
    return intraHammingDistances, intersHammingDistances

if __name__ == "__main__":

    intraInterFolders = [
        ["example output/intras", "example output/inters"],
        ["example output/intras", "example output/inters"],
        ["example output/intras", "example output/inters"],
    ]

    intraHammingDistances = []
    interHammingDistances = []

    for intraFolder, interFolder in intraInterFolders:
        intraFingerprints = ImageHelper.loadImagesFromFolder(intraFolder)
        interFingerprints = ImageHelper.loadImagesFromFolder(interFolder)
        intraHDs, interHDs = calculateHammingDistance(intraFingerprints, interFingerprints)
        
        intraHDs = np.add(intraHDs, np.random.random(len(intraHDs)) * 0.1)
        interHDs = np.add(interHDs, np.random.random(len(interHDs)) * 0.1)
        intraHammingDistances.append(intraHDs)
        interHammingDistances.append(interHDs) 

    intraGuassians = [GuassianDistribution.fromData(dist) for dist in intraHammingDistances]
    interGuassians = [GuassianDistribution.fromData(dist) for dist in interHammingDistances]

    OverTimeTestingDispaly.plot(intraGuassians, interGuassians, intraHammingDistances, interHammingDistances)
    plt.show()