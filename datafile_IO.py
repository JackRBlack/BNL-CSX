import numpy as np
import codecs, json 

def write_data(FILEPATH, *args):
    ''' 
    [function]
        save several numpy array datas to json file. 
    
    [args]
        FILEPATH: string. e.g., "./data/decay.json"
        *args: numpy array, no limit of N
    
    [return]
        if success, return True
        
    [example]
        write_data("./data/somedata.json", a, b, c)
    
    [author]
        Wenjie Chen
    '''
    import codecs, json 
    data = []
    for var in args:
        data.append(var.tolist())

    # write data as json
    json.dump(data, codecs.open(FILEPATH, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    
    print("Successfully write data in", FILEPATH)
    
    return

def read_data(FILEPATH):
    ''' 
    [function]
        read several numpy array datas from json file. 
    
    [args]
        FILEPATH: string. e.g., "./data/decay.json"
    
    [return]
        a list of several numpy array datas
        
    [example]
        data = read_data("./data/somedata.json")
    
    [author]
        Wenjie Chen
    '''
    obj_data = codecs.open(FILEPATH, 'r', encoding='utf-8').read()
    temp = json.loads(obj_data)
    data = []
    # unpack and pack the tuple
    for var in temp:
        data.append(np.array(var))
    return data