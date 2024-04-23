import numpy as np

def safe_position_grid_and_names(SafeOriginXYZ):
    SafeOriginX = SafeOriginXYZ[0]
    SafeOriginY = SafeOriginXYZ[1]
    SafeOriginZ = SafeOriginXYZ[2]
    
    SamplingPointsX = 5
    SamplingPointsY = 5
    SamplingSpacingX = 100 #mm
    SamplingSpacingY = 100 #mm
    
    SafePositionGridAndNames = np.array(np.zeros((SamplingPointsX, SamplingPointsY, 6)), dtype=object)
    PointNameInt = 0
    
    for YPoint in range(SafePositionGridAndNames.shape[1]):
        for XPoint in range(SafePositionGridAndNames.shape[0]):
            XCoordsmm = np.round(SafeOriginX+XPoint*SamplingSpacingX,3)
            YCoordsmm = np.round(SafeOriginY+YPoint*SamplingSpacingY,3)
            ZCoordsmm = np.round(SafeOriginZ)
            SafePositionGridAndNames[XPoint, YPoint, 0] = XCoordsmm
            SafePositionGridAndNames[XPoint, YPoint, 1] = YCoordsmm
            SafePositionGridAndNames[XPoint, YPoint, 2] = ZCoordsmm
            SafePositionGridAndNames[XPoint, YPoint, 3] = make_PointName(PointNameInt, XCoordsmm, YCoordsmm)
            SafePositionGridAndNames[XPoint, YPoint, 4] = make_ButtonTag(XPoint, YPoint)
            SafePositionGridAndNames[XPoint, YPoint, 5] = PointNameInt
            
            PointNameInt = PointNameInt + 1
    
    return SafePositionGridAndNames

def make_PointName(PointNameInt, XCoordsmm, YCoordsmm):
    return 'Sampling '+str(PointNameInt)+': \n('+str(XCoordsmm)+','+str(YCoordsmm)+') mm'

def make_ButtonTag(XPoint, YPoint):
    return 'Sampling '+str(XPoint)+','+str(YPoint)