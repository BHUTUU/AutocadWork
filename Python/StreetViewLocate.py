import tkinter as tk
import threading, sys
import webview
from pyproj import Transformer
import win32com.client as wc

# <<<----------- AutoCAD CS → EPSG mapping ----------->>>
ACAD_CS_TO_EPSG = {
    "UTM84-40N": "EPSG:32640",
    "UTM84-41N": "EPSG:32641",
    "UTM84-42N": "EPSG:32642",
    "UTM84-43N": "EPSG:32643",
    "UTM84-44N": "EPSG:32644",
    "UTM84-45N": "EPSG:32645",
    "WGS84": "EPSG:4326",
    "BRITISHNATGRID": "EPSG:27700",
    "WEBMERCATOR": "EPSG:3857"
}
map_url = None  # shared state
TRANSFORMER = None
coodinateSystem=None
# <<<---- AutoCAD point picker ---->>>
def get_point_from_autocad():
    global TRANSFORMER
    global coodinateSystem
    acad = wc.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    util = doc.Utility
    util.Prompt("\nSelect a point: ")
    point = util.GetPoint()
    coodinateSystem=str(doc.GetVariable("CGEOCS")).strip().upper()
    if not coodinateSystem in ACAD_CS_TO_EPSG.keys():
        doc.SendCommand(f'(alert "No coordinate system found in this drawing please do set by DRAWINGSETTINGS command in Civil 3D.") ')
        sys.exit(1)
    # <<<----Coordinate transformer (FIXED CRS) ---->>>
    TRANSFORMER = Transformer.from_crs(
        ACAD_CS_TO_EPSG.get(coodinateSystem),
        "EPSG:4326",
        always_xy=True
    )
    return point[0], point[1]
# <<<---- Background worker ---->>>
def pick_point_worker():
    global map_url
    try:
        easting, northing = get_point_from_autocad()
        lon, lat = TRANSFORMER.transform(easting, northing)
        status.set(
            f"CS: {acad_cs} ({epsg})\n"
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
        "StreetView Locate ~BHUTUU",
        map_url,
        width=1000,
        height=700
    )
    webview.start()

# <<<----------- Tkinter UI ----------->>>
root = tk.Tk()
root.title("AutoCAD Streetview Locate")
root.geometry("420x220")

tk.Label(
    root,
    text="AutoCAD/C3D → Google Street View",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)

tk.Button(
    root,
    text="Pick Point from AutoCAD",
    font=("Segoe UI", 11),
    command=on_pick_point,
    width=30
).pack(pady=10)

status = tk.StringVar(value="Waiting for AutoCAD input...")

tk.Label(
    root,
    textvariable=status,
    font=("Consolas", 9),
    justify="left"
).pack(pady=10)
root.mainloop()