import streamlit as st
import pandas as pd
import plotly.express as px


def plot_interactive_bar_chart_HR():
    
    df_hr =pd.read_csv(r'C:\Users\kosta\streamlit\new data files for final show moment\hr\df_all_hr.csv', header=0)
    
    category_labels = ['Low', 'Mid', 'High']
   
    num_categories = 3
    
    hr_min = df_hr['HR'].min()
    hr_max = df_hr['HR'].max()
    
    thresholds = [hr_min]
    thresholds.extend([hr_min + (i + 1) * ((hr_max - hr_min) / num_categories) for i in range(num_categories - 1)])
    thresholds.append(hr_max)

    categories = pd.cut(df_hr['HR'], bins=thresholds, labels=category_labels)

    category_counts = categories.value_counts().reindex(category_labels, fill_value=0)

    df_counts = pd.DataFrame({'Categories': category_counts.index, 'Counts': category_counts.values})

    fig_hr = px.bar(df_counts, x='Categories', y=[thresholds[i + 1] - thresholds[i] for i in range(num_categories)], base=thresholds[:-1], title="Overall HR Data")
    
    fig_hr.update_traces(
        hoverinfo='y',
        hovertemplate='Threshold: %{y}'
    )

    fig_hr.update_layout(
        xaxis_title='Categories',
        yaxis_title='Thresholds',
        showlegend=False
    )

    st.plotly_chart(fig_hr)
    
def plot_interactive_bar_chart_EDA():
    
    df_eda =pd.read_csv(r'C:\Users\kosta\streamlit\new data files for final show moment\eda\df_all_eda.csv', header=0)
    
    category_labels = ['Low', 'Mid', 'High']
 
    num_categories = 3
    
    eda_min = df_eda['EDA'].min()
    eda_max = df_eda['EDA'].max()
    
    thresholds = [eda_min]
    thresholds.extend([eda_min + (i + 1) * ((eda_max - eda_min) / num_categories) for i in range(num_categories - 1)])
    thresholds.append(eda_max)

    categories = pd.cut(df_eda['EDA'], bins=thresholds, labels=category_labels)

    category_counts = categories.value_counts().reindex(category_labels, fill_value=0)

    df_counts = pd.DataFrame({'Categories': category_counts.index, 'Counts': category_counts.values})

    fig_eda = px.bar(df_counts, x='Categories', y=[thresholds[i + 1] - thresholds[i] for i in range(num_categories)], base=thresholds[:-1], title="Overall EDA Data")
    
    fig_eda.update_traces(
        hoverinfo='y',
        hovertemplate='Threshold: %{y}'
    )

    fig_eda.update_layout(
        xaxis_title='Categories',
        yaxis_title='Thresholds',
        showlegend=False
    )

    st.plotly_chart(fig_eda)
    
def plot_interactive_line_charts(data, start_time_eda, end_time_eda, start_time_hr, end_time_hr):
    
    filtered_data_eda = data[(data['Time'] >= start_time_eda) & (data['Time'] <= end_time_eda)]

    fig_eda = px.line(filtered_data_eda, x='Time', y='EDA', title="Line Chart for EDA")
    fig_eda.update_layout(
        xaxis_title='Time',
        yaxis_title='EDA',
        showlegend=True
    )
    
    st.plotly_chart(fig_eda)
    plot_interactive_bar_chart_EDA()

    filtered_data_hr = data[(data['Time'] >= start_time_hr) & (data['Time'] <= end_time_hr)]
    
    fig_hr = px.line(filtered_data_hr, x='Time', y='HR', title="Line Chart for HR")
    fig_hr.update_layout(
        xaxis_title='Time',
        yaxis_title='HR',
        showlegend=True
    )
    
    st.plotly_chart(fig_hr)
    plot_interactive_bar_chart_HR()
    
def homepage(mean_calorie, mean_weight, health_data=None):
    st.subheader("Welcome to the Homepage!")
    st.write(f"Average Calorie Intake: {mean_calorie} calories")
    st.write(f"Average Weight: {mean_weight} kg")

    if health_data:
        st.subheader("Health Information")
        
        df_health_data = pd.DataFrame(health_data).T.reset_index()
        df_health_data.columns = ['Date', 'Calories', 'Weight']

        df_health_data['Date'] = pd.to_datetime(df_health_data['Date']).dt.date
        st.dataframe(df_health_data)

def popup():
    st.subheader("Health Information")
    
    selected_dates = st.multiselect("Select dates:", pd.date_range(start='2023-11-25', end='2023-12-31'))

    for date in selected_dates:
        st.write(f"Date: {date}")
        calorie_input = st.number_input("Enter your daily calorie intake:", min_value=0)
        weight_input = st.number_input("Enter your weight (in kg):", min_value=0)

        if st.button("Saved"):
           
            if 'health_data' not in st.session_state:
                st.session_state.health_data = {}

            st.session_state.health_data[date] = {'calories': calorie_input, 'weight': weight_input}

            st.success("Health information saved!")
            
def render_homepage():
    mean_calorie = mean_weight = 0
    health_data = getattr(st.session_state, 'health_data', {})

    if health_data:
        all_calories = [data['calories'] for data in health_data.values()]
        all_weights = [data['weight'] for data in health_data.values()]
        mean_calorie = sum(all_calories) / len(all_calories)
        mean_weight = sum(all_weights) / len(all_weights)

    homepage(mean_calorie, mean_weight, health_data)

def render_health():
    popup()

def render_gym():
    plot_interactive_bar_chart_HR()
    plot_interactive_bar_chart_EDA()
    
def main():
    
    
    # Read data from CSV file
    csv_file_path = r'C:\Users\kosta\streamlit\new data files for final show moment\result\df_result.csv'
    data = pd.read_csv(csv_file_path)

   # Convert 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])
   
    st.set_page_config(page_title="Health App", layout="wide")

    tabs = ["Homepage", "Health", "Gym"]
    tab_labels = ["Home", "Health", "Gym"]

    current_tab_index = st.sidebar.selectbox("Navigation", range(len(tabs)), format_func=lambda i: tab_labels[i])

    current_tab = tabs[current_tab_index]

    if current_tab == "Homepage":

        mean_calorie = mean_weight = 0
        health_data = getattr(st.session_state, 'health_data', {})
        
        if health_data:
            all_calories = [data['calories'] for data in health_data.values()]
            all_weights = [data['weight'] for data in health_data.values()]
            mean_calorie = sum(all_calories) / len(all_calories)
            mean_weight = sum(all_weights) / len(all_weights)

        homepage(mean_calorie, mean_weight, health_data)
    elif current_tab == "Health":
        popup()
    elif current_tab == "Gym":
        plot_interactive_line_charts(data, data['Time'].min(), data['Time'].max(), data['Time'].min(), data['Time'].max())

if __name__ == "__main__":
    main()
