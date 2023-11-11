import streamlit as st

# Create three tabs: Tab 1, Tab 2, and Tab 3
tabs = ["Tab 1", "Tab 2", "Tab 3"]
selected_tab = st.sidebar.radio("Select Tab", tabs)

# Add content to each tab
if selected_tab == "Tab 1":
    st.title("Welcome to Tab 1")
    st.write("This is the content for Tab 1.")

elif selected_tab == "Tab 2":
    st.title("Explore Tab 2")
    st.write("Content for Tab 2 goes here.")

elif selected_tab == "Tab 3":
    st.title("Tab 3 Insights")
    st.write("Content for Tab 3 can be added here.")

