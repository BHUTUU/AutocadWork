import win32com.client

def remove_duplicate_objects():
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        acad.Visible = True  # Optional: Set to True to make AutoCAD visible

        doc = acad.ActiveDocument
        ms = doc.ModelSpace

        objects_to_delete = []

        for obj1 in ms:
            if obj1.ObjectName == "AcDbEntity":  # Check if it's a valid entity
                # Get object type, properties, and coordinates
                obj1_type = obj1.EntityName
                obj1_props = obj1.GetAttributes()
                obj1_coords = obj1.InsertionPoint

                for obj2 in ms:
                    if obj1 is not obj2 and obj2.ObjectName == "AcDbEntity":  # Check if it's a valid entity and not the same object
                        obj2_type = obj2.EntityName
                        obj2_props = obj2.GetAttributes()
                        obj2_coords = obj2.InsertionPoint

                        # Check if object types, properties, and coordinates match
                        if obj1_type == obj2_type and obj1_props == obj2_props and obj1_coords == obj2_coords:
                            objects_to_delete.append(obj2)

        # Delete duplicate objects
        for obj in objects_to_delete:
            obj.Delete()

        print("Duplicate objects removed successfully.")

    except Exception as e:
        print("Error:", e)

# Example usage
remove_duplicate_objects()
