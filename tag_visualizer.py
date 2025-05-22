import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, key="refresh")

# Floor selector
floor = st.selectbox("Select Floor", ["Floor 2", "Floor 3", "Floor 4"])

# Floor-specific URLs
floor_csv_urls = {
    "Floor 2": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwfUuy1HXGj_tkGpqNqOYMX4NtYGBEgCVZLR1eBEUFRYVoh00cO-TH4_9GD6XYnJipOWKW_y8KhKYT/pub?output=csv",
    "Floor 3": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnU2GckOZBJrCWK5iejVKBzQ2ZfCcbVd5qGFNN24soM-ZA6kWl7gxe7XTOPJPnW-eNA92k3b-zWNN-/pub?output=csv",
    "Floor 4": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrqDRRhr548jAmoP7AYjNlD6YvHDCxX6-HukCj4o_hxbHXTfwBPOaxVJjzd5f5PwPWfGDcu5DUdB40/pub?output=csv"
}

# Load the selected CSV
df = pd.read_csv(floor_csv_urls[floor])

# Fix column names
df.columns = df.columns.str.strip()

# Convert timestamps
for col in ["TIMESTAMP TAG1", "TIMESTAMP TAG2", "TIMESTAMP TAG3"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Sidebar filters
show_tag1 = st.sidebar.checkbox("Show TAG1", value=True)
show_tag2 = st.sidebar.checkbox("Show TAG2", value=True)
show_tag3 = st.sidebar.checkbox("Show TAG3", value=True)

# Plot
fig, ax = plt.subplots()
ax.set_title(f"{floor.upper()} - Tag Positions")
ax.set_xlabel("X")
ax.set_ylabel("Y")

if show_tag1:
    ax.scatter(df["TAG1 X"], df["TAG1 Y"], label="TAG1", color="blue")
if show_tag2:
    ax.scatter(df["TAG2 X"], df["TAG2 Y"], label="TAG2", color="green")
if show_tag3:
    ax.scatter(df["TAG3X"], df["TAG3Y"], label="TAG3", color="red")

ax.legend()
ax.grid(True)
st.pyplot(fig)

# Display latest timestamps
st.subheader("Latest Timestamps")
st.write({
    "TAG1": df['TIMESTAMP TAG1'].dropna().max(),
    "TAG2": df['TIMESTAMP TAG2'].dropna().max(),
    "TAG3": df['TIMESTAMP TAG3'].dropna().max()
})
