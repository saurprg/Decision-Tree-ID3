import pandas as pd
import math
def getdata():
    data = {
            'outlook':['sunny','sunny','overcast','rainy','rainy','rainy','overcast','sunny','sunny','rainy','sunny','overcast','overcast','rainy'],
            'temp':['hot','hot','hot','mild','cool','cool','cool','mild','cool','mild','mild','mild','hot','mild'],
            'humidity':['high','high','high','high','normal','normal','normal','high','normal','normal','normal','high','normal','high'],
            'windy':[False,True,False,False,False,True,True,False,False,False,True,True,False,True],
            'play':['no','no','yes','yes','yes','no','yes','no','yes','yes','yes','yes','yes','no']
    }
    data_frame = pd.DataFrame(data)
    return data_frame

def getBankData(split_fraction):
    if(split_fraction>1 and split_fraction<=0):
        print('Invalid Split Fraction')
        return None

    #read the data
    data_frame = pd.read_csv('bank.csv');
    
    
    data_records = data_frame[list(data_frame.columns)].to_dict(orient = 'records')
    new_data = []
    
    #PROCESSING OF DATA
    for data_record in data_records:
        
        #ASSIGN CLASS TO BALANCE RANGES
        if(data_record['balance']<10000):
            data_record['balance'] = 'LessThan10000'
        elif(data_record['balance']>=10000 and data_record['balance']<20000) :
            data_record['balance'] = 'LessThan20000'
        elif(data_record['balance']>=20000 and data_record['balance']<30000) :
            data_record['balance'] = 'LessThan30000'
        elif(data_record['balance']>=30000 and data_record['balance']<40000) :
            data_record['balance'] = 'LessThan40000'
        elif(data_record['balance']>=40000 and data_record['balance']<50000) :
            data_record['balance'] = 'LessThan50000'
        else:
            data_record['balance'] = 'GreaterThan500000'
            
        #ASSIGN CLASS DURATION RANGES
        if(data_record['duration']<=365):
            data_record['duration']='LessThan365secs'
        elif(data_record['duration']>365 and data_record['duration']<=730):
            data_record['duration']='LessThan730secs'
        elif(data_record['duration']>730 and data_record['duration']<=995):
            data_record['duration']='LessThan995secs'
        else:
            data_record['duration']='MoreThan995secs'
        
        #ASSIGN CLASS AGE RANGES
        if(data_record['age']<=40):
            data_record['age']='Adults'
        elif(data_record['age']>40 and data_record['age']<=60):
            data_record['age']='MiddleAged'
        else:
            data_record['age']='SeniorCitizens'
        
        new_data.append(data_record);
        
    data_frameq = pd.DataFrame(new_data);
    del data_frameq['pdays']
    #randomize the order of data
    data_frameq = data_frameq.sample(frac=1).reset_index(drop=True)
    
    #find the split point
    mid = int(round(split_fraction*len(data_frameq.index),0))
    
    #split the data
    train_data = data_frameq.iloc[ : mid , : ]
    test_data = data_frameq.iloc[ mid : , :  ]

    #return 
    return train_data,test_data

def unique_vals(data,attr):
    """"find unique values for column in dataset"""
    col = data[attr].unique()
    return list(col)

def getClassCount(data,attr,classname):
    """counts no. of examples for each given class"""
    return list((data[attr].values)).count(classname)

def getProportion(data,attr,classname):
    """propotion of particular class value"""
    return getClassCount(data,attr,classname)/len(list((data[attr].values)))


def entropy(data,attr,classname,lcol):
    """
        this function returns entropy of particular
        atrribute : 'attr' with  labels stored in 'lcol'
        for particular class(value) as 'classname'
        --additional : pass attr=lcol to get entropy of system
    """
    pyes=0.0
    pno=0.0
    if attr == lcol:
        #this condition is to find the entropy of system
        pyes = getProportion(data,attr,'yes')
        pno =  getProportion(data,attr,'no')
        lgyes = 0.0
        lgno = 0.0
        if(pyes != 0.0):
            lgyes=math.log2(pyes)
        if(pno != 0.0):
            lgno=math.log2(pno)
        entrpy = -pyes*lgyes-pno*lgno;
        return entrpy
    #only consider a part of dataframe with value classname
    df = data[data[attr] == classname]
    n = len(list(df[attr].values))
    if(n==0):
        #no such attribute value the enntropy can not be determind
        print('Error : No such attribute as',classname)
        return -1.0
    pyes = len(list(df[df[lcol]=='yes'][attr].values))/n
    pno = len(list(df[df[lcol]=='no'][attr].values))/n
    
    lgyes = 0.0
    lgno= 0.0
    
    if(pyes != 0.0):
        lgyes=math.log2(pyes)
    if(pno != 0.0):
        lgno=math.log2(pno)
    #H(S) = -P1log2(P1)-P2log2(P2)
    entrpy = -pyes*lgyes-pno*lgno;
    return entrpy

def split(data,attr,classname):
    """split data for given classname of given attribute"""
    return data[data[attr]==classname]

def find_best_node(data):
    """
        returns the name and entropy of maximum entropy attribute for give 'data'
    """
    columns , lcol= list(data.columns)[:-1],list(data.columns)[-1]
    max_tot_entropy = -1.0
    best_attr = ""
    sys_entropy = entropy(data,lcol,'-',lcol);
    # print("{0:10}   {1:10}".format("attribute","entropy"))
    # print('-----------------------')  
    for col in columns:
        tot_entropy = 0.0
        for classname in unique_vals(data,col):
            tot_entropy += getProportion(data,col,classname)*entropy(data,col,classname,lcol)
        tot_entropy = sys_entropy-tot_entropy
        # print("{0:10}   {1:2f}".format(col,tot_entropy))
        if(max_tot_entropy<tot_entropy):
            max_tot_entropy = tot_entropy
            best_attr = col
    # print("**Best Choice :",best_attr)
    return best_attr,max_tot_entropy

if __name__ == '__main__':
    # print(getdata())
    # print(unique_vals(getBankData(),'balance').count(59))
    # print(getClassCount(getdata(),'outlook','overcast'))
    # print(getProportion(getdata(),'outlook','overcast'))
    # print(entropy(getdata(),'play','temp','play'))
    # print(split(getdata(),'outlook','sunny'))
    # print(entropy(split(getdata(),'outlook','sunny'),'temp','mild','play'))
    data = getBankData(0.5)
    # print(entropy(data[data['outlook']=='overcast'][['temp','humidity','windy','play']],'play','-','play'))
    # print(unique_vals(data[data['outlook']=='overcast'][['temp','humidity','windy','play']],'play'))
    # find_best_node(data[data['outlook']=='overcast'][['temp','humidity','windy','play']])
