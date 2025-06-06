import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
import matplotlib.image as mpimg
import numpy as np
def compute_extent_with_two_anchors(floor, width, height):
    px2_x, px2_y = anchor2_pixel_positions[floor]
    rx2_x, rx2_y = anchor2_real_coords[floor]

    px3_x, px3_y = anchor3_pixel_positions[floor]
    rx3_x, rx3_y = anchor3_real_coords[floor]

    dx_pixel = px2_x - px3_x
    dy_pixel = px2_y - px3_y

    dx_real = rx2_x - rx3_x
    dy_real = rx2_y - rx3_y

    scale_x = dx_real / dx_pixel
    scale_y = dy_real / dy_pixel

    origin_x, origin_y = origin_positions[floor]

    extent = [
        -origin_x * scale_x,
        (width - origin_x) * scale_x,
        -origin_y * scale_y,
        (height - origin_y) * scale_y
    ]
    return extent


# Auto-refresh every 5 seconds (5000 ms)
st_autorefresh(interval=5000, key="refresh")

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

# Map floors to images
floor_bg_images = {
    "Floor 2": "FLOOR2.png",
    "Floor 3": "FLOOR3.png",
    "Floor 4": "FLOOR4.png"
}
# Pixel coordinates of anchor 2 in image (per floor)
origin_positions = {
    "Floor 2": (510, 240),
    "Floor 3": (497 , 240),
    "Floor 4": (713, 214)
}
# Pixel coordinates of anchor 2 in image (per floor)
anchor2_pixel_positions = {
    "Floor 2": (282, 522                                                                                                                    ),
    "Floor 3": (263, 560),
    "Floor 4": (248, 390)
}

# Real-world coordinates of anchor 2 on the grid (per floor)
anchor2_real_coords = {
    "Floor 2": (-11.3, 14.97),
    "Floor 3": (-11.4, 14.62),
    "Floor 4": (-17.9, 6.96)
}
# Multi-select dropdown to choose which tags to show
tags_to_show = st.multiselect(
    "Select Tags to Show",
    options=["TAG1", "TAG2", "TAG3"],
    default=["TAG1", "TAG2", "TAG3"]
)

# Load image and get size
bg_img = mpimg.imread(floor_bg_images[floor])
height, width = bg_img.shape[0], bg_img.shape[1]
#                                                                                                           bg_img = np.fliplr(bg_img)  # This flips the image left-to-right

# Get the anchor pixel that should be treated as (0,0)
origin_x, origin_y = origin_positions[floor]

# Get second anchor pixel and real coords
pixel_x2, pixel_y2 = anchor2_pixel_positions[floor]
real_x2, real_y2 = anchor2_real_coords[floor]

# Calculate pixel differences (relative to origin)
delta_px_x = pixel_x2 - origin_x
delta_px_y = pixel_y2 - origin_y

# Calculate scale factors (real distance / pixel distance)
scale_x = real_x2 / delta_px_x
scale_y = real_y2 / delta_px_y

# Calculate scaled extent for imshow to align grid and image
extent = [
    -origin_x * scale_x,           # left boundary
    (width - origin_x) * scale_x,  # right boundary
    -origin_y * scale_y,           # bottom boundary
    (height - origin_y) * scale_y  # top boundary
]

# Dropdown: Select how many latest positions to show (with 1 included)
num_points = st.selectbox("Show how many latest positions?", [1, 5, 20, 50, 100, 500, "All"], index=1)


# Plot setup
fig, ax = plt.subplots()
# Plot the background image
ax.imshow(bg_img, extent=extent, origin="lower", zorder=0)
ax.set_xlim(extent[0], extent[1])
ax.set_ylim(extent[2], extent[3])
ax.set_title(f"{floor.upper()} - Tag Positions")
ax.set_xlabel("X")
ax.set_ylabel("Y")

# Plot tags with the selected number of latest positions
if "TAG1" in tags_to_show:
    tag1_df = df[["TAG1 X", "TAG1 Y", "TIMESTAMP TAG1"]].dropna()
    if num_points != "All":
        tag1_df = tag1_df.sort_values("TIMESTAMP TAG1", ascending=False).head(num_points)
    ax.scatter(tag1_df["TAG1 X"], tag1_df["TAG1 Y"], label="TAG1", color="blue")

if "TAG2" in tags_to_show:
    tag2_df = df[["TAG2 X", "TAG2 Y", "TIMESTAMP TAG2"]].dropna()
    if num_points != "All":
        tag2_df = tag2_df.sort_values("TIMESTAMP TAG2", ascending=False).head(num_points)
    ax.scatter(tag2_df["TAG2 X"], tag2_df["TAG2 Y"], label="TAG2", color="green")

if "TAG3" in tags_to_show:
    tag3_df = df[["TAG3X", "TAG3Y", "TIMESTAMP TAG3"]].dropna()
    if num_points != "All":
        tag3_df = tag3_df.sort_values("TIMESTAMP TAG3", ascending=False).head(num_points)
    ax.scatter(tag3_df["TAG3X"], tag3_df["TAG3Y"], label="TAG3", color="red")



# Rotate the grid 180 degrees by inverting axes
ax.invert_xaxis()
ax.invert_yaxis()
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Display latest timestamps for selected tags only
st.subheader("Latest Timestamps")
latest_timestamps = {}
if "TAG1" in tags_to_show:
    latest_timestamps["TAG1"] = df['TIMESTAMP TAG1'].dropna().max()
if "TAG2" in tags_to_show:
    latest_timestamps["TAG2"] = df['TIMESTAMP TAG2'].dropna().max()
if "TAG3" in tags_to_show:
    latest_timestamps["TAG3"] = df['TIMESTAMP TAG3'].dropna().max()

st.write(latest_timestamps)
