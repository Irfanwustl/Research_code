import scipy.spatial.distance
import numpy as np

def distance(data,dataStd,refdata,phenoClass):
  



  total = 0
  num_obs = data.shape[0]


  for i in range(num_obs):
    for j in range(i+1,num_obs):
      total += scipy.spatial.distance.euclidean(data[i],data[j])

  return total

def correlation(data,dataStd,refdata,phenoClass):


  total = 0 

  with np.errstate(divide='ignore',invalid='ignore'):
    corr = np.corrcoef(data)

  # xij = NaN only occurs if either the variable xi or xj had variance 0
  # Then, cov(xi, xj) = 0
  # Therefore, we can set NaN values to 0
  corr[np.isnan(corr)] = 0
  #corr[np.isnan(corr)] = 1

  num_vars = corr.shape[0]
  for i in range(num_vars):
    for j in range(i+1,num_vars):
      total += abs(corr[i,j])

  return total




def condition(data,dataStd,refdata,phenoClass):
  '''
  print ("in condition number data")
  print(data)
  print ("dataStd")
  print(dataStd[:5])
  print("\n\n")
  '''
  return np.linalg.cond(data, p=2)

def condition2(data,dataStd,refdata,phenoClass):
  '''
  print ("in condition number data")
  print(data)
  print ("dataStd")
  print(dataStd[:5])
  print("\n\n")
  '''
  return np.linalg.cond(data.T, p=2)


def affectSize(data,dataStd,refdata,phenoClass):
  total = 0
  num_obs = data.shape[0]

  newdata=data.copy()
  newstd=dataStd.copy()

  newdata=newdata.astype(float)
  newstd=newstd.astype(float)


  newdataprocessed=np.divide(newdata,newstd,out=newdata, where=newstd!=0)

  for i in range(num_obs):
    for j in range(i+1,num_obs):
      total +=scipy.spatial.distance.euclidean(newdataprocessed[i],newdataprocessed[j])
      

  return total


def effectSize_cos(data,dataStd,refdata,phenoClass):
  total = 0
  num_obs = data.shape[0]

  newdata=data.copy()
  newstd=dataStd.copy()

  newdata=newdata.astype(float)
  newstd=newstd.astype(float)


  newdataprocessed=np.divide(newdata,newstd,out=newdata, where=newstd!=0)

  for i in range(num_obs):
    for j in range(i+1,num_obs):
      total +=scipy.spatial.distance.cosine(newdataprocessed[i],newdataprocessed[j])
      

  return total



#######ready. Did some manual check#####
def effectsize_cohen(data,dataStd,refdata,phenoclass):
    
  cohen_d=0
  
  maxindex=np.argmax(data,axis=0)
  
  
  
  n,d=data.shape
  
  for cpgindex in range(d):
      class2=phenoclass.iloc[maxindex[cpgindex],:]==2
      class2_mean=np.mean(refdata.values[cpgindex,class2])
      class2_std=np.std(refdata.values[cpgindex,class2])
      
      class1=phenoclass.iloc[maxindex[cpgindex],:]==1
      class1_mean=np.mean(refdata.values[cpgindex,class1])
      class1_std=np.std(refdata.values[cpgindex,class1])
      
      SDpooled=np.sqrt((class1_std**2+class2_std**2)/2)
      
      if SDpooled!=0:
          temp_d=(class1_mean-class2_mean)/SDpooled
      else:
          temp_d=(class1_mean-class2_mean)
      cohen_d=cohen_d+temp_d
  return cohen_d
#######done Did some manual check#####

def calculate_proportion(maxindex,phenoClass):
  n,d=phenoClass.shape
  
  total_cpg=maxindex.shape[0]
  proportion_list=[0] * n
  
  
  for celltype in range(n):
      temp= np.count_nonzero(maxindex==celltype)
      proportion_list[celltype]=temp
  
  #print(proportion_list)
  minval=min(proportion_list)
  #print(minval)
  shouldbe=float(total_cpg/n)
  #print(shouldbe)
  prop_score=minval/float(shouldbe)
  
  #print (prop_score)
  return prop_score

def effectsize_cohen2(data,dataStd,refdata,phenoclass):
    
  cohen_d=0
  
  maxindex=np.argmax(data,axis=0)
  

  
  prop=calculate_proportion(maxindex,phenoclass)
  
  
  n,d=data.shape
  
  for cpgindex in range(d):
      class2=phenoclass.iloc[maxindex[cpgindex],:]==2
      class2_mean=np.mean(refdata.values[cpgindex,class2])
      class2_std=np.std(refdata.values[cpgindex,class2])
      
      class1=phenoclass.iloc[maxindex[cpgindex],:]==1
      class1_mean=np.mean(refdata.values[cpgindex,class1])
      class1_std=np.std(refdata.values[cpgindex,class1])
      
      SDpooled=np.sqrt((class1_std**2+class2_std**2)/2)
      if SDpooled!=0:
          temp_d=(class1_mean-class2_mean)/SDpooled
      else:
          temp_d=(class1_mean-class2_mean)
     
      cohen_d=cohen_d+temp_d

  return cohen_d*prop
