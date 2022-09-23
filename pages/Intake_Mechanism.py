import streamlit as st
import numpy as np
import math
from helpers.motors import ALL_MOTORS

st.set_page_config(
    page_title="Intake Mechanism",
    page_icon="./assets/FIRST-Icon.png"
)

st.title("Intake Mechanism")

def get_motor_from_selection(motor_name):
    for motor in ALL_MOTORS:
        if motor.name == motor_name:
            return motor

def parse_gearing(input_string):
    """Returns the overall gear ratio for the drivetrain from an input string"""
    parsed_ratios = input_string.split(", ")

    ratios = []

    for ratio in parsed_ratios:
        driving_gear, driven_gear = ratio.split(":")
        ratios.append(float(driven_gear) / float(driving_gear))


    return np.prod(ratios)

def calculate():
    session_state = st.session_state

    selected_motor = get_motor_from_selection(session_state.get("motor_select"))

    gearing = parse_gearing(session_state.get("gearing"))

    speed_nl = (selected_motor.free_speed / (gearing) * (360 / 60)) * math.pi * 2 * (session_state.get("roller_dia") / 2) / 360 * session_state.get("num_sides")

    time_to_dist_nl = 1 / (speed_nl / session_state.get("travel_dist"))

    stall_load = selected_motor.stall_torque * session_state.get("num_motors") * (gearing) * 39.37 * 0.2248 \
    * (session_state.get("gb_efficiency") / 100) / (session_state.get("roller_dia") / 2)

    current_draw_per_motor_l = ((((selected_motor.stall_current * session_state.get("num_motors")) - \
                        (selected_motor.free_current * session_state.get("num_motors"))) / \
                        (selected_motor.stall_torque * session_state.get("num_motors"))) * \
                        (session_state.get("drag_load") * session_state.get("roller_dia") / 2 / (gearing) / \
                        (0.2248 * 39.37)) + (selected_motor.free_current * session_state.get("num_motors"))) / \
                        session_state.get("num_motors")

    speed_l = (((-1) * ((selected_motor.free_speed / (gearing) * (360 / 60)) / (stall_load)) * (session_state.get("drag_load"))) \
    + (selected_motor.free_speed / (gearing) * (360 / 60))) * (math.pi * 2 * (session_state.get("roller_dia") / 2) / 360) * session_state.get("num_sides")

    time_to_dist_l = 1 / (speed_l / session_state.get("travel_dist"))

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Speed No Load",
        value=f"{round(speed_nl, 2)} in/s",
        delta=f"{round(time_to_dist_nl, 2)} sec"
    )

    col2.metric(
        "Speed Loaded",
        value=f"{round(speed_l, 2)} in/s",
        delta=f"{round(time_to_dist_l, 2)} sec"
    )

    col3.metric(
        "Current Draw Per Motor",
        value=f"{round(current_draw_per_motor_l, 2)} Amp"
    )

    col4.metric(
        "Stall Drag Load",
        value=f"{round(stall_load, 2)} lbs"
    )


st.selectbox(
    "Choose Motor",
    [motor.name for motor in ALL_MOTORS],
    key="motor_select",
    on_change=calculate
)

col1, col2, col3 = st.columns(3)

col1.number_input(
    "Number of Motors per Gearbox",
    key="num_motors",
    value=1,
    on_change=calculate
)

col2.number_input(
    "Gearbox Efficiency",
    key="gb_efficiency",
    value=80.0,
    on_change=calculate
)

col3.number_input(
    "Travel Distance (in)",
    key="travel_dist",
    value=20.0,
    on_change=calculate
)

col1.number_input(
    "Number of Intake Sides (2 or 1)",
    key="num_sides",
    value=1,
    on_change=calculate
)

col2.number_input(
    "Roller Diamteter (in)",
    key="roller_dia",
    value=2.125,
    on_change=calculate
)

col3.number_input(
    "Drag Load",
    key="drag_load",
    value=3.0,
    on_change=calculate
)

st.text_input(
    "Gearing",
    key="gearing",
    value="1:3",
    on_change=calculate
)

st.caption("Enter gearing values as comma seperated values. Ex: \"9:60, 5:40\"")