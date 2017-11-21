# The decay of CDW signal. by Wenjie Chen

import numpy as np
#from databroker import DataBroker as db, get_table
import matplotlib.pyplot as plt
import codecs, json 


def require_fccd_intensity(time_interval, scan_num):
    '''
    [function]
        read fccd intensity of ROI data from scan # scan_num
    [args]
        time_interval: time interval between two pictures
        scan_num: integer
    [return]
        return a tuple variable (t, signal_area, background_area) where
            t: numpy array, time
            signal_area: numpy array, the counts of signal area
            background_area: numpy array, the counts of background area
    [example]
        (t, signal_area, background_area) = require_fccd_intensity(2, 95831)
    
    [author]
        Wenjie Chen
    '''
    # read data
    raw_data = db[scan_num]
    data=get_table(raw_data,fill=False)
    
    # prepare variables
    t = np.array([0])
    signal_area = np.array([])
    background_area = np.array([])
    
    # pull data out
    for count in data.fccd_stats2_total:
        signal_area = np.append(signal_area, count)
        t = np.append(t, t[-1] + time_interval)
    t = np.delete(t, -1)

    for count in data.fccd_stats3_total:
        background_area = np.append(background_area, count)
    
    # pack the variables to return a tuple
    return (t, signal_area, background_area)
    
def calculate_relative_intensity(signal_area, area_size1, background_area, area_size2):
    ''' 
    [function]
        calulate the relative intensity: mean signal - mean background. 
    
    [args]
        signal_area: numpy array, the counts of signal area
        background_area: numpy array, the counts of background area
        area_size1: the size of signal area
        area_size2: the size of background area
    [return]
        relative_intensity: numpy array
        
    [example]
        relative_intensity = calculate_relative_intensity(signal_area, 20000, background_area, 16000)
    
    [author]
        Wenjie Chen
    '''
    return signal_area/area_size1 - background_area/area_size2

def plot_decay_curve(t, relative_intensity):
    plt.figure(figsize=(8, 5))
    plt.plot(t, relative_intensity)
    plt.xlabel('t / s')
    plt.ylabel('relative intensity')
    plt.title('the decay of CDW signal')
    return


def save_decay_data(t, signal_area, background_area, FILEPATH):
    ''' 
    [function]
        save decay data to json file. 
    
    [args]
        t: numpy array, time
        signal_area: numpy array, the counts of signal area
        background_area: numpy array, the counts of background area
        FILEPATH: string. e.g., "./data/decay.json"
    
    [return]
        if success, return True
        
    [example]
        if save_decay_data(t, signal_area, background_area, "./data/decay.json")
    
    [author]
        Wenjie Chen
    '''
    t_tol = t.tolist()
    signal_area_tol = signal_area.tolist()
    background_area_tol = background_area.tolist()

    # package datas as a tuple
    data = (t_tol, signal_area_tol, background_area_tol)

    # write data as json
    json.dump(data, codecs.open(FILEPATH, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    return True

def read_decay_data(FILEPATH):
    ''' 
    [function]
        read decay data from json file. 
    
    [args]
        FILEPATH: string. e.g., "./data/decay.json"
    
    [return]
        return a tuple variable (t, signal_area, background_area) where
            t: numpy array, time
            signal_area: numpy array, the counts of signal area
            background_area: numpy array, the counts of background area
            
    [example]
        (t, signal_area, background_area) = read_decay_data("./data/decay.json")
    
    [author]
        Wenjie Chen
    '''
    obj_data = codecs.open(FILEPATH, 'r', encoding='utf-8').read()
    data = json.loads(obj_data)

    # unpack and pack the tuple
    return (np.array(data[0]), np.array(data[1]), np.array(data[2]))