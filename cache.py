import base64

def encode_ico_to_base64(filepath):
    try:
        with open(filepath, "rb") as file:
            # Read the binary content of the file
            binary_data = file.read()
            # Encode the binary data to base64
            base64_data = base64.b64encode(binary_data).decode()
            return base64_data
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
file_path = "icon.ico"
base64_data = encode_ico_to_base64(file_path)
if base64_data:
    with open("requiredicon.py", "w") as file:
        file.write(base64_data)
        file.close()
