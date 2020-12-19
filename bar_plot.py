#!/usr/bin/env python
# coding: utf-8

# # PM25 Barplot

# ## Import library

# In[326]:


import pandas as pd
import matplotlib.pyplot as plt


# ## Read .csv file
# ให้นำ .csv ไปใส่ใน folder ชื่อ City แล้วใส่ชื่อเมืองที่จะนำเข้าโปรแกรม

# In[327]:


city = "Bangkok"
df = pd.read_csv('./City/'+ city +'.csv')


# ## Process flow
# หลังจากที่เราอ่านไฟล์มาแล้ว ขั้นแรกเราจะตัดในส่วนที่ไม่มีข้อมูล PM2.5 ออกรวมถึงค่าที่เราไม่ได้ใช้

# In[328]:


df = df.loc[df['pm25']!=' ']
df = df[['date','pm25']]


# แปลงค่า date เป็นชนิด datetime และค่า PM2.5 เป็นชนิดตัวเลข

# In[329]:


df['date'] = pd.to_datetime(df.date)
df['pm25'] = pd.to_numeric(df.pm25)


# เลือกช่วงเวลาที่เราสนใจ

# In[330]:


df_2018 = df.loc[(df['date'].dt.year == 2018) & (df['date'].dt.month >= 10)]
df_2019 = df.loc[(df['date'].dt.year == 2019)]
df_2020 = df.loc[(df['date'].dt.year == 2020) & (df['date'].dt.month < 3)]
df = df_2018.append(df_2019.append(df_2020), ignore_index=True)


# In[331]:


df


# ในส่วนนี้เราจะใช้ date แบ่งออกเป็นเดือนและปี แล้วจากนั้นจะใช้ฟังชั่นเพื่อนับค่า PM2.5 ที่มีค่าเกิน 100 ในแต่ละเดือน

# In[332]:


df = df.groupby([df['date'].dt.year.rename('year'), df['date'].dt.month.rename('month')])['pm25'].apply(lambda x: (x>100).sum()).reset_index()


# In[333]:


df


# เราไม่ชอบตัวเลข จึงเปลี่ยนตัวเลขธรรมดาให้กลายเป็นอักษรย่อ

# In[334]:


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


# In[335]:


df


# เปลี่ยน year กับ month เป็น string

# In[336]:


df['year'] = df['year'].astype(str)
df['month'] = df['month'].astype(str)


# เราจะใช้ year กับ month ที่แปลงเป็น string สร้าง col ใหม่เพื่อให้สวยงาม

# In[337]:


df['month_year'] = df['month'] + " - " + df['year']


# ตั้งค่ากราฟโดยตั้งให้ month_year เป็น row แล้วใช้ pm25 plot แล้วนำสิ่งที่ plot ไป save เก็บไว้ใน folder ชื่อ City_Barlot

# In[338]:


ax = df.set_index('month_year')['pm25'].plot(kind='bar',figsize=(19, 10),color='cadetblue',rot=45, fontsize=14)
plt.title("Historical PM2.5 > 100 Per Month ("+ city +")", y=1.013, fontsize=22)
plt.ylabel("Count of PM2.5 > 100", labelpad=16, fontsize=16)
plt.xlabel("", labelpad=16, fontsize=16)

for p in ax.patches:
    ax.annotate("%d" % p.get_height(), (p.get_x() + p.get_width() / 2, p.get_height()),
                ha='center', va='center', fontsize=16, color='black', rotation=0, xytext=(0, 7),
                textcoords='offset points')
    
figure = ax.get_figure()    
figure.savefig('./City_Barplot/'+city+'.png', dpi=150)


# In[ ]:




