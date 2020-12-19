#!/usr/bin/env python
# coding: utf-8

# # PM25 Heatmap

# ## Import library

# In[426]:


import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


# ## Read .csv file
# ให้นำ .csv ไปใส่ใน folder ชื่อ City แล้วใส่ชื่อเมืองที่จะนำเข้าโปรแกรม

# In[427]:


city = "Bangkok"
df = pd.read_csv('./City/'+ city +'.csv')


# ## Process flow
# หลังจากที่เราอ่านไฟล์มาแล้ว ขั้นแรกเราจะตัดในส่วนที่ไม่มีข้อมูล PM2.5 ออกรวมถึงค่าที่เราไม่ได้ใช้

# In[428]:


df = df.loc[df['pm25']!=' ']
df = df[['date','pm25']]


# แปลงค่า date เป็นชนิด datetime และค่า PM2.5 เป็นชนิดตัวเลข

# In[429]:


df['date'] = pd.to_datetime(df.date)
df['pm25'] = pd.to_numeric(df.pm25)


# เรียงลำดับข้อมูลใหม่ด้วย date

# In[430]:


df = df.sort_values('date')


# สร้าง col ใหม่โดยแบ่ง datetime เป็น day,month และ year

# In[431]:


df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['year'] = df['date'].dt.year


# เราไม่ชอบตัวเลข จึงเปลี่ยนตัวเลขธรรมดาให้กลายเป็นอักษรย่อ

# In[432]:


month_to_short = {1: "Jan",
                  2: "Feb",
                  3: "Mar",
                  4: "Apr",
                  5: "May",
                  6: "Jun",
                  7: "Jul",
                  8: "Aug",
                  9: "Sep",
                  10: "Oct",
                  11: "Nov",
                  12: "Dec"}
df['month'] = df['month'].map(month_to_short)


# เราจะใช้ year กับ month แปลงเป็น string สร้าง col ใหม่เพื่อให้สวยงาม

# In[433]:


df['year'] = df['year'].astype(str)
df['month'] = df['month'].astype(str)
df['month_year'] = df['month'] + " - " + df['year']


# สร้าง cats เพื่อใช้เป็นลำดับในการเรียงข้อมูล

# In[434]:


cats = []
for x in pd.unique(df['month_year']):
    cats.append(x)


# เลือกช่วงเวลาที่เราสนใจ

# In[435]:


df_2018 = df.loc[(df['date'].dt.year == 2018) & (df['date'].dt.month >= 10)].reset_index(drop=True)
df_2019 = df.loc[(df['date'].dt.year == 2019)].reset_index(drop=True)
df_2020 = df.loc[(df['date'].dt.year == 2020) & (df['date'].dt.month < 3)].reset_index(drop=True)
df = df_2018.append(df_2019.append(df_2020), ignore_index=True)


# เปลี่ยน dataframe โดยใช้ index เป็น month_year และ ใช้ day เป็น col ใส่ values ด้วยค่า pm25

# In[436]:


df = df.pivot(index='month_year', columns='day', values='pm25')


# หลังจากที่เปลี่ยน dataframe ใหม่เราต้องเรียงลำดับใหม่ โดยใช้ cats ที่ทำไว้ก่อนหน้านี้

# In[437]:


df.index = pd.CategoricalIndex(df.index, categories= cats)
df.sort_index(level=0, inplace=True)


# ตั้งค่า heatmap ที่จะ plot เราจะใช้ seaborn ในการ plot แล้วนำสิ่งที่ plot ไปทำเป็นรูป

# In[438]:


sns.palplot(sns.diverging_palette(1, 1, n = 19))
plt.figure(figsize =(40,15))
sns.set(font_scale = 2)
ax = sns.heatmap(df,annot=True, fmt=".0f", cmap="YlOrRd", linewidths=0.05, vmin=0, vmax=200)
figure = ax.get_figure()    
figure.savefig('./City_Heatmap/'+city+'.png', dpi=150)

