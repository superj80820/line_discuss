import pyscreenshot as ImageGrab

class computerIO(object):
    def __init__(self):
        pass

    def screenshop(self):
        image = ImageGrab.grab()
        return image