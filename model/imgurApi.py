from imgurpython import ImgurClient
import json


class imgurApi(object):
    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client = ImgurClient(self.client_id, self.client_secret, self.access_token, self.refresh_token)

    def upload(self, image_path):
        ret = self.client.upload_from_path(image_path)
        if ret.get("link"):
            return ret
        else:
            return False