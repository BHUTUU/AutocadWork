import win32com.client,os, shutil

class SeperateLayouts:
    numberOfLayouts = []
    @classmethod
    def getNumberOfLayouts(cls, path_to_source_dwg):
        layoutarray = []
        try:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True
            doc = acad.Documents.Open(path_to_source_dwg)
            layouts = doc.Layouts
            cls.numberOfLayouts = len(layouts) - 1 #model space ko v count kr raha hai to remove kr diya 1.
            for layout in layouts:
                layoutarray.append(layout.Name)
            layoutarray.remove("Model")
            return (cls.numberOfLayouts, layoutarray)
        except Exception:
            return [False, "Could not connect to AutoCAD."]
    @classmethod
    def deleteAllLayoutsExceptIndex(filePath, fileName: str, index: str):
        try:
            acad = win32com.client.Dispatch("AutoCAD.Application")
            acad.Visible = True
            doc = acad.Documents.Open(filePath)
            layouts = doc.Layouts
            for layout in layouts:
                layoutName = str(layout.Name)
                if layoutName == fileName or layoutName == index or layoutName == "Model":
                    continue
                else:
                    layout.Delete()
            for layout in layouts:
                layoutName = str(layout.Name)
                if layoutName == "Model":
                    continue
                elif layoutName == fileName:
                    break
                else:
                    layout.Name = fileName
        except Exception:
            return [False, "Could not connect to AutoCAD."]
    @staticmethod
    def doSeparate(path_to_source_dwg, path_to_dir_for_generated_dwg):
        if not os.path.isfile(path_to_source_dwg):
            return [False, "The path to the source dwg is not valid."]
        if not os.path.isdir(path_to_dir_for_generated_dwg):
            return [False, "The path to the dir for generated dwg is not valid."]
        layoutNumberAndName = SeperateLayouts.getNumberOfLayouts(path_to_source_dwg)
        if layoutNumberAndName[0] == False:
            return layoutNumberAndName
        numberOfLayouts = layoutNumberAndName[0]
        # layoutarray = layoutNumberAndName[1]
        baseNameOfDwg = str(path_to_source_dwg)[:-4]
        initialForRange=1
        errorInFiles=[]
        if path_to_source_dwg in os.listdir(path_to_dir_for_generated_dwg):
            initialForRange=2
        for i in range(initialForRange, int(numberOfLayouts)+1):
            tempfilehold  = os.path.join(path_to_dir_for_generated_dwg, f"{baseNameOfDwg}{i}.dwg")
            if not os.path.isfile(tempfilehold):
                shutil.copy(path_to_source_dwg, tempfilehold)
                delResponse = SeperateLayouts.deleteAllLayoutsExceptIndex(tempfilehold, f"{baseNameOfDwg}{i}.dwg", str(i))
                if delResponse[0] == False:
                    errorInFiles.append(tempfilehold+": error while deleting layouts for this file")
            else:
                errorInFiles.append(tempfilehold+": This file already exists at destination so i will not even delete layouts from it.")
        return [True, errorInFiles]
