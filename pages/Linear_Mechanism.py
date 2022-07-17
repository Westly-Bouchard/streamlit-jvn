import streamlit as st
import numpy as np
import math
from helpers.motors import ALL_MOTORS

st.title("Linear Mechanism")

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
        ratios.append(int(driven_gear) / int(driving_gear))


    return np.prod(ratios)

def calculate():
    session_state = st.session_state

    selected_motor = get_motor_from_selection(session_state.get("motor_select"))

    gearing = parse_gearing(session_state.get("gearing"))

    speed_nl = (selected_motor.free_speed / (gearing) * (360 / 60)) * math.pi * 2 * (session_state.get("pully_dia") / 2) / 360

    time_to_dist_nl = 1 / (speed_nl / session_state.get("travel_dist"))

    stall_load = selected_motor.stall_torque * session_state.get("num_motors") * (gearing) * 39.37 * 0.2248 \
        * (session_state.get("gb_efficiency") / 100) / (session_state.get("pully_dia") / 2)

    current_draw_per_motor_l = ((((selected_motor.stall_current * session_state.get("num_motors")) - \
                            (selected_motor.free_current * session_state.get("num_motors"))) / \
                            (selected_motor.stall_torque * session_state.get("num_motors"))) * \
                            (session_state.get("applied_load") * session_state.get("pully_dia") / 2 / (gearing) / \
                            (0.2248 * 39.37)) + (selected_motor.free_current * session_state.get("num_motors"))) / \
                            session_state.get("num_motors")

    speed_l = (((-1) * ((selected_motor.free_speed / (gearing) * (360 / 60)) / (stall_load)) * (session_state.get("applied_load"))) \
        + (selected_motor.free_speed / (gearing) * (360 / 60))) * (math.pi * 2 * (session_state.get("pully_dia") / 2) / 360)

    time_to_dist_l = 1 / (speed_l / session_state.get("travel_dist"))

    st.write(stall_load)

    st.write(current_draw_per_motor_l)

    st.write(speed_nl)

    st.write(speed_l)

st.selectbox(
    "Choose Motor",
    [motor.name for motor in ALL_MOTORS],
    key="motor_select",
    on_change=calculate
)

col1, col2 = st.columns(2)

col1.number_input(
    "Number of Motors per Gearbox",
    key="num_motors",
    value=1,
    on_change=calculate
)

col2.number_input(
    "Gearbox Efficiency (%)",
    key="gb_efficiency",
    value=80,
    on_change=calculate
)

col3, col4, col5 = st.columns(3)

col3.number_input(
    "Travel Distance",
    key="travel_dist",
    value=24,
    on_change=calculate
)

col4.number_input(
    "Applied Load (lbs)",
    key="applied_load",
    value=180,
    on_change=calculate
)

col5.number_input(
    "Pully Diameter (in)",
    key="pully_dia",
    value=1.273,
    on_change=calculate
)

st.text_input(
    "Gearing",
    key="gearing",
    value="1:12",
    on_change=calculate
)

st.caption("Enter gearing values as comma seperated values. Ex: \"9:60, 5:40\"")