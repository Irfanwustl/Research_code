#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yaml


# In[5]:


with open('inputs.yaml', 'r') as file:
    yamlinfo = yaml.safe_load(file)


# In[7]:


print(yamlinfo['sample_name'])

