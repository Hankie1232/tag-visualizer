import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

# Floor selector
floor = st.selectbox("Select Floor", ["Floor 2", "Floor 3", "Floor 4"])

# Floor-specific URLs
floor_csv_urls = {
    "Floor 2": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwfUuy1HXGj_tkGpqNqOYMX4NtYGBEgCVZLR1eBEUFRYVoh00cO-TH4_9GD6XYnJipOWKW_y8KhKYT/pub?output=csv",
    "Floor 3": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSnU2GckOZBJrCWK5iejVKBzQ2ZfCcbVd5qGFNN24soM-ZA6kWl7gxe7XTOPJPnW-eNA92k3b-zWNN-/pub?output=csv",
    "Floor 4": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQrqDRRhr548jAmoP7AYjNlD6YvHDCxX6-HukCj4o_hxbHXTfwBPOaxVJjzd5f5PwPWfGDcu5DUdB40/pub?output=csv"
}

# Load CSV
df = pd.read_csv(floor_csv_urls[floor])
df.columns = df.columns.str.strip()

# Convert timestamps
for col in ["TIMESTAMP TAG1", "TIMESTAMP TAG2", "TIMESTAMP TAG3"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Create two tabs
tab1, tab2 = st.tabs(["All Positions", "Latest Tag Position"])

with tab1:
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

with tab2:
    st.subheader(f"Latest Tag Positions on {floor}")
    
    latest_positions = {}
    fig2, ax2 = plt.subplots()
    ax2.set_title("Latest Tag Position")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")

    if not df.empty:
        for tag, x_col, y_col, time_col, color in [
            ("TAG1", "TAG1 X", "TAG1 Y", "TIMESTAMP TAG1", "blue"),
            ("TAG2", "TAG2 X", "TAG2 Y", "TIMESTAMP TAG2", "green"),
            ("TAG3", "TAG3X", "TAG3Y", "TIMESTAMP TAG3", "red"),
        ]:
            latest_time = df[time_col].dropna().max()
            if pd.notna(latest_time):
                latest_row = df[df[time_col] == latest_time].iloc[0]
                x, y = latest_row[x_col], latest_row[y_col]
                latest_positions[tag] = {"X": x, "Y": y, "Timestamp": latest_time}
                ax2.scatter(x, y, label=tag, color=color)

        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)
        st.write("Latest Coordinates:")
        st.json(latest_positions)
    else:
        st.warning("No data available.")
