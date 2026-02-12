import tkinter as tk
import threading
import sys, re, os
import webview
from pyproj import Transformer
import win32com.client as wc, pythoncom
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
    "OSGB1936.NATIONALGRID": "EPSG:27700",
    "WEBMERCATOR": "EPSG:3857"
}
map_url = None
TRANSFORMER = None
REVERSETRANSFORMER = None
coordinateSystem = None
street_view_block_active_instance=None
doc=None
# <<<---- WebView API (JS → Python) ---->>>
class WebAPI:
    def update_url(self, url):
        global map_url, REVERSETRANSFORMER,doc, street_view_block_active_instance
        map_url = url
        print("Street View URL changed:")
        print(url)
        print("-" * 60)
        lat, long, heading, pitch = self.parse_streetview_url(url)
        northing, easting = REVERSETRANSFORMER.transform(long, lat)
        try:
            street_view_block_active_instance.InsertionPoint = WebAPI.APoint(northing, easting, 0)
            street_view_block_active_instance.Rotation=((360 -heading) * 3.141592653589793) / 180
            # print(360-heading)
            # print((street_view_block_active_instance.Rotation * 180) / 3.141592653589793)
            # doc.regen(1)
        except Exception:
            print("failed to move the block")
            pass
        # print(self.parse_streetview_url(url))
    def parse_streetview_url(self, url):
        pattern = r'@(-?\d+\.\d+),(-?\d+\.\d+),3a,[^h]*?([0-9.]+)h,([0-9.]+)t'
        match = re.search(pattern, url)
        if not match:
            raise ValueError("No Street View pano data in URL")
        lat = float(match.group(1))
        lon = float(match.group(2))
        heading = float(match.group(3))  # yaw
        pitch = float(match.group(4))
        return lat, lon, heading, pitch
    @staticmethod
    def APoint(x, y, z=0.0):
        return wc.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8,
            (x, y, z)
        )
# <<<---- Street View lock JS ---->>>
URL_WATCHER_JS = r"""
(function () {
    function forceStreetView() {
        const url = location.href;
        // Already Street View
        if (url.includes("!1e1") || url.includes("3a")) {
            window.pywebview.api.update_url(url);
            return;
        }
        // Extract lat/lon
        const match = url.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
        if (!match) return;
        const lat = match[1];
        const lon = match[2];
        const streetUrl =
            `https://www.google.com/maps/@${lat},${lon},3a,75y,90t/data=!3m1!1e1`;
        location.replace(streetUrl);
    }
    const pushState = history.pushState;
    history.pushState = function () {
        pushState.apply(history, arguments);
        forceStreetView();
    };
    const replaceState = history.replaceState;
    history.replaceState = function () {
        replaceState.apply(history, arguments);
        forceStreetView();
    };
    window.addEventListener('popstate', forceStreetView);
    let lastUrl = location.href;
    setInterval(() => {
        if (location.href !== lastUrl) {
            lastUrl = location.href;
            forceStreetView();
        }
    }, 500);
})();
"""
# <<<---- AutoCAD point picker ---->>>
def get_point_from_autocad():
    global TRANSFORMER, REVERSETRANSFORMER,coordinateSystem, street_view_block_active_instance, doc
    street_view_block = "streetViewLocate_Suman_Kumar_BHUTUU"
    source_file = os.path.join(os.getcwd(),"streetViewLocate_block.dwg")
    acad = wc.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    util = doc.Utility
    util.Prompt("\nSelect a point: ")
    point = util.GetPoint()
    coordinateSystem = str(doc.GetVariable("CGEOCS")).strip().upper()
    if coordinateSystem not in ACAD_CS_TO_EPSG:
        doc.SendCommand(
            '(alert "No coordinate system found. Set it using DRAWINGSETTINGS in Civil 3D.") '
        )
        sys.exit(1)
    TRANSFORMER = Transformer.from_crs(
        ACAD_CS_TO_EPSG[coordinateSystem],
        "EPSG:4326",
        always_xy=True
    )
    REVERSETRANSFORMER = Transformer.from_crs(
        "EPSG:4326",
        ACAD_CS_TO_EPSG[coordinateSystem],
        always_xy=True
    )
    street_view_block_active_instance=doc.ModelSpace.InsertBlock(
        WebAPI.APoint(point[0], point[1], 0),
        source_file,
        1.0, 1.0, 1.0,
        0
    )
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
        map_url = (
            f"https://www.google.com/maps/"
            f"@{lat},{lon},3a,75y,90t/data=!3m1!1e1"
        )
        root.after(0, open_webview)
    except Exception as e:
        status.set(f"Error: {e}")
# <<<---- WebView runner (main thread) ---->>>
def open_webview():
    api = WebAPI()
    window = webview.create_window(
        "StreetView Locate ~BHUTUU",
        map_url,
        width=1000,
        height=700,
        js_api=api
    )
    def on_loaded():
        window.evaluate_js(URL_WATCHER_JS)
    window.events.loaded += on_loaded
    webview.start()
# <<<---- Button handler ---->>>
def launch():
    threading.Thread(target=pick_point_worker, daemon=True).start()
# <<<---- Tkinter UI ---->>>
root = tk.Tk()
root.title("AutoCAD/C3D → StreetView Locate")
root.geometry("420x220")
tk.Label(
    root,
    text="AutoCAD/C3D → StreetView Locate",
    font=("Segoe UI", 12, "bold")
).pack(pady=10)
tk.Button(
    root,
    text="Pick Point from AutoCAD",
    font=("Segoe UI", 11),
    command=launch,
    width=28
).pack(pady=10)
status = tk.StringVar(value="Waiting for input...")
tk.Label(
    root,
    textvariable=status,
    font=("Consolas", 9),
    justify="left"
).pack(pady=10)
root.mainloop()