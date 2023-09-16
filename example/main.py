import matplotlib.pyplot as plt
import pickle
import sys
sys.path.append(__file__ + '\..\..')

import TS2TF

# load normalized data
with open(__file__ + "\..\exampledata.pkl", 'rb') as file:
    x, y = pickle.load(file)

# Estimate system with second order tf
estimate = TS2TF.SOS(
    x, y, 
    epochs = 1000, 
    L = 0.9,
    K = 0.7,
    ωn = 5,
    ζ = 0.7
)

print(estimate['tf'])

plt.plot(x, y, alpha=0.75)
plt.plot(x, estimate['y'])
plt.show()