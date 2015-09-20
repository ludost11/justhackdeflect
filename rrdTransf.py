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
    
    def dateToLinuxT(self, dateStart,dateEnd,startTime,endTime):
        """ 
        Transform real date and time into unix time format        
            Examples arguments format:
                    date = '25/12/1970'  ----- DAY/MONTH/YEAR
                    date = '26/12/1970'
                    startTime = [14,30]  ----- 24h schedule with hour and min
                    endTime = [8,00]
        """
        startDateLinux = time.mktime(datetime.datetime.strptime(dateStart, "%d/%m/%Y").timetuple())
        startTimeLinux = startDateLinux + startTime[0]*60*60 + startTime[1]*60
        endDateLinux = time.mktime(datetime.datetime.strptime(dateEnd, "%d/%m/%Y").timetuple())      
        endTimeLinux = endDateLinux + endTime[0]*60*60 + endTime[1]*60
        
        return startTimeLinux, endTimeLinux
        
        
    def rrdToMat(self,filesDir,nbSamp):
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
#        N = (endLinuxTime-startLinuxTime)*60/sampleRate+1 #Number of data point. The +1 is to include start & end
        DataMap = np.zeros([nbSamp,Dim]) #Matrix initialization
        
        os.chdir(filesDir) #Goes into dir where files are located
         
        for file in os.listdir(filesDir):  #Goes through each file in the dir
        	if file[-3:] == 'rrd': #make sure to use only the rrd files
                 
#                 startRow = 
        		
        		myrrd = pyrrd.rrd.RRD(file)
        		data = myrrd.fetch()
        		
        		for CatIndex in range(0, len(data)): #Every category in each file
        			Cat = data.keys()[CatIndex]  #Current category

           			if Cat in CatToInclude:
        				print Cat		
                            
        				for lineNo in range(0,nbSamp-1):
        					catNo = CatToInclude.index(Cat)
        					DataMap[lineNo,catNo] = data[Cat][lineNo][1]
        					data[data.keys()[CatIndex]][0]
        
        os.chdir(curDir) #Goes back to original workspace

        return DataMap
  
  
  
  
#add all len + 1 to know the number of dimmensions of the vectors
#datetime(1970,1,1).total_secconds()
#Corrupt fiiles : 9cf865ecd54b3e9a5a6174ca20a57ed6.rrd ['HTTP', 'ssh']  
#				6cd61c25ed55b002e865a54757ed2b86.rrd ['RX_packets', 'RX_Bytes', 'TX_errors', 'RX_errors', 'TX_Bytes', 'TX_packets']
#				0867550c23cc09ebbb1e4cada39ac7e6.rrd ['RX_Bytes']
#				user, MEM
#		 	