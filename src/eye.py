# -*- coding: UTF-8 -*-

import numpy

from PIL import ImageDraw

class Eye:
    """
    片目描画クラス

    【責務】
    ・指示される寸法に従い、目の各部品を描画する
    """

    def __init__(self):
        """
        コンストラクタが呼ばれた後に呼ばれるメソッド
        """
        # --- 白目 ---
        #: 白目中心ベクトル
        self.__white_eye_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 白目左上ベクトル
        self.__white_eye_lt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 白目右下ベクトル
        self.__white_eye_rb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 白目幅
        self.__white_eye_size_w = 0
        #: 白目高さ
        self.__white_eye_size_h = 0

        # --- 黒目 ---
        #: 黒目中心ベクトル
        self.__black_eye_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 黒目左上ベクトル
        self.__black_eye_lt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 黒目右下ベクトル
        self.__black_eye_rb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 黒目直径
        self.__black_eye_size = 0

        # --- 上まぶた ---
        #: 上まぶた高さ比率左
        self.__upper_eyelid_rate_l = 0.0
        #: 上まぶた高さ比率右
        self.__upper_eyelid_rate_r = 0.0
        #: 上まぶた左上ベクトル
        self.__upper_eyelid_lt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 上まぶた左下ベクトル
        self.__upper_eyelid_lb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 上まぶた右上ベクトル
        self.__upper_eyelid_rt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 上まぶた右下ベクトル
        self.__upper_eyelid_rb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 上まぶた描画必要有無
        self.__need_upper_eyelid_draw = False

        # --- 下まぶた ---
        #: 下まぶた高さ比率左
        self.__lower_eyelid_rate_l = 0.0
        #: 下まぶた高さ比率右
        self.__lower_eyelid_rate_r = 0.0
        #: 下まぶた左上ベクトル
        self.__lower_eyelid_lt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 下まぶた左下ベクトル
        self.__lower_eyelid_lb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 下まぶた右上ベクトル
        self.__lower_eyelid_rt_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 下まぶた右下ベクトル
        self.__lower_eyelid_rb_vec = numpy.array([0,0,0], dtype=numpy.int)
        #: 下まぶた描画必要有無
        self.__need_lower_eyelid_draw = False

        # まぶた描画用変数を算出する
        self.__calc_eyelid()

    def set_white_eye(self, x, y, size_w, size_h):
        """ 
        白目パラメータを設定する

        :param int x: 白目中心x座標
        :param int y: 白目中心y座標
        :param int size_w: 幅[pix]
        :param int size_h: 高さ[pix]
        """
        self.__white_eye_vec = numpy.array([x, y, 0], dtype=numpy.int)
        self.__white_eye_lt_vec = self.__white_eye_vec + numpy.array([-size_w/2, -size_h/2, 0], dtype=numpy.int)
        self.__white_eye_rb_vec = self.__white_eye_vec + numpy.array([size_w/2, size_h/2, 0], dtype=numpy.int)
        self.__white_eye_size_w = size_w
        self.__white_eye_size_h = size_h

        # まぶた描画用変数を算出する
        self.__calc_eyelid()

    def set_black_eye(self, x, y, size):
        """ 
        黒目パラメータを設定する

        :param int x: 黒目中心x座標（白目中心からの相対座標）
        :param int y: 黒目中心y座標（白目中心からの相対座標）
        :param int size: 直径[pix]
        """
        self.__black_eye_vec = self.__white_eye_vec + numpy.array([x, y, 0], dtype=numpy.int)
        self.__black_eye_lt_vec = self.__black_eye_vec + numpy.array([-size/2, -size/2, 0], dtype=numpy.int)
        self.__black_eye_rb_vec = self.__black_eye_vec + numpy.array([size/2, size/2, 0], dtype=numpy.int)
        self.__black_eye_size = size

    def set_eyelid(self, upper_rate_l, upper_rate_r, lower_rate_l, lower_rate_r):
        """ 
        まぶたパラメータを設定する

        :param float upper_rate_l: 上まぶた高さ比率左
        :param float upper_rate_r: 上まぶた高さ比率右
        :param float lower_rate_l: 下まぶた高さ比率左
        :param float lower_rate_r: 下まぶた高さ比率右
        """
        self.__upper_eyelid_rate_l = upper_rate_l
        self.__upper_eyelid_rate_r = upper_rate_r
        self.__lower_eyelid_rate_l = lower_rate_l
        self.__lower_eyelid_rate_r = lower_rate_r

        # 左右とも0の場合は描画しない
        if upper_rate_l==0 and upper_rate_r==0:
            self.__need_upper_eyelid_draw = False
        else:
            self.__need_upper_eyelid_draw = True
        if lower_rate_l==0 and lower_rate_r==0:
            self.__need_lower_eyelid_draw = False
        else:
            self.__need_lower_eyelid_draw = True

        # まぶた描画用変数を算出する
        self.__calc_eyelid()

    def __calc_eyelid(self):
        """ 
        まぶた描画用変数を算出する
        """
        self.__upper_eyelid_lt_vec = self.__white_eye_lt_vec
        self.__upper_eyelid_lb_vec = self.__upper_eyelid_lt_vec + numpy.array([0, self.__white_eye_size_h * self.__upper_eyelid_rate_l, 0], dtype=numpy.int)
        self.__upper_eyelid_rt_vec = self.__upper_eyelid_lt_vec + numpy.array([self.__white_eye_size_w, 0, 0], dtype=numpy.int)
        self.__upper_eyelid_rb_vec = self.__upper_eyelid_rt_vec + numpy.array([0, self.__white_eye_size_h * self.__upper_eyelid_rate_r, 0], dtype=numpy.int)
        
        self.__lower_eyelid_lt_vec = self.__white_eye_lt_vec + numpy.array([0, self.__white_eye_size_h, 0], dtype=numpy.int)
        self.__lower_eyelid_lb_vec = self.__lower_eyelid_lt_vec + numpy.array([0, -self.__white_eye_size_h * self.__lower_eyelid_rate_l, 0], dtype=numpy.int)
        self.__lower_eyelid_rt_vec = self.__lower_eyelid_lt_vec + numpy.array([self.__white_eye_size_w, 0, 0], dtype=numpy.int)
        self.__lower_eyelid_rb_vec = self.__lower_eyelid_rt_vec + numpy.array([0, -self.__white_eye_size_h * self.__lower_eyelid_rate_r, 0], dtype=numpy.int)

    def draw(self, draw):
        """ 
        全パーツを描画する

        :param ImageDraw draw: Drawオブジェクト
        """
        # 白目
        draw.ellipse((self.__white_eye_lt_vec[0], self.__white_eye_lt_vec[1] , self.__white_eye_rb_vec[0], self.__white_eye_rb_vec[1]), outline=255, fill=255)
        # 黒目
        draw.ellipse((self.__black_eye_lt_vec[0], self.__black_eye_lt_vec[1] , self.__black_eye_rb_vec[0], self.__black_eye_rb_vec[1]), outline=0, fill=0)
        # 上まぶた
        if self.__need_upper_eyelid_draw==True:
            draw.polygon((  (self.__upper_eyelid_lt_vec[0], self.__upper_eyelid_lt_vec[1]),
                            (self.__upper_eyelid_lb_vec[0], self.__upper_eyelid_lb_vec[1]),
                            (self.__upper_eyelid_rb_vec[0], self.__upper_eyelid_rb_vec[1]),
                            (self.__upper_eyelid_rt_vec[0], self.__upper_eyelid_rt_vec[1])
                        ), outline=0, fill=0)
        # 下まぶた
        if self.__need_lower_eyelid_draw==True:
            draw.polygon((  (self.__lower_eyelid_lt_vec[0], self.__lower_eyelid_lt_vec[1]),
                            (self.__lower_eyelid_lb_vec[0], self.__lower_eyelid_lb_vec[1]),
                            (self.__lower_eyelid_rb_vec[0], self.__lower_eyelid_rb_vec[1]),
                            (self.__lower_eyelid_rt_vec[0], self.__lower_eyelid_rt_vec[1])
                        ), outline=0, fill=0)


