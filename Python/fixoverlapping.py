import win32com.client
import sys
from shapely.geometry import Polygon

acad = win32com.client.Dispatch("AutoCAD.Application")
doc = acad.ActiveDocument
try:
    doc.SelectionSets.Item("PYSEL").Delete()
except:
    pass
ss = doc.SelectionSets.Add("PYSEL")
ss.SelectOnScreen()
#validate_selections:
number_of_selection=len([i for i in ss])
POLYLINES=[]
if number_of_selection == 2:
    for obj in ss:
        if obj.ObjectName == "AcDbPolyline" and obj.Closed:
            POLYLINES.append(obj)
        else:
            doc.SendCommand('(alert "Selected objects must be closed polylines!" ) ')
            sys.exit(1)
else:
    doc.SendCommand('(alert "There must be at least and not more than 2 Closed polylines!" ) ')
    sys.exit(1)
vertices_of_pl1 = POLYLINES[0].Coordinates
vertices_of_pl2 = POLYLINES[1].Coordinates
points_of_pl1 = [(vertices_of_pl1[i], vertices_of_pl1[i+1]) for i in range(0, len(vertices_of_pl1), 2)]
points_of_pl2 = [(vertices_of_pl2[i], vertices_of_pl2[i+1]) for i in range(0, len(vertices_of_pl2), 2)]
print("Points of Pl1", points_of_pl1)
print("Points of Pl2", points_of_pl2)
poly1 = Polygon(points_of_pl1)
poly2 = Polygon(points_of_pl2)
if poly1.intersects(poly2):
    intersection = poly1.intersection(poly2)
    print("Intersection type:", intersection.geom_type)
    if intersection.geom_type == "Polygon":
        print("Vertices: ", list(intersection.exterior.coords))
    elif intersection.geom_type == "LineString":
        print("Line coordinates: ", list(intersection.coords))
    elif intersection.geom_type == "Point":
        print("Point: ", intersection.coords)
else:
    print("Polygon does not intersect")