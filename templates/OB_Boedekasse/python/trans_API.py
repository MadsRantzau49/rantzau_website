import dropbox

# Replace this with your Dropbox access token
ACCESS_TOKEN = "sl.Bxo0D6hXtxDtjbgv2P9J6amFO7HQ8FD_B8FegfGEDbPWZ9InAA_rmpnM4acth75A7SJxSPQhWuFcVa4e0AcR1Ei51y7ahLmJvQCEWk_uc5aB9oZ8e_PmeWmhayONaqVCAUOH689Mmr7N4Hp4DkW6Xdc"

# Specify the path to the directory you want to check
DIRECTORY_PATH = "/your/directory/path"

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# List files in the specified directory
try:
    result = dbx.files_list_folder(DIRECTORY_PATH)
    files = result.entries

    # Find the latest uploaded file
    if files:
        latest_file = max(files, key=lambda x: x.server_modified)
        print("Latest uploaded file:", latest_file.name)
        print("File metadata:", latest_file)
    else:
        print("No files found in the specified directory.")

except dropbox.exceptions.ApiError as e:
    print("Error fetching files from Dropbox:", e)
