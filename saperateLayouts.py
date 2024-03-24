import os
import win32com.client

def save_layout_as_separate_files(dwg_path):
    try:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        acad.Visible = True  # Optional: Set to True to make AutoCAD visible

        doc = acad.Documents.Open(dwg_path)
        layouts = doc.Layouts

        for layout in layouts:
            # Get layout number
            layout_number = layout.TabOrder

            # Create a new drawing file name based on layout number
            new_dwg_name = f"layout_{layout_number}.dwg"

            # Save the layout as a separate drawing file  
            layout.Copy(new_dwg_name)

            # Close the new document without saving changes to keep only the layout
            acad.Documents.Item(acad.Documents.Count - 1).Close(False)

            # Rename the saved file to the new name
            os.rename(new_dwg_name, f"layout_{layout_number}.dwg")

        # Close the original document
        doc.Close()

        print("Layouts saved as separate files successfully.")

    except Exception as e:
        print("Error:", e)

# Example usage
dwg_path = os.path.join(os.getcwd(), "test.dwg")
save_layout_as_separate_files(dwg_path)
