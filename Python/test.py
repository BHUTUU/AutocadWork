import win32com.client as wc, pythoncom, os
import time
def APoint(x, y, z=0.0):
    return wc.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        (x, y, z)
    )
street_view_block = "streetViewLocate_Suman_Kumar_BHUTUU"
source_file = os.path.join(os.getcwd(),'streetViewLocate_block.dwg')
acad = wc.Dispatch("AutoCAD.Application")
doc = acad.ActiveDocument
# doc.Database.Insert(street_view_block, source_file, False)
street_view_block_active_instance=doc.ModelSpace.InsertBlock(
    APoint(70, 50, 0),
    source_file,
    1.0, 1.0, 1.0,
    0
)
print(dir(street_view_block_active_instance))
for i in range(0,360,20):
#     street_view_block_active_instance.InsertionPoint=APoint(i,i,0)

    street_view_block_active_instance.InsertionPoint = APoint(i, i, 0)
    street_view_block_active_instance.Rotation= i if i<360 else 0
    doc.regen(1)
    time.sleep(2)
time.sleep(10)
street_view_block_active_instance.Delete(),