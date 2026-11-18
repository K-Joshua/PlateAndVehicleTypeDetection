import os

class picture_helper:
    
    def delete_jpeg_picture(file_path: str):

        if os.path.exists(file_path):
            os.remove(file_path)
            print("Image deleted.")
        else:
            print("Image does not exist.")