import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

current_tab = 'Homepage'

def plot_interactive_bar_chart_EDA():
    
    df = pd.read_csv(r"C:\Users\kosta\streamlit\Exporting_data_file\11-11-2023 18h22m18s\df_eda.csv")

    filtered_df = df[df['EDA'] >= 1]
    
    bins = [0.5, 4, 8, float('inf')]
    labels = ['Low', 'Medium', 'High']
    
    filtered_df['Category'] = pd.cut(filtered_df['EDA'], bins=bins, labels=labels, right=False)

    grouped_df = filtered_df.groupby(['Category', 'EDA']).size().reset_index(name='Count')
   
    median_value = filtered_df['EDA'].median()
    mean_value = filtered_df['EDA'].mean()
    mode_value = filtered_df['EDA'].mode().iloc[0]  

    chart = alt.Chart(grouped_df).mark_bar().encode(
        x='EDA:Q',
        y='Count:Q',
        color='Category:N',
        tooltip=['Category:N', 'EDA:Q', 'Count:Q']
    )

    chart = chart + \
        alt.Chart(pd.DataFrame({'value': [mean_value]})).mark_rule(color='red').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [median_value]})).mark_rule(color='green').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [mode_value]})).mark_rule(color='blue').encode(x='value:Q', size=alt.value(2))

    st.altair_chart(chart, use_container_width=True)
    
def plot_interactive_bar_chart_BVP():
    
    df = pd.read_csv(r"C:\Users\kosta\streamlit\Exporting_data_file\11-11-2023 18h11m22s\df_bvp.csv")
    
    filtered_df = df[(df['BVP'] >= 2) & (df['BVP'] <= 260)]

    bins = [ 1.5, 4, 8, 500]
    labels = [ 'Low', 'Medium', 'High']

    filtered_df['Category'] = pd.cut(filtered_df['BVP'], bins=bins, labels=labels, right=False)

    grouped_df = filtered_df.groupby(['Category', 'BVP']).size().reset_index(name='Count')
   
    median_value = filtered_df['BVP'].median()
    mean_value = filtered_df['BVP'].mean()
    mode_value = filtered_df['BVP'].mode().iloc[0]  

    chart = alt.Chart(grouped_df).mark_bar().encode(
        x='BVP:Q',
        y='Count:Q',
        color='Category:N',
        tooltip=['Category:N', 'BVP:Q', 'Count:Q']
    )

    chart = chart + \
        alt.Chart(pd.DataFrame({'value': [mean_value]})).mark_rule(color='red').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [median_value]})).mark_rule(color='green').encode(x='value:Q', size=alt.value(2)) + \
        alt.Chart(pd.DataFrame({'value': [mode_value]})).mark_rule(color='blue').encode(x='value:Q', size=alt.value(2))

    st.altair_chart(chart, use_container_width=True)
    
def plot_interactive_line_charts(data, start_time_eda, end_time_eda, start_time_bvp, end_time_bvp):
    st.subheader('Interactive Line Charts')
    
    filtered_data_eda = data[(data['Time'] >= start_time_eda) & (data['Time'] <= end_time_eda)]
    
    fig_eda = px.line(filtered_data_eda, x='Time', y='EDA', title="Line Chart for EDA")
    fig_eda.update_layout(
        xaxis_title='Time',
        yaxis_title='EDA',
        showlegend=True
    )
    
    st.plotly_chart(fig_eda)
    plot_interactive_bar_chart_EDA()

    filtered_data_bvp = data[(data['Time'] >= start_time_bvp) & (data['Time'] <= end_time_bvp)]
    
    fig_bvp = px.line(filtered_data_bvp, x='Time', y='BVP', title="Line Chart for BVP")
    fig_bvp.update_layout(
        xaxis_title='Time',
        yaxis_title='BVP',
        showlegend=True
    )
    
    st.plotly_chart(fig_bvp)
    plot_interactive_bar_chart_BVP()

def manage_food_history():
    st.subheader('Food Consumption Tracker')

    if 'food_history' not in st.session_state:
        st.session_state.food_history = pd.DataFrame(columns=['Datetime', 'Food', 'Calories'])
    
    food_consumed = st.text_input('Enter the Consumed Food:')
    calories_consumed = st.number_input('Enter the Calories Consumed:', min_value=0)
    
    if st.button('Add to History'):
        current_datetime = pd.Timestamp.now()
        st.session_state.food_history = st.session_state.food_history.append({'Datetime': current_datetime, 'Food': food_consumed, 'Calories': calories_consumed}, ignore_index=True)
        st.success(f"Added: {food_consumed} with {calories_consumed} calories at {current_datetime} to the history.")

    with st.expander("Food Consumption History"):
        st.write(st.session_state.food_history)

    st.subheader('Average Weekly Calorie Consumption')
    st.session_state.food_history['Datetime'] = pd.to_datetime(st.session_state.food_history['Datetime'])
    weekly_calories_user = st.session_state.food_history.set_index('Datetime').resample('W-Mon')['Calories'].sum()
    average_weekly_calories_user = weekly_calories_user.mean()
    st.write(f'The average weekly calorie consumption based on user inputs is: {average_weekly_calories_user:.2f} calories.')

    weekly_calories_total = st.session_state.food_history.resample('W-Mon', on='Datetime')['Calories'].sum()
    average_weekly_calories_total = weekly_calories_total.mean()
    st.write(f'The average weekly calorie consumption for the entire history is: {average_weekly_calories_total:.2f} calories.')

def main():
    global current_tab

    csv_file_path = r"C:\Users\kosta\streamlit\Exporting_data_file\11-11-2023 14h46m51s\df_result.csv"
    data = pd.read_csv(csv_file_path)

    data['Time'] = pd.to_datetime(data['Time'])

    tab = st.experimental_get_query_params().get("tab", ["Homepage"])[0]
    current_tab = tab

    if st.button("Homepage"):
         current_tab = 'Homepage'
         st.experimental_set_query_params(tab=current_tab)
         homepage_content()
    
    elif st.button("Gym"):
         current_tab = 'Gym'
         st.experimental_set_query_params(tab=current_tab)
         gym_content(data)
    
    elif st.button("Health"):
         current_tab = 'Health'
         st.experimental_set_query_params(tab=current_tab)
         health_content()
    
    elif st.button("Pop-up"):
         current_tab = 'Pop-up'
         st.experimental_set_query_params(tab=current_tab)
         popup_content()
         
@st.cache_resource(experimental_allow_widgets=True)
def homepage_content():
    
    st.write('With our app you can see the data related to EDA and BVP while keeping a track of your calories and weight!')
    st.divider()
    st.write('The EDA stands for Electrodermal activity. EDA is used to measure the conductance of the skin, also known as sweat.')
    st.write(' The BVP stands for blood volume pulse. The BVP is used as a method to measure heartbeats by measuring the volume of blood that flows through the arteries where the sensor is placed, the E4 empathica wristband.')
    
    st.divider()
    st.write('Average weekly calorie consumption(measured by last 7 inputs in dataframe): 123')
    st.write('Average weekly weight(measured by last 7 inputs in dataframe): 123')
    st.divider()

    calendar = pd.DataFrame(index=['Week 1','Week 2','Week 3', 'Week 4'], columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    st.write(calendar)

@st.cache_resource(experimental_allow_widgets=True)
def gym_content(data):
    st.write('This is the gym content.')

    plot_interactive_line_charts(data, data['Time'].min(), data['Time'].max(), data['Time'].min(), data['Time'].max())

@st.cache_resource(experimental_allow_widgets=True)
def health_content():
    st.write('This is the health content.')
    
    calorie = pd.DataFrame(index=['Input values:'], columns=['Your calorie intake on Monday was : 1', 'Your calorie intake on Tuesday was : 2', 'Your calorie intake on Wednesday was : 3',
    'Your calorie intake on Thursday was : 4', 'Your calorie intake on Friday was : 5', 'Your calorie intake on Saturday was : 6', 'Your calorie intake on Sunday was : 7'])

    weight = pd.DataFrame(index=['Input values'], columns=['Your weight on Monday was : ', 'Your weight on Tuesday was : ', 'Your weight on Wednesday was : ',
    'Your weight on Thursday was : ', 'Your weight on Friday was : ', 'Your weight on Saturday was : ', 'Your weight on Sunday was : '])
    
    st.write(calorie, 'Average calorie consumption for your week was : ')
    
    st.write(weight, 'Avegare weight for your week was : ')

@st.cache_resource(experimental_allow_widgets=True)
def popup_content():
    st.write('This is the pop-up content.')
        
if __name__ == '__main__':
    main()
