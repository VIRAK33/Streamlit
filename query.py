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


def listStudent(progress):
    arr = []
    studentInDepartment = []
    for i in range(0, len(progress)):
        id = progress.iloc[i][1]
        name = progress.iloc[i][2]
        sex =  progress.iloc[i][3]
        dep = progress.iloc[i][4]
        group = progress.iloc[i][5]
        course = progress.iloc[i][6]
        module = progress.iloc[i][7]
        completedDate = progress.iloc[i][9]
        year = progress.iloc[i][10]

        if [id, name, sex,course,group, dep, module, year] not in arr:
            arr.insert(i, [id, name, sex, course,group, dep, module, year])
        if [id, name, sex, dep, year] not in studentInDepartment:
            studentInDepartment.insert(i, [id, name, sex, dep, year])
            
    md1 = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course','Group', 'Department', 'Module', 'Year'])
    listStudentInDepartment = pd.DataFrame(studentInDepartment, columns = ['ID', 'Student Name', 'Sex', 'Department', 'Year'])
    return md1, listStudentInDepartment

def numberStudentEachCourse(md1):
    arr_= []
            
    for i in range(0, len(md1)):
        course = md1.iloc[i][3]
        dep = md1.iloc[i][5]
        module = md1.iloc[i][6]
        year = md1.iloc[i][7]

        m = md1[(md1['Course'] == course) & (md1['Sex'] == 'M')].count()
        male = m[0]
        f = md1[(md1['Course'] == course) & (md1['Sex'] == 'F')].count()
        female = f[0]

        if [course, year , male, female] not in arr_:
            arr_.insert(i,[course, year , male, female])
    md2 = pd.DataFrame(arr_, columns = ['Course', 'Year' , 'Male', 'Female'])
    return md2

def studentDetail(md, studentName):
    arr = []
    md = md[(md['Student Name'] == studentName)]
    course = md['Course Name'].unique()

    for i in range(0, len(course)):

        totalCourse = md[(md['Course Name'] == course[i])].count()
        if [course[i], totalCourse[0]] not in arr:
            arr.insert(i, [course[i], totalCourse[0]])
        
        md2 = pd.DataFrame(arr, columns = ['Course', 'Total Completed'])

    return md2