import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime


def course_summary(md):

    # start_date = '2020-10-22'
    # end_date = '2020-12-01'

    df = []
    for i in range(0, len(md)):
        course = md.iloc[i][6]
        moduleName = md.iloc[i][7]
        # male_student = md[ (md['Sex'] == 'M') & (md['Course Name'] == course) & (md['Completion Date'] >= str(start_date)) & (md['Completion Date'] <= str(end_date))]
        # female_student = md[ (md['Sex'] == 'F') & (md['Course Name'] == course) & (md['Completion Date'] >= str(start_date)) & (md['Completion Date'] <= str(end_date)) ]
        male_student = md[ (md['Sex'] == 'M') & (md['Course Name'] == course)]
        female_student = md[ (md['Sex'] == 'F') & (md['Course Name'] == course)]
        m = male_student['ID'].count()
        f = female_student['ID'].count()

        if [course,moduleName,m,f] not in df:
            df.insert(i, [course,moduleName,m,f])


    df = pd.DataFrame(df, columns = ['Course', 'Module Name', 'Male Student Enroll', 'Female Student Enroll'])
    return df