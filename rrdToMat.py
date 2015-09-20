# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 17:58:46 2015

@author: phc
"""
import pyrrd.rrd
import os
import datetime
import numpy as np


FileDir = "/home/phc/Desktop/justhackdeflect/hetzner9"
CatToInclude = ["OUT", "TOTAL", "IN", 
			"http_res", 
			"RTA",
			"1min", "5min", "15min",
			"ESTABLISHED", "WAITING", "LISTENERS",
			"DROP",
			"Loss"] #RTA and http_res will have to be excluded 
					#when workking with different dataset because they repeat themselves
os.chdir(FileDir)


Dim = len(CatToInclude)
rowNb = 288 #To change according to data (number of sample)

DataMap = np.zeros([rowNb,Dim])

for i in os.listdir('.'):
	if i[-3:] == 'rrd':
		
		myrrd = pyrrd.rrd.RRD(i)
		data = myrrd.fetch()
		
		for CatIndex in range(0, len(data)):
			Cat = data.keys()[CatIndex]
			if Cat in CatToInclude:
				print Cat		
				for lineNb in range(0,rowNb-1):
					catNb = CatToInclude.index(Cat)
					DataMap[lineNb,catNb] = data[Cat][lineNb][1]
					data[data.keys()[CatIndex]][0]

#		print len(data)
		
#add all len + 1 to know the number of dimmensions of the vectors
#datetime(1970,1,1).total_secconds()
#Corrupt fiiles : 9cf865ecd54b3e9a5a6174ca20a57ed6.rrd ['HTTP', 'ssh']  
#				6cd61c25ed55b002e865a54757ed2b86.rrd ['RX_packets', 'RX_Bytes', 'TX_errors', 'RX_errors', 'TX_Bytes', 'TX_packets']
#				0867550c23cc09ebbb1e4cada39ac7e6.rrd ['RX_Bytes']
#				user, MEM
#		 	