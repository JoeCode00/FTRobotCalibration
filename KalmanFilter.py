import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from pykalman import KalmanFilter

#FTData = pd.FTDataFrame(columns=['NoiseAR','NoiseReg', 'x', 'beta', 'y'], index=range(1000))
FTData = np.zeros((6,1000,2))
# FTData['NoiseAR'] = np.random.normal(loc=0.0, scale=1.0, size=1000)
# FTData['NoiseReg'] = np.random.normal(loc=0.0, scale=1.0, size=1000)
# plt.plot(FTData[['NoiseAR','NoiseReg']])
# plt.show()

FTData_Entries = 0

FTData[0,:,0] = [0,0,0,0,0,0]
FTData = np.roll(FTData, 1, 1)
FTData_Entries = FTData_Entries + 1

if FTData_Entries > 1000:
    
# for i in range(1000):
#     if i == 0:
#         FTData.loc[i, 'x'] = FTData.loc[i, 'NoiseAR']
#     else:
#         FTData.loc[i, 'x'] = 0.95 * FTData.loc[i - 1, 'x'] + FTData.loc[i, 'NoiseAR']

# plt.plot(FTData['x'])
# plt.show()

# for i in range(1000):
#     FTData.loc[i, 'beta'] = np.sin(np.radians(i))

# plt.plot(FTData['beta'])
# plt.show()

# FTData['y'] = FTData['x']*FTData['beta'] + FTData['NoiseReg']

# plt.plot(FTData[['x', 'y']])
# plt.show()


#H = FTData['FZ'].values.reshape(1000,1,1).astype(float)

    
    kf = KalmanFilter(
        transition_matrices=[1.],
        observation_matrices=np.reshape(FTData[1,:,0],(1000,1,1)).tolist(),
        transition_covariance=[2.],
        observation_covariance=[2.],
        initial_state_mean=[0.],
        initial_state_covariance=[2.],
        em_vars=['transition_covariance', 'observation_covariance', 'initial_state_mean', 'initial_state_covariance']
    )
    
    #kf = kf.em(FTData['y'].values.astype(float))
    kf = kf.em(FTData[2,:,0].tolist())
    
    # filtered_state_estimates = kf.filter(FTData['y'].values.astype(float))[0]
    # smoothed_state_estimates = kf.smooth(FTData['y'].values.astype(float))[0]
    
    filtered_state_estimates = kf.filter(FTData[2,:,0].tolist())[0]
    smoothed_state_estimates = kf.smooth(FTData[2,:,0].tolist())[0]
    
    smoothed_output = smoothed_state_estimates[999]

pl.figure(figsize=(10, 6))
lines_true = pl.plot(FTData['beta'].values, linestyle='-', color='b')
lines_filt = pl.plot(filtered_state_estimates, linestyle='--', color='g')
lines_smooth = pl.plot(smoothed_state_estimates, linestyle='-.', color='r')
pl.legend(
    (lines_true[0], lines_filt[0], lines_smooth[0]),
    ('true', 'filtered', 'smoothed')
)
pl.xlabel('time')
pl.ylabel('state')

pl.show()