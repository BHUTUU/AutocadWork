import tkinter as tk
import threading
import webview
from pyproj import Transformer
import win32com.client

# <<<----Coordinate transformer (FIXED CRS) ---->>>
TRANSFORMER = Transformer.from_crs(
    "EPSG:32640",  # UTM84-40N
    "EPSG:4326",
    always_xy=True
)

map_url = None  # shared state

# <<<---- AutoCAD point picker ---->>>
def get_point_from_autocad():
    acad = win32com.client.Dispatch("AutoCAD.Application.25")
    doc = acad.ActiveDocument
    util = doc.Utility

    util.Prompt("\nSelect a point: ")
    point = util.GetPoint()

    return point[0], point[1]

# <<<---- Background worker ---->>>
def pick_point_worker():
    global map_url

    try:
        easting, northing = get_point_from_autocad()
        lon, lat = TRANSFORMER.transform(easting, northing)

        status.set(
            f"E: {easting:.3f}  N: {northing:.3f}\n"
            f"Lat: {lat:.6f}  Lon: {lon:.6f}"
        )

        # Satellite / 3D view url format:
        map_url = f"https://www.google.com/maps/@{lat},{lon},300m/data=!3m1!1e3"


        # Ask main thread to open webview of the selected coordinate
        root.after(0, open_webview)

    except Exception as e:
        status.set(f"Error: {e}")

# <<<---- running the webview on main thread ---->>>
def open_webview():
    webview.create_window(
        "Google Map",
        map_url,
        width=1000,
        height=700
    )
    webview.start()

# <<<---- Button handler ---->>>
def launch():
    threading.Thread(target=pick_point_worker, daemon=True).start()

# <<<---- Tkinter UI ---->>>
root = tk.Tk()
root.title("AutoCAD → Google Map")
root.geometry("420x220")

tk.Label(
    root,
    text="UTM84-40N → Google Street View",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Pick Point from AutoCAD",
    font=("Segoe UI", 11),
    command=launch,
    width=25
).pack(pady=10)

status = tk.StringVar(value="Waiting for input...")

tk.Label(
    root,
    textvariable=status,
    font=("Consolas", 9),
    justify="left"
).pack(pady=10)

root.mainloop()
