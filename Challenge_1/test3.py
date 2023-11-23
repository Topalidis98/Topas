import streamlit as st
import pandas as pd
import altair as alt

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
    
def homepage(mean_calorie, mean_weight):
    st.write("Welcome to the Homepage!")
    st.subheader("Mean Health Information")
    st.write(f"Mean Calorie Intake: {mean_calorie} calories")
    st.write(f"Mean Weight: {mean_weight} kg")

def health():
    st.subheader("Health Information")
    calorie_input = st.number_input("Enter your daily calorie intake:", min_value=0)
    weight_input = st.number_input("Enter your weight (in kg):", min_value=0)

    if st.button("Save Health Information"):
        # Initialize lists in session state if not present
        if 'calories' not in st.session_state:
            st.session_state.calories = []
        if 'weights' not in st.session_state:
            st.session_state.weights = []

        # Store the health information in lists
        st.session_state.calories.append(calorie_input)
        st.session_state.weights.append(weight_input)

        st.success("Health information saved!")

def main():
    st.set_page_config(page_title="Health App", layout="wide")

    tabs = ["Homepage", "Health", "Gym"]
    current_tab = st.sidebar.radio("Navigation", tabs)

    if current_tab == "Homepage":
        # Calculate mean of stored values
        mean_calorie = mean_weight = 0
        if hasattr(st.session_state, 'calories') and len(st.session_state.calories) > 0:
            mean_calorie = sum(st.session_state.calories) / len(st.session_state.calories)
        if hasattr(st.session_state, 'weights') and len(st.session_state.weights) > 0:
            mean_weight = sum(st.session_state.weights) / len(st.session_state.weights)

        homepage(mean_calorie, mean_weight)
    elif current_tab == "Health":
        health()
    elif current_tab == "Gym":
        plot_interactive_bar_chart_BVP()
        plot_interactive_bar_chart_EDA()

if __name__ == "__main__":
    main()
