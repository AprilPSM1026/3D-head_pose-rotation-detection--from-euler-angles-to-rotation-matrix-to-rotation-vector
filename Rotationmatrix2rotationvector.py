import math
import numpy as np
import cv2
from scipy.spatial import distance as dist
def Euler_convert2rotationvector(head_rotation):
      
    roll =head_rotation[:,1]
    pitch =head_rotation[:,0]
    yaw = head_rotation[:,2]
    
    #---original coordinate value
    x0=np.array([1,0,0])
    y0=np.array([0,1,0])
    z0=np.array([0,0,1])
 
    init_point=np.sqrt((np.square(x0)+np.square(y0)+np.square(z0)))

    head_distance_=[]
    
    print 'init = ',init_point 
    print "roll = ", roll
    print "pitch = ", pitch
    print "yaw = ", yaw
    print ""
    yxz_=[]
    for key,yaw_ in enumerate(yaw):
        yawMatrix = np.matrix([
        [math.cos(yaw_), -math.sin(yaw_), 0],
        [math.sin(yaw_), math.cos(yaw_), 0],
        [0, 0, 1]
        ])

        pitchMatrix = np.matrix([
        [math.cos(pitch[key]), 0, math.sin(pitch[key])],
        [0, 1, 0],
        [-math.sin(pitch[key]), 0, math.cos(pitch[key])]
        ])

        rollMatrix = np.matrix([
        [1, 0, 0],
        [0, math.cos(roll[key]), -math.sin(roll[key])],
        [0, math.sin(roll[key]), math.cos(roll[key])]
        ])

        R = yawMatrix * pitchMatrix * rollMatrix  #-------compute rotation matrix
       
        theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
        
        if theta!=0:
            multi = 1 / (2 * math.sin(theta))
        else:
            multi=0
        
        rx = multi * (R[2, 1] - R[1, 2]) * theta
        ry = multi * (R[0, 2] - R[2, 0]) * theta
        rz = multi * (R[1, 0] - R[0, 1]) * theta
        
        yxz=np.array([ry,rx,rz])
        yxz_.append(yxz)#----------composed in the order of yxz     
    
    yxz2arr=np.array(yxz_)

    #-----head movement variance analysis    
    accumulated_distance_ = 0.0
    accumulated_distance=[]
    for key in range(1,len(yxz2arr)):
        
        cur_distance=dist.euclidean(yxz2arr[key-1],yxz2arr[key])
        accumulated_distance_=accumulated_distance_+cur_distance
        accumulated_distance.append(accumulated_distance_)
        
    accumulated_distance2arr=np.array(accumulated_distance)
   
    return acm_distance2arr
