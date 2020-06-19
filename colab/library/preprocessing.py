import numpy as np
import pandas as pd

#pose : 0-23
#face : 24-163
    #lower-face-line : 24-57
    #eye-brow : 58-77
    #nose : 78-95
    #eye : 96-119
    #outer-mouth :  120-143
    #inner-mouth : 144-159
    #pupil : 160-163
#left hand : 164-205
#right hand : 205-247

def delete_face(X_):
    #X_ must be pyhton list
    array = []

    for i in range(len(X_)):
        temp_frame=[]
        if i == 0:
            temp_frame = X_[i][:24] #body
        else:
            temp_frame += X_[i][:24]
        temp_frame += X_[i][164:248] #left hand and right hand
        array.append(temp_frame)

    X_ = pd.DataFrame(array)
        
    #returns pandas dataframe
    return X_
    
def minimize_face(X_):
        #X_ must be pyhton list
        #include eye and outer-mouth
    array = []

    for i in range(len(X_)):
        temp_frame=[]
        if i == 0:
            temp_frame = X_[i][:24] #body
        else:
            temp_frame += X_[i][:24] #body
        temp_frame += X_[i][96:119] #eye
        temp_frame += X_[i][120:143] #outer-mouth
        temp_frame += X_[i][164:248] #left hand and right hand
        array.append(temp_frame)

    X_ = pd.DataFrame(array)
        
    #returns pandas dataframe
    return X_

def split_in_blocks(X_data, n_steps):
    blocks = int(len(X_data) / n_steps)
       
    return np.array(np.split(X_data,blocks))