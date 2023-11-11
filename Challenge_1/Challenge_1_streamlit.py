import streamlit as st
import pandas as pd
import plotly.express as px

# Function to plot interactive line charts for EDA and BVP
def plot_interactive_line_charts(data, start_time_eda, end_time_eda, start_time_bvp, end_time_bvp):
    st.subheader('Interactive Line Charts')
    
    # Filter data for EDA based on time range
    filtered_data_eda = data[(data['Time'] >= start_time_eda) & (data['Time'] <= end_time_eda)]
    
    # Plot line chart for EDA
    fig_eda = px.line(filtered_data_eda, x='Time', y='EDA', title="Line Chart for EDA")
    fig_eda.update_layout(
        xaxis_title='Time',
        yaxis_title='EDA',
        showlegend=True
    )
    
    st.plotly_chart(fig_eda)

    # Filter data for BVP based on time range
    filtered_data_bvp = data[(data['Time'] >= start_time_bvp) & (data['Time'] <= end_time_bvp)]
    
    # Plot line chart for BVP
    fig_bvp = px.line(filtered_data_bvp, x='Time', y='BVP', title="Line Chart for BVP")
    fig_bvp.update_layout(
        xaxis_title='Time',
        yaxis_title='BVP',
        showlegend=True
    )
    
    st.plotly_chart(fig_bvp)

# Main Streamlit app
def main():
    st.title('Interactive Analysis between EDA and BVP')

    # Read data from CSV file
    csv_file_path = r"C:\Users\kosta\Downloads\df_result (1).csv"
    data = pd.read_csv(csv_file_path)

    # Convert 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])

    # Create tabs in the sidebar
    tab = st.sidebar.radio('Navigation', ['Tab 1', 'Tab 2', 'Tab 3'])

    if tab == 'Tab 1':
        # Define slider for interactivity - Line Charts
        st.subheader("Line Chart Configuration for EDA")
        start_time_line_eda = st.slider("Select Start Time - Line Chart (EDA)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].min().timestamp())
        end_time_line_eda = st.slider("Select End Time - Line Chart (EDA)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].max().timestamp())

        st.subheader("Line Chart Configuration for BVP")
        start_time_line_bvp = st.slider("Select Start Time - Line Chart (BVP)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].min().timestamp())
        end_time_line_bvp = st.slider("Select End Time - Line Chart (BVP)", min_value=data['Time'].min().timestamp(), max_value=data['Time'].max().timestamp(), value=data['Time'].max().timestamp())

        # Call function for interactive line charts
        plot_interactive_line_charts(data, pd.Timestamp(start_time_line_eda, unit='s'), pd.Timestamp(end_time_line_eda, unit='s'),
                                     pd.Timestamp(start_time_line_bvp, unit='s'), pd.Timestamp(end_time_line_bvp, unit='s'))

    elif tab == 'Tab 2':
        st.subheader('Food Consumption Tracker')
        food_consumed = st.text_input('Enter the Consumed Food:')
        calories_consumed = st.number_input('Enter the Calories Consumed:', min_value=0)

        st.write(f"You've consumed: {food_consumed} with {calories_consumed} calories.")
        
        # Add more content related to food consumption in Tab 2 as needed

    elif tab == 'Tab 3':
        st.write('Content for Tab 3')
        # Add content for Tab 3 as needed

if __name__ == '__main__':
    main()
