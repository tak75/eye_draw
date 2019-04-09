# -*- coding: UTF-8 -*-

# import math
# import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# Pillow(PIL)はPythonの画像処理ライブラリ。OpenCVのような複雑処理はできないが、シンプルで使いやすい。
# Pillowは開発が停止しているPIL(Python Image Library)からフォークされたライブラリ。
# pillow か PIL のどちらか一方のみがインストールされた環境でないと使えない。
# import する場合はどちらも from PIL となるようなので要注意。
from PIL import Image
# from PIL import ImageFont
from PIL import ImageDraw

from eye import Eye

class Eyes:
    """
    両目描画クラス

    【責務】
    ・両目を描画する
    """

    def __init__(self):
        """ 
        コンストラクタが呼ばれた後に呼ばれるメソッド
        """
        # Raspberry Pi pin configuration:
        RST = 24

        # 128x64 display with hardware I2C:
        self.__disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

        # Initialize library.
        self.__disp.begin()

        # Get display width and height.
        self.__width = self.__disp.width
        self.__height = self.__disp.height

        # Clear display.
        self.__disp.clear()
        self.__disp.display()

        # Create image buffer.
        # Make sure to create image with mode '1' for 1-bit color.
        self.__image = Image.new('1', (self.__width, self.__height))

        # Create drawing object.
        self.__draw = ImageDraw.Draw(self.__image)
        # Clear image buffer by drawing a black filled box.
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)
        # Draw the image buffer.
        self.__disp.image(self.__image)
        self.__disp.display()

        # 左右の目のインスタンスを作成
        # ここでの左右はディスプレイとしての左右であり、顔としての左右とは逆である
        self.__eye_l = Eye()
        self.__eye_r = Eye()

        self.set_nomal()

    def set_nomal(self):
        """ 
        通常の目を描画
        """
        self.__eye_l.set_white_eye(30,32,60,60)
        self.__eye_l.set_black_eye(0,10,30)
        self.__eye_l.set_eyelid(0,0,0,0)
        self.__eye_l.draw(self.__draw)

        self.__eye_r.set_white_eye(96,32,60,60)
        self.__eye_r.set_black_eye(0,10,30)
        self.__eye_r.set_eyelid(0,0,0,0)
        self.__eye_r.draw(self.__draw)

        self.__disp.image(self.__image)
        self.__disp.display()

    def set_anger(self, level):
        """ 
        怒った目を描画

        :param int level: 怒りのレベル（1～10）
        """

        if level<1: level=1
        elif level>10: level=10

        rate_out = 0.1*level/2
        rate_in = 0.2*level/3

        # 描画領域クリア
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)

        self.__eye_l.set_eyelid(rate_out,rate_in,0.1,0.1)
        self.__eye_l.draw(self.__draw)

        self.__eye_r.set_eyelid(rate_in,rate_out,0.1,0.1)
        self.__eye_r.draw(self.__draw)

        self.__disp.image(self.__image)
        self.__disp.display()

    def set_surprized(self, level):
        """ 
        驚いた目を描画

        :param int level: 驚きのレベル（1～5）
        """

        if level<1: level=1
        elif level>5: level=5

        size = 50 + level*3

        # 描画領域クリア
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)

        self.__eye_l.set_white_eye(30,32,size,size)
        self.__eye_l.draw(self.__draw)

        self.__eye_r.set_white_eye(96,32,size,size)
        self.__eye_r.draw(self.__draw)

        self.__disp.image(self.__image)
        self.__disp.display()

    def set_black_eyes(self, dir_vec, rate):
        """ 
        目を動かす

        :param vector dir_vec: 方向単位ベクトル
        :param float rate: 比率
        """

        if rate<-1: rate=-1
        elif rate>1: rate=1

        # 描画領域クリア
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=0)

        self.__eye_l.set_black_eye(30,32,size,size)
        self.__eye_l.draw(self.__draw)

        self.__eye_r.set_white_eye(96,32,size,size)
        self.__eye_r.draw(self.__draw)

        self.__disp.image(self.__image)
        self.__disp.display()

