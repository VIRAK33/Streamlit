import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime


def course_summary(md):

    df = []
    for i in range(0, len(md)):
        course = md.iloc[i][6]
        moduleName = md.iloc[i][7]
        dep = md.iloc[i][4]


        if [course,moduleName,dep] not in df:
            df.insert(i, [course,moduleName,dep])


    df = pd.DataFrame(df, columns = ['Course', 'Module Name','Department'])


    return df

def course_summary_(md):
    
    df = []
    for i in range(0, len(md)):
        course = md.iloc[i][6]
        moduleName = md.iloc[i][7]


        if [course,moduleName] not in df:
            df.insert(i, [course,moduleName])


    df = pd.DataFrame(df, columns = ['Course', 'Module Name'])

    return df

def courseStudent(md,course):
    if course == 'All':
        progress = md[(md['State'] == 1)]
    else:
        progress = md[(md['State'] == 1) & (md['Course Name'] == course)]
    # pg = progress.groupby(['Student Name','Course Name']).count()
    # print(pg[['ID']])
    arr = []
    for i in range(0, len(progress)):
        name = progress.iloc[i][2]
        sex =  progress.iloc[i][3]
        course = progress.iloc[i][6]

        completed = progress[progress['Student Name'] == name].count()


        if [name, sex,course, completed[0]] not in arr:
            arr.insert(i, [name, sex, course, completed[0]])


    pro = pd.DataFrame(arr, columns = ['Student Name', 'Sex', 'Course', 'Completed'])
    pro.sort_values(by=['Student Name'], inplace=True)
    return pro