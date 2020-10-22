from PIL import Image
from lib.my_error import MakerFailed

# GIFのベースとなるステージ
class Stage:
    def __init__(self, width = 100, height = 100, color = (255, 255, 255), ground = None):
        self.width = width
        self.height = height
        self.color = color
        if ground is None:
            self.ground = self.height * 0.8
        else:
            self.ground = ground

        self.image = Image.new("RGB", (self.width, self.height), self.color)



# 単色の塗りつぶしのスプライト
class MonoSprite:
    def __init__(self, width=0, height=0, color=(0,0,0), resize=(0, 0)):
        self.mode = mode
        self.width = width
        self.height = height
        self.color = color
        self.image = Image.new("RGB", (self.width, self.height), self.color)


# 画像ファイルをロードしたスプライト
class LoadSprite:
    def __init__(self, path: list or str, resize=(0, 0)):
        if type(path) == str:
            path = [path]
        elif type(path) != list:
            raise MakerFailed("スプライトのロードに失敗しました")
        
        self.images = []
        for p in range(len(path)):
            self.images.append(Image.open(path[p]))
            if resize[0] > 0 and resize[1] > 0:
                self.images[p] = self.images[p].resize((resize[0], resize[1]))
        self.image = self.images[0]
        self.width, self.height = self.image.size[0], self.image.size[1]
