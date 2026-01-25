import tkinter as tk
import webbrowser
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

TARGET_EPSG = "EPSG:4326"


def get_autocad_coordinate_system():
    acad = wc.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument

    cs = doc.GetVariable("CGEOCS")
    if not cs:
        raise RuntimeError("CGEOCS not set in drawing")

    return cs.strip().upper()


def build_transformer():
    acad_cs = get_autocad_coordinate_system()

    if acad_cs not in ACAD_CS_TO_EPSG:
        raise RuntimeError(f"Unsupported coordinate system: {acad_cs}")

    source_epsg = ACAD_CS_TO_EPSG[acad_cs]

    transformer = Transformer.from_crs(
        source_epsg,
        TARGET_EPSG,
        always_xy=True
    )

    return transformer, acad_cs, source_epsg


def pick_point_from_autocad():
    acad = wc.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    util = doc.Utility

    util.Prompt("\nSelect a point: ")
    pt = util.GetPoint()

    return pt[0], pt[1]


def on_pick_point():
    try:
        transformer, acad_cs, epsg = build_transformer()

        easting, northing = pick_point_from_autocad()
        lon, lat = transformer.transform(easting, northing)

        status.set(
            f"CS: {acad_cs} ({epsg})\n"
            f"E: {easting:.3f}  N: {northing:.3f}\n"
            f"Lat: {lat:.6f}  Lon: {lon:.6f}"
        )

        url = f"https://www.google.com/maps/@{lat},{lon},300m/data=!3m1!1e3"
        webbrowser.open(url)

    except Exception as e:
        status.set(f"Error: {e}")


# <<<----------- Tkinter UI ----------->>>
root = tk.Tk()
root.title("AutoCAD → Google Street View")
root.geometry("480x260")

tk.Label(
    root,
    text="AutoCAD → Google Street View Locator",
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
