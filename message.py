# about
# info
# help_list[make, eq, eq-math, vat, times, range]


about = """
```md
  Jumping Ichiyo
==================
< about >
Ichiyoを数式で動かそう！(笑)
IchiyoがジャンプするGIF画像を作成します
式や変数を変えられます

< command >
* jump
    - make
        * sub-cmd[]  説明        ( デフォルト値 )
        - eq[]       式          ( y = 0.5*g*t*t - v0*t + ground )
        - var[]      変数        ( t = 0, g = 9.8, v0 = 80, x, y, ground )
        - times[]    ループ回数  ( times ≦ 50 )
        - range[]    表示範囲    ( above-ground )
    - last
    - help
        - make
        - eq
        - eq-math  editing
        - var
        - times
        - range
    - info

< tutorial >
1. jump make    (send default gif-image)
2. jump make eq[y = 0.5*g*t*t - v0*t + ground]
3. jump make eq[y = 0.5*g*t*t - v0*t + ground] var[v0 = 50]
4. jump make eq[y = -300 * (1-(1-sin(pi*t*0.03)^3)) + ground]
```
"""



info = """
```md
  Jumping Ichiyo
==================
<repo: https://github.com/stonesaw/jumping-ichiyo>
<lang: Python3>
<lib: discord.py Pillow>

Prod. Sou
```
"""



help_list = {
"make": """
```md
< make help >
与えられた式や変数によってGIF画像を作ります
makeコマンドは、jump make のキーワードと eq[] 、var[] などのサブコマンドで構成されます

        jump make sub_cmd1[...] sub_cmd2[...]
複数行で書くこともできます        
        jump make sub_cmd1[...]
        sub_cmd2[...]

tips: 'jump make'は常にデフォルトのGIF画像を送ります
```
""",


"eq": """
```md
< eq help >
式を指定します
二つ以上の式を指定する場合は , で区切ります

        eq[eq1, eq2 ...]
    ex) eq[y = sin(t)*-200 + ground]
    ex) eq[y = sin(t)*-200 + ground, x = t*5]

[!] 座標系は左上が(0, 0)で右下に行くほどプラスされます
default: y = 0.5*g*t*t - v0*t + ground

* sin, cosなどの詳しいヘルプは 'jump help eq-math' を見てね
```
""",


"eq-math": """
```md
< eq-math help >
式の記法についてもうちょっと...

*editing now ...*

```
""",


"var": """
```md
< var help >
変数を定義します
既に定義されている`g`や`v0`を再定義することも出来ます
    
        var[name=float(value), name2=float(value2) ...]
    ex) var[g = 4.8, v0 = 50]
    ex) jump make eq[y = 0.5*g*t^2 - up + ground] var[up = 100]

default: [t = 0, g = 9.8, v0 = 80, x, y, ground]
- x       Ichiyoの x座標
- y       Ichiyoの y座標
- ground  地面の高さ
```
""",


"times": """
```md
< times help >
GIF画像を作るときのループ回数を設定します
1 ~ 50の間で指定してください

        times[int]
    ex) times[20]

default: 50
```
""",


"range": """
```md
< range help >
Ichiyoを表示する範囲を指定します

        range[key-word]
    ex) range[free]

rangeコマンドのキーワードは以下の通りです

- default    地面より上
- free       どこまでも...
- lock       地面より上、x方向は、画面上のみ
- display    画面上
```
"""
}
