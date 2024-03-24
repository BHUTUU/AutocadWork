import win32com.client

class ReplaceTextByMLeader:
    @staticmethod
    def createMleader(coordinate_for_arrow, coordinate_for_lander,text_to_show_on_mleader):
        try:
            acad = win32com.client.GetActiveObject("Autocad.Application")
        except:
            return [False, "Autocad is not running. Run it and open the drawing as current in which you want me to work."]
        arrow_x, arrow_y = coordinate_for_arrow
        lander_x, lander_y = coordinate_for_lander
        cmd = f'(command "MLEADER" "A" "{arrow_x},{arrow_y}", "L" "{lander_x},{lander_y}" "{text_to_show_on_mleader}) ""'
        try:
            acad.ActiveDocument.SendCommand(cmd)
            return [True, "Mleader created."]
        except:
            return [False, "Mleader creation failed. Don't worry just try the same again."]
    @staticmethod
    def doReplace(layerName, ifText=True, ifMtext=True):
        response = "Working on it...!"
        try:
            acad = win32com.client.GetActiveObject("Autocad.Application")
        except:
            return [False, "Autocad is not Running. Run it and open the drawing as current in which you want me to work."]
        activeDoc = acad.ActiveDocument
        modelSpace = activeDoc.ModelSpace
        objectsFound = 0
        for objects in modelSpace:
            if objects.Layer == layerName and (objects.ObjectName == "AcDbText" or objects.ObjectName == "AcDbMText"):
                objectsFound += 1
                if ifText:
                    if objects.objectName == "AcDbText":
                        coordinates = (objects.InsetionPoint[0], objects.InsetionPoint[1])
                        TextValue = objects.TextString
                        objects.Delete()
                        coordinatesForLander = (float(coordinates[0])+10, float(coordinates[1])+10)
                        response = ReplaceTextByMLeader.createMleader(coordinate_for_arrow=coordinates, coordinate_for_lander=coordinatesForLander,text_to_show_on_mleader=TextValue)
                        if response[0] == False:
                            return response
                if ifMtext:
                    if objects.objectName == "AcDbMText":
                        coordinates = (objects.LeaderPoint[0], objects.LeaderPoint[1])
                        TextValue = objects.TextString
                        objects.Delete()
                        coordinatesForLander = (float(coordinates[0])+10, float(coordinates[1])+10)
                        response = ReplaceTextByMLeader.createMleader(coordinate_for_arrow=coordinates, coordinate_for_lander=coordinatesForLander,text_to_show_on_mleader=TextValue)
                        if response[0] == False:
                            return response
                if not ifMtext or not ifText:
                    return [False, "Both ifMtext and ifText is not True hence no task for me to do."]
        if objectsFound == 0:     
            return [True, "Task completed. But i didn't found any text or mtext in the proveded layer to replace."]
            