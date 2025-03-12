import os
import streamlit as st
import json
import datetime
import plotly.graph_objects as go


# Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "circadian.json")

# Load the JSON data
try:
    with open(json_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    st.error(f"Error: The file 'circadian.json' was not found in {script_dir}")
    st.stop()

# Extract time, brightness, and CCT values
time_values = [entry["time"] for entry in data]
brightness_values = [entry["brightness"] for entry in data]
cct_values = [entry["cct"] for entry in data]

# Convert time in minutes to AM/PM format
time_labels = [datetime.timedelta(minutes=t) for t in time_values]
time_labels = [(datetime.datetime.min + t).strftime("%I:%M %p") for t in time_labels]  # Format as AM/PM

# Streamlit App Layout
st.title("Circadian Data Visualization")
st.write("This app visualizes Brightness and CCT over time.")

# Selectbox for choosing the graph
graph_option = st.selectbox(
    "Select the graph to display:",
    ["Brightness vs Time", "CCT vs Time", "Brightness & CCT Overlapping"]
)

# Create interactive Plotly graphs
fig = go.Figure()

if graph_option == "Brightness vs Time":
    fig.add_trace(go.Scatter(
        x=time_labels, y=brightness_values,
        mode="lines+markers",
        name="Brightness",
        marker=dict(color="blue"),
        hoverinfo="x+y"
    ))
    fig.update_layout(
        title="Time vs Brightness",
        xaxis_title="Time (AM/PM)",
        yaxis_title="Brightness Level",
        xaxis=dict(tickangle=-45)
    )

elif graph_option == "CCT vs Time":
    fig.add_trace(go.Scatter(
        x=time_labels, y=cct_values,
        mode="lines+markers",
        name="CCT (Color Temperature)",
        marker=dict(color="red"),
        hoverinfo="x+y"
    ))
    fig.update_layout(
        title="Time vs CCT",
        xaxis_title="Time (AM/PM)",
        yaxis_title="CCT (K)",
        xaxis=dict(tickangle=-45)
    )

elif graph_option == "Brightness & CCT Overlapping":
    fig.add_trace(go.Scatter(
        x=time_labels, y=brightness_values,
        mode="lines+markers",
        name="Brightness",
        marker=dict(color="blue"),
        hoverinfo="x+y"
    ))
    fig.add_trace(go.Scatter(
        x=time_labels, y=cct_values,
        mode="lines+markers",
        name="CCT (Color Temperature)",
        marker=dict(color="red"),
        hoverinfo="x+y"
    ))
    fig.update_layout(
        title="Brightness & CCT Overlapping",
        xaxis_title="Time (AM/PM)",
        yaxis_title="Values",
        xaxis=dict(tickangle=-45)
    )

# Display the graph
st.plotly_chart(fig)

st.write("Select from the dropdown to switch between graphs.")
