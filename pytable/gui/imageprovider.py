import os.path as path

from PIL import ImageTk


# to do choix résolution
class ImageProvider:
    def __init__(self, root=""):
        self.root = root
        self.images = {}

    def build_image_path(self, name):
        return path.join(self.root, name + ".png")

    def get_image(self, name):
        image = None

        try:
            image = self.images[name]
        except KeyError:
            image = ImageTk.PhotoImage(file=self.build_image_path(name))
            self.images[name] = image

        return image
