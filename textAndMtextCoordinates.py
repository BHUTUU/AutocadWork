import win32com.client

def get_text_mtext_coordinates(layer_name):
    acad = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad.ActiveDocument
    ms = doc.ModelSpace

    coordinates_and_values = []

    for obj in ms:
        if obj.Layer == layer_name and (obj.ObjectName == "AcDbText" or obj.ObjectName == "AcDbMText"):
            if obj.ObjectName == "AcDbText":
                coordinates = (obj.InsertionPoint[0], obj.InsertionPoint[1])
                value = obj.TextString
                coordinates_and_values.append((coordinates, value))
                obj.Delete()
                mleader = ms.AddMLeader(coordinates[0], coordinates[1])
                mleader.TextString = value
                mleader.Layer = layer_name
                mleader.StyleName = "Standard"
                mleader.LeaderLineType = 0
            elif obj.ObjectName == "AcDbMText":
                coordinates = (obj.InsertionPoint[0], obj.InsertionPoint[1])
                value = obj.TextString
                coordinates_and_values.append((coordinates, value))
                obj.Delete()
                mleader = ms.AddMLeader(coordinates[0], coordinates[1])
                mleader.TextString = value
                mleader.Layer = layer_name
                mleader.StyleName = "Standard"
                mleader.LeaderLineType = 0

    return coordinates_and_values

layer_name = "this_is_my_layer_for_text"  # Specify the name of the layer you want to retrieve objects from
coordinates_and_values = get_text_mtext_coordinates(layer_name)
print(coordinates_and_values)
