import base64
from io import BytesIO
import os

class processImage(object):
    def __init__(self):
        pass

    def base64ToImage(self, image_name, image_content):
        with open("{}.jpg".format(image_name), "wb") as fh:
            fh.write(base64.decodebytes(image_content.encode()))

    def lineImageToBase64(self, image_content):
        data = bytes()
        for item in image_content:
            data += item
        encoded_string = base64.b64encode(data).decode('utf-8')
        return encoded_string

    def PILimageToBase64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def deleteImage(self, image_name):
        os.remove("{}.jpg".format(image_name))
        print("delete image : {}".format(image_name))
