#coding:utf-8

from captcha.image import ImageCaptcha
import numpy as np
import random
import os
import cv2
from PIL import Image


# 验证码中的字符

# 数字
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# 小写字母
t = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# 大写字母
T = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

char_set = []
for i in t:
    char_set.append(i)
for i in number:
    char_set.append(i)


# 验证码长度为5个符
def random_captcha_text(char_set, captcha_size=5):
    """
    生成验证码字符串
    :param char_set: 候选集
    :param captcha_size: 验证码长度
    :return: 验证码字符串
    """
    captcha_text = []
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text

def gen_captcha_text_and_image():
    """
    生成验证码图片
    :return:
    """
    image = ImageCaptcha()
    captcha_text = random_captcha_text(char_set=char_set)
    captcha_text = ''.join(captcha_text)
    captcha = image.generate(captcha_text)
    captcha_image = Image.open(captcha)
    captcha_image = np.array(captcha_image)
    return captcha_text, captcha_image

def main():
    # 保存路径
    path = '/Users/lxp/spider/captcha_data/ceshi_data/'
    count = 10
    for i in range(count):
        text, image = gen_captcha_text_and_image()
        fullPath = os.path.join(path, text + ".jpg")
        cv2.imwrite(fullPath, image)
        print("{0}/{1}".format(i+1,count))
    print("\nDone!")

if __name__ == "__main__":
    main()
