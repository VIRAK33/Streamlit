import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime
import module_config
import sidebar as side
import query as qr
import base64
from datetime import timedelta
from io import StringIO, BytesIO
import urllib.request

module_config.style()

sns.set_theme(style="darkgrid")

def download_csv(md):
    csv = md.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a style="float:left" href="data:file/csv;base64,{b64}">Download csv file</a>' 

    st.markdown(href, unsafe_allow_html=True)


def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = BytesIO()
	plt.savefig(buffered, format="jpg", bbox_inches='tight')
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a style="float:left" href="data:file/jpg;base64,{img_str}">Download Image</a>'
	return href

# st.title('Data Visualization')
data_file = st.file_uploader("Upload a file", type=("csv", "csv"))

if data_file is not None:
    st.sidebar.title('Data Visualization')
    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
    # st.write(file_details)
    df = pd.read_csv(data_file)
    df = df.rename(columns={'userid':'userid', 'username': 'ID', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'State', 'CompletionDate':'Completion Date'})
    df = df[(df.Group != 'test') & (df.Group != 'Channa') & (df.Group != 'RATHPISEY') & (df.Group != 'Daneth') & (df.Group != 'Sreylam') & (df.Group != 'Sinkeo')]
    
    md = df
    md['Year'] = md['Group'].apply(lambda x: x.split('-')[0])
    radio_select = st.sidebar.radio('Feature', ['Course', 'Student', 'Completion'])

    # Course = side.select_course(md)
    if radio_select == 'Course':
        option_course = ['All courses and students', 'Course Summary', 'Student Learning Progress',
                        'Recently active Students', 'Department Summary'
                        ]
        question = side.features(option_course)

        all_courses = md['Course Name'].unique()
        all_courses = np.insert(all_courses, 0, 'All', axis=0)

        # Select question 0 "All courses and students"
        if question == option_course[0]:
            course = st.selectbox(
                'Select course:',
                (all_courses)
            )
            col1,col2 = st.beta_columns(2)
            with col1:
                md = md[['ID', 'Student Name', 'Sex', 'Group', 'Department', 'Course Name', 'State', 'Completion Date']]

                if course == 'All':
                    st.dataframe(data=md, height=600)

                else:
                    md = md[md['Course Name'] == course ]
                    st.dataframe(data=md, height=600)
                
                download_csv(md)
                if course == 'All':
                    # st.markdown('<style>' + open('icons.css').read() + '</style>', unsafe_allow_html=True)
                    # st.markdown('<i class="material-icons">book</i>', unsafe_allow_html=True)
                    st.markdown('<b>Short Form:</b>', unsafe_allow_html=True)
                    st.markdown('- CCA: Climate Change and Adaptation')
                    st.write('- CC: Cover Crop')
                    st.write('- DAD: Database Analysis and Design')
                    st.write('- EG: Environmental Geology')
                    st.write('- FM: Food Microbiology')
                    st.write('- GT: Geodesy and Topography')
                    st.write('- IM: Image Processing')
                    st.write('- ICS: Introduction to Computer Science')
                    st.write('- NLP: Natural Language Processing')
                    st.write('- SE: Software Engineering')
                    st.write('- SM: Strength of Material')
                    st.write('- TS: Topographic Surveying')


            with col2:
                md = md.rename(columns={'userid':'ID', 'username': 'Student ID', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'Completion State', 'CompletionDate':'Completion Date'})
                md['CN']=df['Course Name'].map({'Climate Change and Adaptation':'CCA', 'Cover Crop':'CC',\
                    'Database Analysis and Design':'DAD', 'Environmental Geology':'EG',\
                    'Food Microbiology':'FM', 'Geodesy and Topography':'GT',\
                    'Geographic Information System and Remote Sensing':'GISRS',\
                    'Image Processing':'IM', 'Introduction to Computer Science':'ICS',\
                    'Natural Language Processing':'NLP', 'Software Engineering':'SE',\
                    'Strength of Material':'SM', 'Topographic Surveying':'TS'})
                if course == 'All':
                    totalRecord = md['Sex'].count()
                    if totalRecord > 0:
                        s = plt.figure(figsize=(7,8), dpi=250)
                        g = sns.countplot( y='CN',hue = 'Sex', data = md)
                        for p in g.patches:
                                percentage = '{:.0f}'.format(p.get_width())
                                x = p.get_x() + p.get_width() + 0.02
                                y = (p.get_y() + p.get_height()/2) + 0.15
                                g.annotate(percentage, (x, y))
                                
                        plt.title("Total of student access in each course")
                        plt.xlabel('Number of students enrolled')
                        plt.ylabel('Courses')
                        s
                        st.markdown(get_image_download_link(s), unsafe_allow_html=True)
                else:
                    totalRecord = md['Sex'].count()
                    if totalRecord > 0:
                        s = plt.figure(figsize=(7,8), dpi=250)
                        g = sns.countplot( x='CN',hue = 'Sex', data = md)
                        for p in g.patches:
                            percentage = '{:.0f}'.format(p.get_height())
                            x = (p.get_x() + p.get_width()/2)
                            y = (p.get_y() + p.get_height()) + 0.5
                            g.annotate(percentage, (x, y))
                                
                        plt.title("Total of student access in: "+ course)
                        plt.xlabel('Number of students')
                        plt.ylabel('Courses')
                        s
                        st.markdown(get_image_download_link(s), unsafe_allow_html=True)


            #Plot Graph_______
            # if course == 'All':
            

            #_______


        # Select question 1 "Course summary"
        if question == option_course[1]:
            course = st.selectbox('Select course:',all_courses)
            col1,col2 = st.beta_columns(2)
            md = qr.course_summary_(md)
            with col1:
                st.dataframe(data=md, height=600)
                # st.write(md)
                download_csv(md)

                st.markdown('<b>Short Form:</b>', unsafe_allow_html=True)
                st.markdown('- CCA: Climate Change and Adaptation')
                st.write('- CC: Cover Crop')
                st.write('- DAD: Database Analysis and Design')
                st.write('- EG: Environmental Geology')
                st.write('- FM: Food Microbiology')
                st.write('- GT: Geodesy and Topography')
                st.write('- IM: Image Processing')
                st.write('- ICS: Introduction to Computer Science')
                st.write('- NLP: Natural Language Processing')
                st.write('- SE: Software Engineering')
                st.write('- SM: Strength of Material')
                st.write('- TS: Topographic Surveying')

            with col2:
                    
                if course == 'All':
                    md =df
                    md = md.rename(columns={'userid':'ID', 'username': 'Username', 'firstname':'Student Name', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'State', 'CompletionDate':'Completion Date'})
                    
                    progress = md[(md['State'] == 1)]
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


                    # plt.figure(figsize=(10,10), dpi=250)
                    s = plt.figure(figsize=(8,7))

                    pro['CN']=pro['Course'].map({'Climate Change and Adaptation':'CCA', 'Cover Crop':'CC',\
                    'Database Analysis and Design':'DAD', 'Environmental Geology':'EG',\
                    'Food Microbiology':'FM', 'Geodesy and Topography':'GT',\
                    'Geographic Information System and Remote Sensing':'GISRS',\
                    'Image Processing':'IM', 'Introduction to Computer Science':'ICS',\
                    'Natural Language Processing':'NLP', 'Software Engineering':'SE',\
                    'Strength of Material':'SM', 'Topographic Surveying':'TS'})

                    g2 = sns.countplot(hue= "Sex",y="CN",  data=pro)

                    for p in g2.patches:
                            percentage = '{:.0f}'.format(p.get_width())
                            x = p.get_x() + p.get_width() + 0.02
                            y = (p.get_y() + p.get_height()/2) + 0.15
                            g2.annotate(percentage, (x, y))
                    
                    plt.yticks(rotation = 45)
                    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2)
                    plt.title("Number of students in each courses")
                    plt.xlabel('Number of students')
                    plt.ylabel('Courses')
                    st.write(s) 
                    plt.savefig('images/Number of students in each courses.png')
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)

                else:
                    md = qr.courseStudent(df,course)
                    totalRecord = md['Sex'].count()
                    if totalRecord > 0:
                        s = plt.figure(figsize=(8,7))
                        g2 = sns.countplot(x="Sex", data=md)

                        for p in g2.patches:
                                percentage = '{:.0f}'.format(p.get_height())
                                x = p.get_x() + p.get_width()/2
                                y = p.get_y() + p.get_height() + 0.4
                                g2.annotate(percentage, (x, y))
                                
                        plt.title("Number of students in: "+ course)
                        plt.xlabel('Gender')
                        plt.ylabel('Number of Students')
                        st.write(s) 
                        st.markdown(get_image_download_link(s), unsafe_allow_html=True)



        if question == option_course[2]:
            course = st.selectbox('Select course:',(md['Course Name'].unique()))
            col1,col2 = st.beta_columns(2)

            today = datetime.date.today()
            last14Day = today - timedelta(14)

            start = ''
            end = ''

            with col1:
                startDate = st.date_input("Start date", datetime.date(2020,9,1))
                # start = st.date_input("Start date",last14Day)

            with col2:
                endDate = st.date_input("End date", today)
            
            # startDate = str(start.month) + "/" + str(start.day) + '/' + str(start.year)
            # endDate = str(end.month) + "/" + str(end.day) + '/' + str(end.year)
            md = df

            progress = md[(md['Completion Date'] >= str(startDate)) & (md['Completion Date'] <= str(endDate)) & (md['Course Name'] == course)]



            # st.dataframe(data=a, height=600)
            

            arr = []
            for i in range(0, len(progress)):
                id = progress.iloc[i][1]
                name = progress.iloc[i][2]
                sex =  progress.iloc[i][3]
                course = progress.iloc[i][6]
                
                completed = progress[progress['Student Name'] == name].count()


                if [id, name, sex,course, completed[0]] not in arr:
                    arr.insert(i, [id, name, sex, course, completed[0]])
                    
            pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course', 'Completed'])
            pro.sort_values(by=['Student Name'], inplace=True)
            c1, c2 = st.beta_columns(2)
            with c1:
                st.dataframe(data=pro, height=600)
                download_csv(pro)
            with c2:
                import math
                maxLesson = pro['Completed'].max()
                totalRecord = pro['Completed'].count()
                if totalRecord > 0:
                    s = plt.figure(figsize=(10,totalRecord/3)) # 1 inch has 3 record
                    g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])

                    for p in g2.patches:
                        percentage = '{:.0f}'.format(p.get_width())

                        x = p.get_x() + p.get_width() + 0.02
                        y = (p.get_y() + p.get_height()/2) + 0.15
                        g2.annotate(percentage, (x, y))

                    x_ticks = np.arange(0, maxLesson + 1, 1)
                    plt.xticks(x_ticks)
                    plt.title("Student Learing Progress: "+ course)
                    plt.xlabel('Number of Completed Courses')
                    plt.ylabel('Student Name')
                    plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                    s
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)



        if question == option_course[3]:
            # st.write(df)
            course = st.selectbox('Select course:',(md['Course Name'].unique()))
            col1,col2 = st.beta_columns(2)

            today = datetime.date.today()
            last14Day = today - timedelta(14)

            with col1:
                # startDate = st.date_input('Start date', last14Day)
                startDate = st.date_input("Start date", datetime.date(2020,9,1))
            with col2:
                endDate = st.date_input('End date', today)

            md = df

            progress = md[(md['State'] == 1) & (md['Completion Date'] >= str(startDate)) & (md['Completion Date'] <= str(endDate)) & (md['Course Name'] == course)]

            arr = []
            for i in range(0, len(progress)):
                id = progress.iloc[i][1]
                name = progress.iloc[i][2]
                sex =  progress.iloc[i][3]
                course = progress.iloc[i][6]
                
                completed = progress[progress['Student Name'] == name].count()


                if [id, name, sex,course, completed[0]] not in arr:
                    arr.insert(i, [id, name, sex, course, completed[0]])
                    

            pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course', 'Completed'])
            pro.sort_values(by=['Student Name'], inplace=True)
            c1, c2 = st.beta_columns(2)
            with c1:
                
                st.dataframe(data=pro, height=600)
                download_csv(pro)
            with c2:
                totalRecord = pro['Completed'].count()
                maxLesson = pro['Completed'].max()
                if totalRecord > 0:

                    s = plt.figure(figsize=(10,totalRecord/3)) # 1 inch has 3 record
                    g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])

                    for p in g2.patches:
                        percentage = '{:.0f}'.format(p.get_width())

                        x = p.get_x() + p.get_width() + 0.02
                        y = (p.get_y() + p.get_height()/2) + 0.15
                        g2.annotate(percentage, (x, y))

                    x_ticks = np.arange(0, maxLesson + 1, 1)
                    plt.xticks(x_ticks)
                    plt.title("Recently Active Student with Learning Progress: "+ course)
                    plt.xlabel('Completed Courses')
                    plt.ylabel('Student Name')
                    plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                    s
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)



        if question == option_course[4]:
            data = md['Department'].unique()
            all_dep = np.insert(data, 0, 'All', axis=0)
            # department = ['GRU','GIC','GGG','GCA','GCI-GRU']
            department = st.selectbox('Select Department:',all_dep)

            if department == 'All':
                progress = md
            else:
                progress = md[md['Department']==department]

            

            md1, listStudentInDepartment = qr.listStudent(progress)
            md2 = qr.numberStudentEachCourse(md1)


            col1,col2 = st.beta_columns(2)
            with col1:
                md2.sort_values(by=['Year'], inplace=True)
                st.markdown('Number of students in each course:')
                st.dataframe(data=md2,height=600, width=553)
                download_csv(md2)

                year_group = md['Year'].unique()
                
                if (department != 'All'):
                    selectYear = ''
                    selectYear = st.selectbox('Select Group Student:',year_group)   
                    st.markdown('List active student')
                    today = datetime.date.today()
                    last14Day = today - timedelta(14)
                    
                    # startDate = st.date_input('Start date', last14Day)
                    startDate = st.date_input("Start date(last 14 days)", datetime.date(2020,9,1))

                    endDate = st.date_input('End date', today)

                    progress = md[(md['Department'] == department) & (md['Completion Date'] >= str(startDate)) & (md['Completion Date'] <= str(endDate)) & (md['Year'] == selectYear)]

                    arr = []
                    for i in range(0, len(progress)):
                        id = progress.iloc[i][1]
                        name = progress.iloc[i][2]
                        sex =  progress.iloc[i][3]
                        course = progress.iloc[i][6]
                        
                        completed = progress[progress['Student Name'] == name].count()


                        if [id, name, sex] not in arr:
                            arr.insert(i, [id, name, sex])
                            

                    pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex'])
                    pro.sort_values(by=['Student Name'], inplace=True)
                    st.dataframe(data=pro,height=600, width=553)
                    download_csv(pro)
                

            with col2:
                s = plt.figure(figsize=(10,8))
                if department == 'All':
                    g = sns.countplot( y='Department',hue = 'Sex', data = listStudentInDepartment)
                    for p in g.patches:
                        percentage = '{:.0f}'.format(p.get_width())
                        x = p.get_x() + p.get_width() + 0.08
                        y = (p.get_y() + p.get_height()/2) + 0.05
                        g.annotate(percentage, (x, y))
                    plt.title("Total student in each Department")
                    plt.xlabel('Number of Students')
                    plt.ylabel('Department')
                    plt.savefig('images/all department1.png', bbox_inches='tight')
                    s
                else:
                    g = sns.countplot( x='Department',hue = 'Sex', data = listStudentInDepartment)
                    for p in g.patches:
                            percentage = '{:.0f}'.format(p.get_height())
                            x = p.get_x() + p.get_width()/2
                            y = (p.get_y() + p.get_height()) + 0.05
                            g.annotate(percentage, (x, y))
                    plt.title("Total student in department "+ department)
                    plt.ylabel('Number of Students')
                    plt.xlabel('Department')
                    plt.savefig('images/all department1.png', bbox_inches='tight')
                    s

                st.markdown(get_image_download_link(s), unsafe_allow_html=True)  

                md = df





    if radio_select == 'Student':
        
        option_student = ['List Student in Department', 'Student Details']
        question = side.features(option_student)

        if question == option_student[0]:
            col1,col2 = st.beta_columns(2)
            with col1:
                data = md['Department'].unique()
                # all_dep = np.insert(data, 0, 'All', axis=0)
                # department = ['GRU','GIC','GGG','GCA','GCI-GRU']
                department = st.selectbox('Select Department:',data)

                if department == 'All':
                    progress = md
                else:
                    progress = md[md['Department']==department]

            
                md1, listStudentInDepartment = qr.listStudent(progress)
                md2 = qr.numberStudentEachCourse(md1)


                year_group = md['Year'].unique()
                # yearStudent = np.insert(year_group, 0, 'All', axis=0)

                # if department != 'All':
                selectYear = st.selectbox('Select Group Student:',year_group)    
                listStudentInDepartment.sort_values(by=['Student Name'], inplace=True)

                st.markdown('List students in '+ department + " department:")


                listStudentInDepartment = listStudentInDepartment[listStudentInDepartment['Year'] == selectYear]
                st.dataframe(data=listStudentInDepartment.style,height=600)

                download_csv(listStudentInDepartment)
            with col2:
                totalRecord = listStudentInDepartment['Year'].count()
                if totalRecord > 0:
                    s = plt.figure(figsize=(10,8))
                    g = sns.countplot( x='Department',hue = 'Sex', data = listStudentInDepartment)
                    for p in g.patches:
                        percentage = '{:.0f}'.format(p.get_height())
                        x = p.get_x() + p.get_width()/2
                        y = (p.get_y() + p.get_height()) + 0.05
                        g.annotate(percentage, (x, y))
                    plt.title("Total " + selectYear + " student in department "+ department)
                    plt.ylabel('Number of Students')
                    plt.xlabel('Department')
                    plt.savefig('images/all department1.png', bbox_inches='tight')
                    s

        if question == option_student[1]:
            col1, col2 = st.beta_columns(2)



            with col1:
                data = md['Department'].unique()
                # all_dep = np.insert(data, 0, 'All', axis=0)
                # department = ['GRU','GIC','GGG','GCA','GCI-GRU']
                department = st.selectbox('Select Department:',data)
                year_group = md['Year'].unique()
                selectYear = st.selectbox('Select Group Student:',year_group)  

                studentData = md[(md['Department']==department) & (md['Year'] == selectYear)]
                student = studentData['Student Name'].unique()
                selectStudent = st.selectbox('Select Student: ', student)
            
                # md1, listStudentInDepartment = qr.listStudent(student)
                # md2 = qr.numberStudentEachCourse(md1)
                # md1
                md = qr.studentDetail(md, selectStudent)
                
                st.dataframe(data=md, height=600)
                download_csv(md)
            
            with col2:

                maxLesson = md['Total Completed'].max()
                totalRecord = md['Total Completed'].count()
                if totalRecord > 0:
                    s = plt.figure(figsize=(7,8)) # 1 inch has 3 record
                    g2 = sns.barplot(x=md['Course'], y= md['Total Completed'])

                    for p in g2.patches:
                        percentage = '{:.0f}'.format(p.get_height())

                        x = p.get_x() + p.get_width()/2
                        y = (p.get_y() + p.get_height() + 0.02)
                        g2.annotate(percentage, (x, y))


                    plt.title("The Completed Lesson in each Course")
                    plt.xlabel('Courses')
                    plt.ylabel('Number of completed')
                    x_ticks = np.arange(0, maxLesson + 1, 1)
                    plt.yticks(x_ticks)
                    plt.savefig('images/Students/'+'The Completed Lesson in each Course.png', bbox_inches='tight')
                    s
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)



                



    if radio_select == 'Completion':
        option_completion = ['Courses Completion Summary']
        question = side.features(option_completion)

        if question == option_completion[0]:

                        
            c1, c2, c3= st.beta_columns(3)

            data = md['Department'].unique()
            # all_dep = np.insert(data, 0, 'All', axis=0)
            # department = ['GRU','GIC','GGG','GCA','GCI-GRU']
            with c1:
                department = st.selectbox('Select Department:',data)
                md = md[md['Department'] == department]
            with c2:
                courses = md['Course Name'].unique()
                course = st.selectbox('Select Course:', courses)

            totalCompleted = c3.number_input('Total Minimum Completed', value=1)
            progress = md[(md['Course Name'] == course)]



            # st.dataframe(data=a, height=600)
            

            arr = []
            for i in range(0, len(progress)):
                id = progress.iloc[i][1]
                name = progress.iloc[i][2]
                sex =  progress.iloc[i][3]
                course = progress.iloc[i][6]
                
                completed = progress[progress['Student Name'] == name].count()


                if [id, name, sex,course, completed[0]] not in arr:
                    arr.insert(i, [id, name, sex, course, completed[0]])
                    
            pro = pd.DataFrame(arr, columns = ['ID', 'Student Name', 'Sex', 'Course', 'Completed'])
            pro.sort_values(by=['Student Name'], inplace=True)

            col1, col2 = st.beta_columns(2)

            with col1:
                pro = pro[pro['Completed'] >= totalCompleted]
                st.dataframe(data=pro, height=600)

                download_csv(pro)
            with col2:

                import math
                maxLesson = pro['Completed'].max()
                totalRecord = pro['Completed'].count()
                if totalRecord > 0:
                    s = plt.figure(figsize=(10,totalRecord/3)) # 1 inch has 3 record
                    g2 = sns.barplot(y=pro['Student Name'], x= pro['Completed'])

                    for p in g2.patches:
                        percentage = '{:.0f}'.format(p.get_width())

                        x = p.get_x() + p.get_width() + 0.02
                        y = (p.get_y() + p.get_height()/2) + 0.15
                        g2.annotate(percentage, (x, y))

                    x_ticks = np.arange(0, maxLesson + 1, 1)
                    plt.xticks(x_ticks)
                    plt.title("Student Learing Progress: "+ course)
                    plt.xlabel('Number of Completed Courses')
                    plt.ylabel('Student Name')
                    plt.savefig('images/Student Learning Proress/'+ str(i) +'.png', bbox_inches='tight')
                    s
                    st.markdown(get_image_download_link(s), unsafe_allow_html=True)

            
