import streamlit as st
import numpy as np
import math
from helpers.motors import ALL_MOTORS

st.set_page_config(
    page_title="Custom 1 Speed Drive",
    page_icon="./assets/FIRST-Icon.png"
)

st.title("Custom 1 Speed Drive")

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

    gearing = parse_gearing(st.session_state["gearing"])

    dt_adjusted_speed = selected_motor.free_speed * (session_state.get("speed_loss") / 100) * \
                        ((session_state.get("wheel_dia") * 0.0254 / 2) * 2 * math.pi) / \
                        (0.3048 * 60) / gearing

    dt_free_speed = dt_adjusted_speed / (st.session_state.get("speed_loss") / 100)

    current_draw_per_motor = ((selected_motor.stall_current - selected_motor.free_current) / selected_motor.stall_torque * \
                            (session_state.get("total_weight") * (session_state.get("weight_on_wheels") / 100) * session_state.get("wheel_coeff") / \
                            session_state.get("num_gearboxes") * 4.44822161526 * session_state.get("wheel_dia") * 0.0254 / 2 / \
                            (session_state.get("drivetrain_efficiency") / 100) / session_state.get("num_motors") / gearing)) + \
                            selected_motor.free_current

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Free Speed",
        value=f"{round(dt_free_speed, 2)} ft/s",
    )

    col2.metric(
        label="Adjusted Speed",
        value=f"{round(dt_adjusted_speed, 2)} ft/s"
    )

    col3.metric(
        label="Current Draw Per Motor",
        value=f"{round(current_draw_per_motor, 2)} Amps"
    )

st.selectbox(
    "Choose Motor",
    [motor.name for motor in ALL_MOTORS],
    key="motor_select",
    on_change=calculate
)

col1, col2 = st.columns(2)

col1.number_input(
    "Speed Loss Constant (%)",
    key="speed_loss",
    value=81.0,
    on_change=calculate
)

col2.number_input(
    "Drivetrain Efficiency (%)",
    key="drivetrain_efficiency",
    value=90.0,
    on_change=calculate
)

col1.number_input(
    "Number of Gearboxes in Drivetrain",
    key="num_gearboxes",
    value=2,
    on_change=calculate
)

col2.number_input(
    "Number of Motors per Gearbox",
    key="num_motors",
    value=3,
    on_change=calculate
)

col1.number_input(
    "Total Weight (lbs)",
    key="total_weight",
    value=150.0,
    on_change=calculate
)

col2.number_input(
    "Weight on DT Wheels (%)",
    key="weight_on_wheels",
    value=100.0,
    on_change=calculate
)

col1.number_input(
    "Wheel Diameter (in)",
    key="wheel_dia",
    value=4.0,
    on_change=calculate
)

col2.number_input(
    "Wheel Coefficient",
    key="wheel_coeff",
    value=1.1,
    on_change=calculate
)

st.text_input(
    "Gearing",
    key="gearing",
    value="9:60",
    on_change=calculate
)

st.caption("Enter gearing values as comma seperated values. Ex: \"9:60, 5:40\"")

