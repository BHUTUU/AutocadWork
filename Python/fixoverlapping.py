import math
import time

import win32com.client
import sys
from shapely import LineString
from shapely.ops import split
from shapely.geometry import Polygon, Point

acad = win32com.client.Dispatch("AutoCAD.Application")
doc = acad.ActiveDocument
try:
    doc.SelectionSets.Item("PYSEL").Delete()
except:
    pass
ss = doc.SelectionSets.Add("PYSEL")
ss.SelectOnScreen()
#validate_selections:
while True:
    try:
        number_of_selection=len([i for i in ss])
        break
    except Exception:
        continue
POLYLINES=[]
if number_of_selection == 2:
    for obj in ss:
        while True:
            try:
                if obj.ObjectName == "AcDbPolyline" and obj.Closed:
                    POLYLINES.append(obj)
                else:
                    doc.SendCommand('(alert "Selected objects must be closed polylines!" ) ')
                    sys.exit(1)
                break
            except Exception:
                continue
else:
    doc.SendCommand('(alert "There must be at least and not more than 2 Closed polylines!" ) ')
    sys.exit(1)
def print_circle_commands(coords, radius=2.0):
    for i in coords:
        x = i[0]
        y = i[1]
        while True:
            try:
                doc.SendCommand(f'(command "CIRCLE" "{x},{y}" "{radius}" ) ')
                break
            except Exception:
                continue
vertices_of_pl1 = POLYLINES[0].Coordinates
vertices_of_pl2 = POLYLINES[1].Coordinates
points_of_pl1 = [(vertices_of_pl1[i], vertices_of_pl1[i+1]) for i in range(0, len(vertices_of_pl1), 2)]
points_of_pl2 = [(vertices_of_pl2[i], vertices_of_pl2[i+1]) for i in range(0, len(vertices_of_pl2), 2)]
# print("Points of Pl1", points_of_pl1)
# print("Points of Pl2", points_of_pl2)
poly1 = Polygon(points_of_pl1)
poly2 = Polygon(points_of_pl2)
result = poly1.difference(poly2)
# print(result)
cmd = '(command "PLINE" '
for x, y in result.exterior.coords:
    cmd += f'"{x},{y}" '
cmd += '"C") '
while True:
    try:
        time.sleep(2)
        doc.SendCommand(cmd)
        break
    except Exception:
        continue


###<------------wasted my time to figure out the simple logical subtraction operation------------>>>
# intersection_geoms = []
# if poly1.intersects(poly2):
#     intersection = poly1.intersection(poly2)
#     print("Intersection type:", intersection.geom_type)
#     if intersection.geom_type == "Polygon":
#         intersection_geoms.append(intersection)
#         # print("Vertices: ", list(intersection.exterior.coords))
#     elif intersection.geom_type == "LineString":
#         # print("Line coordinates: ", list(intersection.coords))
#         sys.exit(0)
#     elif intersection.geom_type == "Point":
#         # print("Point: ", intersection.coords)
#         sys.exit(0)
#     elif intersection.geom_type == "MultiLineString":
#         sys.exit(0)
#     elif intersection.geom_type == "MultiPoint":
#         sys.exit(0)
#     elif intersection.geom_type == "MultiPolygon":
#         for geom in intersection.geoms:
#             intersection_geoms.append(geom)
#             print(geom)
# else:
#     print("Polygon does not intersect")
#     sys.exit(0)
#
# corrected_poly1 = points_of_pl1
# intersection_boundary = poly1.boundary.intersection(poly2.boundary)
# intersection_points = [(p.x, p.y) for p in intersection_boundary.geoms]
# intersection_point_used_index = 0
# print_circle_commands(intersection_points)
#
#
# def replace_block(base_polyline_points_list, to_remove_points_list, to_add_points_list):
#     global intersection_points
#     global intersection_point_used_index
#     start_boundary=intersection_points[intersection_point_used_index]
#     end_boundary=intersection_points[intersection_point_used_index+1]
#     intersection_point_used_index += 2
#     #<<<-----------find block start----------->>>
#     start = base_polyline_points_list.index(to_remove_points_list[0])
#     end = start + len(to_remove_points_list)
#
#     #<<<-----------replace block----------->>>
#     return (
#         base_polyline_points_list[:start] +
#         [start_boundary] +
#         to_add_points_list +
#         [end_boundary] +
#         base_polyline_points_list[end:]
#     )
# def intersection_handler(intersection_geometry):
#     global corrected_poly1
#     overlapping_vertices_of_p1 = [i for i in list(intersection_geometry.exterior.coords) if i in points_of_pl1 and i not in points_of_pl2]
#     overlapping_vertices_of_p2 = [i for i in list(intersection_geometry.exterior.coords) if i in points_of_pl2 and i not in points_of_pl1]
#     corrected_poly1=replace_block(corrected_poly1, overlapping_vertices_of_p1, overlapping_vertices_of_p2)
#
#
# for ig in intersection_geoms:
#     intersection_handler(ig)
# print("\n\n\n\n")
# cmd = '(command "PLINE" '
# for x, y in points_of_pl2:
#     cmd += f'"{x},{y}" '
# cmd += '"C") '
# doc.SendCommand(cmd)