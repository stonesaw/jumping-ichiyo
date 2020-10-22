from PIL import Image
from lib.my_error import MakerFailed
from lib.maker_base import Stage, MonoSprite, LoadSprite



"""gif画像を生成するクラス"""
class Maker:
    stage = Stage(width=360, height=640, color=(160, 161, 254))
    sprite = LoadSprite(["image/ichiyo00.png", "image/ichiyo01.png"], resize=(100, 100))
    
    # put block
    block = LoadSprite("image/block.png")
    __resize_h = int((stage.height - stage.ground) / 2)
    __resize_w =  int(block.width * __resize_h / block.height)
    block.image = block.image.resize((__resize_w, __resize_h))
    __x, __y = 0, 0
    for __y in range(2):
        for __x in range(int(stage.width / __resize_w) + 1):
            stage.image.paste(block.image, (__x*__resize_w, int(stage.ground) + __y*__resize_h))


    """[!] ここに直接eqを入れると危険なので、必ずパーサーを通してから引数を入れる"""
    @classmethod
    def make(cls, eq: list, var: dict, times: int, self_range: str) -> None:
        gif = []

        print(">>> Maker running ...")

        # GIF画像作成のメインループ
        for var["t"] in range(times):
            for i in range(len(eq)):
                # TODO ここのチェックもパーサーへ    
                try:
                    exec("import math; " + eq[i], {}, var)
                except Exception as e:
                    raise e
            
            # TODO パーサーでキーワードのチェック
            if self_range == "default": # 地面より上
                var["y"] = min([cls.stage.ground - cls.sprite.height, var["y"]])
            elif self_range == "lock": # 画面内かつ地面より上
                var["x"] = min([cls.stage.width - cls.sprite.width, max([var["x"], 0])])
                var["y"] = min([cls.stage.ground - cls.sprite.height, max([var["y"], 0])])
            elif self_range == "display": # 画面内
                var["x"] = min([cls.stage.width - cls.sprite.width, max([var["x"], 0])])
                var["y"] = min([cls.stage.height - cls.sprite.height, max([var["y"], 0])])
            elif self_range == "free": # 制限なし
                pass
                
            back = cls.stage.image.copy()

            # スプライトのy座標(高さ)によってスプライトをアニメーションする
            splited_y = int(int(var["y"]) * len(cls.sprite.images) / int(cls.stage.ground)) # 表示する画像を変える
            splited_y = max([0, min(splited_y, len(cls.sprite.images))])
            img = cls.sprite.images[len(cls.sprite.images) - 1 - splited_y]
            back.paste(img, (int(var["x"]), int(var["y"])), img)
            
            gif.append(back)

        gif[0].save("image/jump.gif", save_all=True, append_images=gif[1:], optimize=False, duration=60, loop=0, quaulity=100)
        print("<<< Maker complete!\n")
