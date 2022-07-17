import streamlit as st

st.set_page_config(
    page_title="JVN Design Calc",
    page_icon="./assets/FIRST-Icon.png",
    menu_items={
        'About': "https://github.com/Westly-Bouchard/streamlit-jvn",
    }
)

st.title("JVN Design Calculator")

st.write("This application is basically just a reskin of the all powerful JVN design calculator used in the First Robotics Competition which can be found [here](https://www.chiefdelphi.com/t/paper-jvns-mechanical-design-calculator-2016/146281)")
