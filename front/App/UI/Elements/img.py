from .div import div

# Maybe window.resources.images contains loaded images that we can just clone ?
# That way we can use window.resoures.audio for audio stuff
class img(div):
    def __init__(self, *args, img = "Default.png",**kwargs):
        super().__init__(*args, **kwargs)