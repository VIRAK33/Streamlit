import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime
import module_config


module_config.style()
st.title('Data Visualization')

data_file = st.file_uploader("Upload a file", type=("csv", "csv"))
if data_file is not None:

    file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
    # st.write(file_details)
    md = pd.read_csv(data_file)
    md = md.rename(columns={'userid':'ID', 'username': 'Username', 'firstname':'Firstname', 'phone1':'Sex', 'department':'Department', 'lastname':'Group', 'courseName':'Course Name', 'moduleName':'Module Name', 'completionstate': 'Completion State', 'CompletionDate':'Completion Date'})
    

    radio_select = st.sidebar.radio('Feature', ['Course', 'Student', 'Complation'])


    def select_course():
        course = st.sidebar.selectbox(
            'Select course:',
            (md['Course Name'].unique())
        )
        return course
    def duration():
        start_date = st.sidebar.date_input('Start date', datetime.date(2020,10,1))
        end_date = st.sidebar.date_input('End date', datetime.date(2020,11,1))
        return start_date, end_date

# st.pyplot()
    if radio_select == 'Course':

        course = select_course()

        # features = st.sidebar.selectbox('Select Feature',('Course', 'Student', 'Completion') )
        # sns.countplot(y="cn", hue = 'phone1', data=md)
        # st.write(features)
        start_date, end_date = duration()


        gic_st = md[ (md['Course Name'] == course) & (md['Completion Date'] > str(start_date)) & (md['Completion Date'] < str(end_date))]
        df1 = gic_st.groupby(['Course Name','Firstname']).count()
        
        st.dataframe(df1)


        # df2 = df1['courseName'], df1['firstname']
        st.write('Show all courses and all students in each course')

        df2 = md.groupby(['Course Name','Module Name','Sex']).count()
        st.dataframe(df2)


        def course_info():
            st.write('Give a summary info for each course (type of course material scorm or html/resource?, how many students enrolled? how many female and male?, how many are active during time t1 to t2?)')
            
            col1,col2 = st.beta_columns(2)

            today = datetime.date.today()

            with col1:
                start_date = st.date_input('Start date', datetime.date(2020,9,1))
            with col2:
                end_date = st.date_input('End date', today)


            df = []
            for i in range(0, len(md)):
                course = md.iloc[i][6]
                moduleName = md.iloc[i][7]
                male_student = md[ (md['Sex'] == 'M') & (md['Course Name'] == course) & (md['Completion Date'] >= str(start_date)) & (md['Completion Date'] <= str(end_date))]
                female_student = md[ (md['Sex'] == 'F') & (md['Course Name'] == course) & (md['Completion Date'] >= str(start_date)) & (md['Completion Date'] <= str(end_date)) ]
                
                m = male_student['ID'].count()
                f = female_student['ID'].count()
                
                if [course,moduleName,m,f] not in df:
                    df.insert(i, [course,moduleName,m,f])


            df = pd.DataFrame(df, columns = ['Course', 'Module Name', 'Male', 'Female'])
            c = md['Course Name'].unique()
            a = np.append(c, 'All')
            a.sort()
            course_ = st.selectbox('Select course name:',(a) )
            if course_ == 'All':
                st.dataframe(df)
            else:
                df = df[(df['Course'] == course_)]
                st.dataframe(df)
        
        course_info()

