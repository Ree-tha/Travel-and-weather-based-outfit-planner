# utils/wardrobe.py

import os

WARDROBE_PATH = "data/wardrobe"

def get_uploaded_clothes():
    clothes = []
    if os.path.exists(WARDROBE_PATH):
        for filename in os.listdir(WARDROBE_PATH):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                clothes.append(filename)
    return clothes
