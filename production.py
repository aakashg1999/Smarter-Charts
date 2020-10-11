
# In[1]:
import numpy as np # linear algebra
import pandas as pd 
from fastai import *
from fastai.vision import *
import torch


# In[2]:

def predict(img_path):
    bs=64
    path= "dataset"
    np.random.seed(2)
    data = ImageDataBunch.from_folder(path,no_check=True,size=224,bs=bs, num_workers=0)
    data.normalize(imagenet_stats)


    # In[3]:


    learn = cnn_learner(data, models.resnet34, metrics=error_rate)


    # In[4]:


    learn.load("testing")


# In[5]:




    # In[8]:
    img = open_image(img_path)
    


    # In[9]:


    #classes = ['hg', 'lg', 'pc', 'sg']
    #data2 = ImageDataBunch.single_from_classes(path, classes, size=224).normalize(imagenet_stats)


    # In[10]:


    pred_class,pred_idx,outputs = learn.predict(img)
    return pred_class


# In[ ]:

#value=predict("C:/Users/aakas/Desktop/Project/Download-2.png")
#print(value)

