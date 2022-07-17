import streamlit as st
import numpy as np
from helpers.motors import ALL_MOTORS

st.set_page_config(
    page_title="Rotary Mechanism",
    page_icon="./assets/FIRST-Icon.png"
)

st.title("Rotary Mechanism")

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

    rot_speed_nl = selected_motor.free_speed / gearing * (360 / 60)

    time_to_90_deg_nl = 90 / rot_speed_nl

    stall_load = selected_motor.stall_torque * session_state.get("num_motors") * gearing * 39.37 * 0.2248 * \
                (session_state.get("gb_efficiency") / 100) / session_state.get("arm_length")

    rot_speed_l = ((-1) * (rot_speed_nl / stall_load) * session_state.get("arm_load")) + rot_speed_nl

    time_to_90_deg_nl = 90 / rot_speed_l

    current_draw_per_motor_l = ((((selected_motor.stall_current * session_state.get("num_motors")) - \
                            (selected_motor.free_current * session_state.get("num_motors"))) / \
                            (selected_motor.stall_torque * session_state.get("num_motors"))) * \
                            (session_state.get("arm_load") * session_state.get("arm_length") / (gearing) / \
                            (0.2248 * 39.37)) + (selected_motor.free_current * session_state.get("num_motors"))) / \
                            session_state.get("num_motors")

    st.write(stall_load)

    st.write(rot_speed_nl)

    st.write(rot_speed_l)

    st.write(current_draw_per_motor_l)


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
    value=65,
    on_change=calculate
)

col1.number_input(
    "Arm Load (lbs)",
    key="arm_load",
    value=0.5,
    on_change=calculate
)

col2.number_input(
    "Arm Length (in)",
    key="arm_length",
    value=2,
    on_change=calculate
)

st.text_input(
    "Gearing",
    key="gearing",
    value="1:3",
    on_change=calculate
)

st.caption("Enter gearing values as comma seperated values. Ex: \"9:60, 5:40\"")