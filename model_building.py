import os
from PIL import Image
import numpy as np
import pandas as pd


data=[]
labels=[]
path=os.path.join(os.getcwd(),'image_data')
for i in os.listdir(path):
    label=i
    for j in os.listdir(os.path.join(path,i)):
        img=Image.open(os.path.join(os.path.join(path,i),j))
        arr=np.array(img).reshape(-1)
        data.append(arr)
        labels.append(label)

data=np.array(data)
print(data.shape)
df=pd.DataFrame(data)
print(df.shape)
# df['label']=labes

