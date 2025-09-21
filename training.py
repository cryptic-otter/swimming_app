import pandas as pd
import streamlit as st
import datetime as dt
import math

#Load data
def load_data():
    ldf=pd.read_excel("SwimmingMarathonTraining.xlsx",sheet_name="Sheet1")
    ldf["Date"]=ldf["Date"].dt.date#Convert Date column
    ldf["Strength Training"]=ldf["Strength Training"].fillna("False")
    ldf["Strength Training Performed"]=ldf["Strength Training Performed"].fillna("False")
    return ldf

#Initialize Data and static variables
if "training_df" not in st.session_state:
    st.session_state.training_df=load_data()

training_df=st.session_state.training_df
today_date=dt.date.today()
day_of_week=today_date.weekday()
if day_of_week!=6:
    day_of_week_delta=-1-day_of_week
else:
    day_of_week_delta=0
start_day=today_date+dt.timedelta(day_of_week_delta)
end_day=today_date+dt.timedelta(day_of_week_delta+6)

start_day_index=training_df.index[training_df["Date"]==start_day].to_list()[0]
end_day_index=training_df.index[training_df["Date"]==end_day].to_list()[0]
today_index=training_df.index[training_df["Date"]==today_date].to_list()[0]

#---------------------------------------------------------------------------------------------------------------------------------------------------
#General Info and Page setup
training_input=st.sidebar.button("Traning Log Form")
st.markdown("<h1><u>Nick's Swimming Dashboard</u></h1>",unsafe_allow_html=True)
st.markdown("<h2 style='text-align:left'>Date: "+str(today_date)+"</h2>", unsafe_allow_html=True)

st.divider()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Weekly Breakdown
def weekly_style(row):
    if (row["Date"] == dt.date.today()) & (pd.isna(row["Pace"])==True):  # condition create green for performed exercise, red for missed
        return ["background-color: red"] * len(row)
    elif (row["Date"] == dt.date.today()) & (pd.isna(row["Pace"])==False):
        return ["background-color: green"] * len(row)
    else:
        return [""] * len(row)

st.markdown("<h2 style='text-align:left'>Weekly Breakdown</h2>",unsafe_allow_html=True)
st.markdown("<h3 style='text-align:left'>Workouts This Week</h3>",unsafe_allow_html=True)

weekly_df=pd.DataFrame(training_df.loc[start_day_index:end_day_index][["Date","Day","Swim Distance (m)","Type","Pace","Strength Training Performed"]])#Adjust to be dynamic for weekly review (Sun-Sat)
styled_df = weekly_df.style.apply(weekly_style, axis=1)
st.dataframe(styled_df,hide_index=True)

st.markdown("<h3 style='text-align:left'>Week in Review</h3>",unsafe_allow_html=True)
weeklyreview_df=pd.DataFrame(training_df.loc[0:6][["Date","Day","Swim Distance (m)","Heart Rate", "Pace"]])#Adjust to be dynamic for weekly review (Sun-Sat)
st.dataframe(weeklyreview_df,hide_index=True)

st.divider()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
#Today and on deck exercises
#During debugging don't forget last day of training will throw an error

#Today and On Deck Exercises - Improvement could be the ability to scroll across days
wb_col1, wb_col2=st.columns(2)
with wb_col1:
    st.markdown("<h2 style='text-align:Center'>Today's Swim</h2>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h5 style='text-align:left'>Distance: "+ str(training_df.loc[training_df["Date"]==today_date,"Swim Distance (m)"].values[0])+ " m</h5>",unsafe_allow_html=True)
        st.markdown("<h5 style='text-align:left'>Type: "+ str(training_df.loc[training_df["Date"]==today_date,"Run"].values[0])+ "</h5>",unsafe_allow_html=True)
        st.markdown("<h5 style='text-align:left'>Strength Training: "+ str(training_df.loc[training_df["Date"]==today_date,"Strength Training"].values[0])+ "</h5>",unsafe_allow_html=True)
with wb_col2:
    st.markdown("<h2 style='text-align:Center'>Tomorrow's Swim</h2>",unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h5 style='text-align:left'>Distance: "+ str(training_df.loc[training_df["Date"]==today_date+dt.timedelta(1),"Swim Distance (m)"].values[0])+ " m</h5>",unsafe_allow_html=True)
        st.markdown("<h5 style='text-align:left'>Type: "+ str(training_df.loc[training_df["Date"]==today_date+dt.timedelta(1),"Run"].values[0])+ "</h5>",unsafe_allow_html=True)
        st.markdown("<h5 style='text-align:left'>Strength Training: "+ str(training_df.loc[training_df["Date"]==today_date+dt.timedelta(1),"Strength Training"].values[0])+ "</h5>",unsafe_allow_html=True)

#Form to Fillout
def write_data(tdf,p,hr,iv,ep,tt,w,s,n,ad):
    tdf.loc[iv,["Pace"]]=p
    tdf.loc[iv,["Heart Rate"]]=hr
    tdf.loc[iv,["Strength Training Performed"]]=ep
    tdf.loc[iv,["Total Time (min)"]]=tt
    tdf.loc[iv,["Weight"]]=w
    tdf.loc[iv,["SWOLF"]]=s
    tdf.loc[iv,["Notes"]]=n
    tdf.loc[iv,["Actual Distance (m)"]]=ad
    tdf.to_excel("SwimmingMarathonTraining.xlsx",sheet_name="Sheet1",index=False)

with st.container(border=True):
    st.markdown("<h3 style='text-align: center'> Training Input Form</h3>",unsafe_allow_html=True)
    date_select=st.selectbox("Select a Date",training_df["Date"],today_index)
    col1_f,col2_f=st.columns([2,2])
    with col1_f:
        pcolh,pcol_colon1,pcolmin,pcol_colon2,pcolsec=st.columns([6,1,6,1,6])
        with pcolh:
            hours=st.number_input("Total Time:",placeholder="h")
        with pcol_colon1:
            st.write("")
            st.write("")
            st.write(":")
        with pcolmin:
            mins=st.number_input("minutes",label_visibility="hidden",placeholder="mm")
        with pcol_colon2:
            st.write("")
            st.write("")
            st.write(":")
        with pcolsec:
            sec=st.number_input("seconds",label_visibility="hidden",placeholder="ss")
        weight=st.number_input("Weight:")
        actual_distance=st.number_input("Distance Swam",placeholder=str(training_df.loc[today_index,"Swim Distance (m)"]))
        
        #Convert Pace to minutes and text string
        #Fix to ingest as text string
        total_time=hours*60+mins+sec/60
        pace_min=round(math.modf((int(hours)*60+int(mins)+int(sec)/60)/training_df.loc[training_df["Date"]==date_select,["Swim Distance (m)"]].values[0][0]*100)[1])
        pace_sec=round(60*math.modf((int(hours)*60+int(mins)+int(sec)/60)/training_df.loc[training_df["Date"]==date_select,["Swim Distance (m)"]].values[0][0]*100)[0])
        pace=pace_min+pace_sec/60
        if pace_sec<10:
            pace_sec_str=str("0"+str(pace_sec))
        else:
            pace_sec_str=str(pace_sec)
        # pace_sec=str(round(math.modf(pace)[1])) + ":" + str(round(math.modf(pace)[0],2)*60)
        if training_df.loc[training_df["Date"]==date_select,["Strength Training"]].values[0][0]!="None":
            exercise_performed=st.checkbox("Exercise Completed",disabled=False)
        else:
            exercise_performed=st.checkbox("Strength Training Performed",disabled=True) 
    with col2_f:
        heart_rate=st.number_input("Heart Rate:")
        swolf=st.number_input("SWOLF:")
    notes=st.text_area("Notes:")
    col1_f,col2_f,col3_f=st.columns([2,1,2])
    with col1_f:
        submitted=st.button("Submit")
    
    #Append info to excel file
    if submitted:
        index_value = training_df.index[training_df["Date"]==date_select].values[:][0]
        write_data(training_df, pace, heart_rate, index_value, exercise_performed, total_time,weight,swolf,notes,actual_distance)
        st.session_state.training_df = load_data()   # rehydrate from disk if you want
        st.rerun()


if submitted:
    st.markdown("<h4 style='text-align:left'>Training Logged!</h4>",unsafe_allow_html=True)

#Edit Training Data
# st.divider()      
# st.markdown("<h2>Edit Data</h2>",unsafe_allow_html=True)
# cols_to_edit=["Date","Swim Distance (m)","Pace","Strength Training Performed","Heart Rate"]
# st.data_editor(training_df[cols_to_edit],hide_index=True)
# edit_data=st.button("Update Data")

# if edit_data:

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#Visual Dashboard
# dates=dict(range=["2025-09-21",dt.date.today()+dt.timedelta(4)])
# lc_fig=px.line(training_df,"Date","SWOLF")
# lc_fig.update_layout(
#     xaxis=dict(range=["2025-09-21",dt.date.today()+dt.timedelta(4)])
# )
# st.plotly_chart(lc_fig)