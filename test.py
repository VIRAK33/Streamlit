
import pandas as pd
import numpy as np

md = pd.read_csv('moodleitcdata.csv')

md = md.rename(columns={'userid':'ID', 'username': 'Username', 'firstname':'Firstname', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'Completion State', 'CompletionDate':'Completion Date'})

list = [['Climate Change and Adaptation', 'resource'],
 ['Cover Crop', 'scorm'],
 ['Database Analysis and Design', 'scorm'],
 ['Environmental Geology', 'scorm'],
 ['Food Microbiology', 'scorm'],
 ['Geodesy and Topography', 'resource'],
 ['Geographic Information System and Remote Sensing', 'scorm'],
 ['Image Processing', 'resource'],
 ['Image Processing', 'scorm'],
 ['Introduction to Computer Science', 'scorm'],
 ['Natural Language Processing', 'resource'],
 ['Software Engineering', 'scorm'],
 ['Strength of Material', 'resource'],
 ['Topographic Surveying', 'scorm']]

numpy_arr = np.array(list)
df = pd.DataFrame(numpy_arr)


# print('Type: \t\tModule name')
# for i in list:
#     for course in i:
#         print(course + ":\t\t", end =" ")
        
#     print()

# print(df)

# course = []
# for i in range(0, len(md)):
#     if [md.iloc[i][6],md.iloc[i][7]] not in course:
#         course.insert(i, [md.iloc[i][6], md.iloc[i][7]])
# print(course)

df = []

for i in range(0, len(md)):
    course = md.iloc[i][6]
    moduleName = md.iloc[i][7]
    male_student = md[ (md['Sex'] == 'M') & (md['Course Name'] == course) ]
    female_student = md[ (md['Sex'] == 'F') & (md['Course Name'] == course) ]
    
    m = male_student['ID'].count()
    f = female_student['ID'].count()
    
    if [course,moduleName,m,f] not in df:
        df.insert(i, [course,moduleName,m,f])
# print(df)

df = pd.DataFrame(df, columns = ['Course', 'Module Name', 'Male', 'Female'])
print(df)

