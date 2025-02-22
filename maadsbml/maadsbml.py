#!/usr/bin/env python
# coding: utf-8

# In[37]:


import maadsbml
import json
import os
import time
# Uncomment IF using jupyter notebook
import nest_asyncio
# Uncomment IF using jupyter notebook
nest_asyncio.apply()


# In[38]:


host='http://127.0.0.1'
port=5595
######################### Change these two folder to your local paths that you used for the volume mappings in Docker
localstagingfolder = "c:\\maads\\agentfilesdocker\\dist\\staging" # change this folder to your local mapped staging folder
localexceptionfolder = "c:\\maads\\agentfilesdocker\\dist\\maadsweb\\exception" # change this folder to your local mapped exception folder
#########################################################

def readifbrokenpipe(jres,hasseasonality):
      # this function is called if there is a broken pipe network issue
      pkey=""
      algofile=""        
      jsonalgostr = ""
    
      pkey= jres.get('AlgoKey')
    
      maadsbmlfile="%s\\%s.txt.working" % (localstagingfolder,pkey)
      if hasseasonality == 1:
        algojsonfile="%s\\%s_trained_algo_seasons.json" % (localexceptionfolder,pkey)
      else:
        algojsonfile="%s\\%s_trained_algo_no_seasons.json" % (localexceptionfolder,pkey)
      
      while True:
          time.sleep(5)            
          if os.path.isfile(maadsbmlfile): 
               continue
          elif os.path.isfile(algojsonfile):
                # Read the json            
              with open(algojsonfile) as f:
                  jsonalgostr = json.load(f)
              break # maadsbml finished
      return jsonalgostr

def hypertraining(host,port,filename,dependentvariable,removeoutliers,hasseasonality,deepanalysis):
  #def hypertraining(host,port,filename,dependentvariable,removeoutliers=0,hasseasonality=0,
    #summer='6,7,8',winter='11,12,1,2',shoulder='3,4,5,9,10',trainingpercentage=70,shuffle=0,
    #deepanalysis=0,username='admin',timeout=1200,company='otics',password='123',email='support@otics.ca',
    #usereverseproxy=0,microserviceid='',maadstoken='123',mode=0):


  #host,port,
  #filename= raw data file in csv format - Note this file is stored on your host machine the DOCKER container needs to be mapped to this volume using -v
  #dependentvariable= dependent variable name - this is the column name in the csv file
  # the file should have a Date column in the format Month/Day/Year
  #username= you can specify a username
  #mode=0
  #timeout=180 - you can modify this in seconds if your data file is large
  #company= change this to the name of your company
  #removeoutliers= specify 1 or 0, 1=remove outliers, 0 do not remove outliers,
  #hasseasonality= specify 1 or 0 to indicate date is affected by seasonaility - 1 = seasonality, 0 = no seasonality,
  #summer= specify the summer months ie. '6,7,8', or set to -1 for no summer
  #winter= specify winter months i.e. '11,12,1,2', or -1 for no winter
  #shoulder= specify shoulder months i.e. '3,4,5,9,10', or -1 for no shoulder season
  #trainingpercentage= specify training percentage i.e. 70, the value represents a percentage to split training and test
  #shuffle= specify 1 or 0 to shuffle the data, 1= shuffle, 0 = no shuffle
  #deepanalysis= specify 1 or 0, 1=deepanalysis, note this will run through deeper algorithms but will take longer, 0 = no deep analysis, this will
  #password='123', - leave as is
  #email='support@otics.ca', - leave as is
  #usereverseproxy=0, - leave as is
  #microserviceid='', leave as is
  #maadstoken='123' leave as is
  summer='6,7,8'
  winter='11,12,1,2'
  shoulder='3,4,5,9,10'
  #shoulder='-1'
  trainingpercentage=75
  shuffle=1
  res=maadsbml.hypertraining(host,port,filename,dependentvariable,removeoutliers,hasseasonality,summer,winter,shoulder,trainingpercentage,shuffle,deepanalysis)
  jres = json.loads(res)

  if jres.get('BrokenPipe') != None: # check if the hypertraining function experienced a brokenpipe - if so wait 
        try:
          res=readifbrokenpipe(jres,hasseasonality)
        except Exception as e:
          print(e)  
           
  print(res)


def hyperprediction(pkey,host,port,inputdata,username):
  
  res=maadsbml.hyperpredictions(pkey,inputdata,host,port,username)
  print(res)

def hyperpredictioncustom(pkey,host,port,inputdata,username,algoname,season):
  res=maadsbml.hyperpredictions(pkey,inputdata,host,port,username,algoname,season)
  print(res)
  
def algoinfo(pk):
   res=maadsbml.algodescription(host,port,pk)
   print(res)

def rundemo(demotype):
    # if demotype=1 then Regression will be run
    # if demotype=0 then Classification will be run
   res=maadsbml.rundemo(host,port,demotype)
   print(res)

def abort(host,port):
   res=maadsbml.abort(host,port)
   print(res)



# In[43]:


# ############Function Commands
# Algoinfo
pk='admin_aesopowerdemand_csv'
#algoinfo(pk)

#pk='admin_aesopowerdemandlogistic_csv'
#algoinfo(pk)

# ############Abort
#abort(host,10000)

# ############Rundemo
#rundemo(1)


# In[45]:


############ Hypertraining
#filename='aesopowerdemandlogistic.csv'
#dependentvariable='AESO_Power_Demand_Label'

filename='aesopowerdemand.csv'
#filename='aesopowerdemandsm.csv'
dependentvariable='AESO_Power_Demand'
removeoutliers=1
hasseasonality=0
deepanalysis=0

#hypertraining(host,port,filename,dependentvariable,removeoutliers,hasseasonality,deepanalysis)


# In[42]:


# ############Hyperpredictions
predictionport=5595
pkey='admin_aesopowerdemandlogistic_csv'
inputdata='6/10/2010,-14.3,-32.0,-12.0'
hyperprediction(pkey,host,predictionport,inputdata,'admin')

#hyperpredictioncustom(pkey,host,predictionport,inputdata,'admin','LogisticRegression','allseason')

pkey='admin_aesopowerdemand_csv'
inputdata='6/10/2010,-14.3,-52.0,-12.0'
hyperprediction(pkey,host,predictionport,inputdata,'admin')

algo='simpleregression_reg'
season='summer'
#hyperpredictioncustom(pkey,host,predictionport,inputdata,'admin',algo,season)


# In[ ]:





# In[ ]:




