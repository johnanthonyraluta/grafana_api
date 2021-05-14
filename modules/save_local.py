import shutil

def file_save():
    with open("destination.png", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)