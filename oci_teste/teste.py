import os
import sys
import platform

folder = os.getcwd()
os_type = platform.system()
base_folder = "coletabuketcloud"
data_folder = "oci_teste"
slash_windows = "\\"  # Windows uses backslash
slash_unix = "/"  # Unix-like systems use forward slash



if os_type.lower() == "windows":
    path_dir = os.path.join(folder, base_folder, data_folder,slash_windows)
else:
    path_dir = os.path.join(folder, base_folder, data_folder,slash_unix)

print(f"Current working directory: {path_dir}")