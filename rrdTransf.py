# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 17:58:46 2015
@author: phc & Chris L.


Transform the data of a server's rrd files into a numpy matrix


"""
import pyrrd.rrd
import os
import numpy as np
import time
import datetime

class rrdTransf:
    #Functions that allow convertion of rrd files into python useful format
    
    def __init__(self):
        self.data = []
    
    def dateToLinux(self, dateStart,dateEnd,startTime,endTime):
        """ 
        Transform real date and time into unix time format        
            Examples arguments format:
                    date = '25/12/1970'  ----- DAY/MONTH/YEAR
                    date = '26/12/1970'
                    startTime = [14,30]  ----- 24h schedule with hour and min
                    endTime = [8,00]  --- Dont forget to include the mins, even if 00
        """
        startDateLinux = time.mktime(datetime.datetime.strptime(dateStart, "%d/%m/%Y").timetuple())
        startTimeLinux = startDateLinux + startTime[0]*60*60 + startTime[1]*60
        endDateLinux = time.mktime(datetime.datetime.strptime(dateEnd, "%d/%m/%Y").timetuple())      
        endTimeLinux = endDateLinux + endTime[0]*60*60 + endTime[1]*60
        
        return int(startTimeLinux), int(endTimeLinux)
        
        
    def rrdToMat(self,startTimeLinux,endTimeLinux,filesDir,sampleRate=10):
        # Name of the categories that will be included from the rrd files
        # sampleRate has to be written in MINUTES
        curDir = os.getcwd()
        
        # Which categories to include in the matrix
        CatToInclude = ["OUT", "TOTAL", "IN", 
        			"http_res", 
        			"RTA",
        			"1min", "5min", "15min",
        			"ESTABLISHED", "WAITING", "LISTENERS",
        			"DROP",
        			"Loss"] #RTA and http_res will have to be excluded 
        					#when workking with different dataset because they repeat themselves
        
        Dim = len(CatToInclude) #Number of type of data
        N = int((endTimeLinux-startTimeLinux)/60/sampleRate) #Number of data point. The +1 is to include start & end
        DataMap = np.zeros([N,Dim]) #Matrix initialization
        
        os.chdir(filesDir) #Goes into dir where files are located
         
        for file in os.listdir(filesDir):  #Goes through each file in the dir
        	if file[-3:] == 'rrd': #make sure to use only the rrd files
        		
        		myrrd = pyrrd.rrd.RRD(file)
        		data = myrrd.fetch(start=startTimeLinux,end=endTimeLinux)
        		
        		for CatIndex in range(0, len(data)): #Every category in each file
        			Cat = data.keys()[CatIndex]  #Current category
        
           			if Cat in CatToInclude:
        				print Cat		
                            
        				for lineNo in range(0,N-1):
        					catNo = CatToInclude.index(Cat)
        					DataMap[lineNo,catNo] = data[Cat][lineNo][1]
        					data[data.keys()[CatIndex]][0]
            
        os.chdir(curDir) #Goes back to original workspace
        return DataMap
