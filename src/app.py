# -*- coding: UTF-8 -*-

from eyes import Eyes

eyes = Eyes()

while True:
    # 普通
    eyes.set_nomal()
    # 怒り
    for level in range(1,11,1):
        eyes.set_anger(level)
    for level in range(10,0,-1):
        eyes.set_anger(level)
    # 普通
    eyes.set_nomal()
    # 驚き
    for level in range(5,0,-1):
        eyes.set_surprized(level)
    for level in range(1,6,1):
        eyes.set_surprized(level)
