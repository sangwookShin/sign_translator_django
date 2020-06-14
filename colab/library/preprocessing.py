import numpy as np
import pandas as pd

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

def split_in_blocks(X_data, n_steps):
    blocks = int(len(X_data) / n_steps)
       
    return np.array(np.split(X_data,blocks))