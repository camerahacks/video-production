###
# Script to create the folder structure that I use to manage files/bins
# when creating a video. First thing I do when I start a new video project
# is to download and run this script on the root of the project folder.
###

import os

# List of main folders and their subfolders
folders = [
        {"name":"Art", "subfolders":[]}, # Logos, SVGs
        {"name":"Video", "subfolders":["B-roll"]},  # Main video folder
        {"name":"Photos", "subfolders":[]}, # Photos
        {"name":"Screencapture", "subfolders":["Screenshots", "Recordings"]}, # Screencapture and screenshots
        {"name":"Graphics", "subfolders":[]}, # Composites, Charts, In video graphics
        {"name":"Thumbnail", "subfolders":[]}, # Thumbnail
        {"name":"Deliver", "subfolders":[]}] # Deliver for final video, transcript, and chapters

print("Creating folders:\n")

# Loop over main folders and create them
for folder in folders:
    os.makedirs(folder['name'], exist_ok=True)
    print(folder['name'])
    if(folder['subfolders']):
        for subf in folder['subfolders']:
            print("  "+subf)
            os.makedirs(os.path.join(folder['name'], subf), exist_ok=True)

print("Folders created successfully!")
