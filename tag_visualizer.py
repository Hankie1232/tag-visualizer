import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=30000, key="refresh")  # Auto-refresh every 30 seconds

# URL of your published Google Sheet as CSV
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnU2GckOZBJrCWK5iejVKBzQ2ZfCcbVd5qGFNN24soM-ZA6kWl7gxe7XTOPJPnW-eNA92k3b-zWNN-/pub?output=csv"

# Load data
df = pd.read_csv(csv_url)

# Assuming columns like:
# 'TIMESTAMP TAG1', 'TAG1 X', 'TAG1 Y', 'TIMESTAMP TAG2', 'TAG2 X', 'TAG2 Y', etc.

# Make timestamp columns datetime type for nicer formatting
df['TIMESTAMP TAG1'] = pd.to_datetime(df['TIMESTAMP TAG1'], errors='coerce')
df['TIMESTAMP TAG2'] = pd.to_datetime(df['TIMESTAMP TAG2'], errors='coerce')
df['TIMESTAMP TAG3'] = pd.to_datetime(df['TIMESTAMP TAG3'], errors='coerce')


st.title("Tag Position Visualizer")

# Tag selection checkboxes
show_tag1 = st.checkbox("Show Tag 1", value=True)
show_tag2 = st.checkbox("Show Tag 2", value=True)
show_tag3 = st.checkbox("Show Tag 3", value=True)

fig, ax = plt.subplots()

if show_tag1:
    x1 = df['TAG1 X']
    y1 = df['TAG1 Y']
    ax.scatter(x1, y1, label="Tag 1")
    # Show latest timestamp for Tag1
    st.write(f"Tag 1 latest timestamp: {df['TIMESTAMP TAG1'].max()}")

if show_tag2:
    x2 = df['TAG2 X']
    y2 = df['TAG2 Y']
    ax.scatter(x2, y2, label="Tag 2")
    st.write(f"Tag 2 latest timestamp: {df['TIMESTAMP TAG2'].max()}")

if show_tag3:
    x3 = df['TAG3X']
    y3 = df['TAG3Y']
    ax.scatter(x3, y3, label="Tag 3")
    st.write(f"Tag 3 latest timestamp: {df['TIMESTAMP TAG3'].max()}")

ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.legend()
ax.grid(True)
st.pyplot(fig)
