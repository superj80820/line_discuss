import base64

class processImage(object):
    def __init__(self):
        pass

    def base64ToImage(self, image_content):
        with open("imageToSave.jpg", "wb") as fh:
            fh.write(base64.decodebytes(image_content.encode()))

    def lineImageToBase64(self, image_content):
        data = bytes()
        for item in image_content:
            data += item
        encoded_string = base64.b64encode(data).decode('utf-8')
        return encoded_string