import base64
from io import BytesIO

class transmissionImage(object):
    def __init__(self):
        pass

    def base64ToImage(self, image_content):
        with open("../res/imageToSave.jpg", "wb") as fh:
            fh.write(base64.decodebytes(image_content.encode()))

    def PILimageToBase64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')