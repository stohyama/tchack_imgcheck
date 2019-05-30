class ImageInformation:
    def __init__(self, image, image_base64, google_vison_api_json, item_code):
        self._image = image
        self._image_base64 = image_base64
        self._google_vison_api_json = google_vison_api_json
        self._item_code = item_code

    @property
    def image(self):
        return self._image

    @property
    def image_base64(self):
        return self._image_base64

    @property
    def google_vison_api_json(self):
        return self._google_vison_api_json

    @property
    def item_code(self):
        return self._item_code
