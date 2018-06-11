# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import cv2
import os
import random
import time

#number
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# 小写字母
t = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

char_set = []
for i in t:
    char_set.append(i)
for i in number:
    char_set.append(i)

CHAR_SET_LEN = len(char_set)

image_filename_list = []
total = 0

# 图像大小
IMAGE_HEIGHT = 60  #80
IMAGE_WIDTH = 160  #250
MAX_CAPTCHA = 8

def get_image_file_name(imgFilePath):
    fileName = []
    total = 0
    for filePath in os.listdir(imgFilePath):
        captcha_name = filePath.split('/')[-1]
        fileName.append(captcha_name)
        total += 1
    random.seed(time.time())
    # 打乱顺序
    random.shuffle(fileName)
    return fileName, total

# 获取训练数据的名称列表
image_filename_list, total_train = get_image_file_name('./train_data')

# 获取测试数据的名称列表
image_filename_list_valid, total_test = get_image_file_name('./test_data')

# 读取图片和标签
def gen_captcha_text_and_image(imageFilePath, image_filename_list,imageAmount):
    num = random.randint(0, imageAmount - 1)
    # print(os.path.join(imageFilePath, image_filename_list[num]))
    img = cv2.imread(os.path.join(imageFilePath, image_filename_list[num]), 0)
    img = cv2.resize(img,(160,60))
    img = np.float32(img)
    text = image_filename_list[num].split('.')[0]
    return text, img

def name2label(name):
    label = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    for i, c in enumerate(name):
        idx = i * CHAR_SET_LEN + ord(c) - ord('0')
        label[idx] = 1
    return label


# label to name
def label2name(digitalStr):
    digitalList = []
    for c in digitalStr:
        digitalList.append(ord(c) - ord('0'))
    return np.array(digitalList)

# 文本转向量
def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('验证码最长5个字符')
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

    def char2pos(c):
        if c == '_':
            k = 62
            return k
        k = ord(c) - 48
        if k > 9:
            k = ord(c) - 55
            if k > 35:
                k = ord(c) - 61
                if k > 61:
                    raise ValueError('No Map')
        return k

    for i, c in enumerate(text):
        idx = i * CHAR_SET_LEN + char2pos(c)
        vector[idx] = 1
    return vector


# 向量转回文本
def vec2text(vec):
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i  # c/63
        char_idx = c % CHAR_SET_LEN
        if char_idx < 10:
            char_code = char_idx + ord('0')
        elif char_idx < 36:
            char_code = char_idx - 10 + ord('A')
        elif char_idx < 62:
            char_code = char_idx - 36 + ord('a')
        elif char_idx == 62:
            char_code = ord('_')
        else:
            raise ValueError('error')
        text.append(chr(char_code))
    return "".join(text)


# 生成一个训练batch
def get_next_batch(imageFilePath, image_filename_list=None, batch_size=128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])

    def wrap_gen_captcha_text_and_image(imageFilePath, imageAmount):
        while True:
            text, image = gen_captcha_text_and_image(imageFilePath, image_filename_list, imageAmount)
            if image.shape == (60, 160):
                return text, image

    for listNum in os.walk(imageFilePath):
        pass
    imageAmount = len(listNum[2])

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image(imageFilePath, imageAmount)

        batch_x[i, :] = image.flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y

# 占位符，X和Y分别是输入训练数据和其标签，标签转换成8*10的向量
X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA * CHAR_SET_LEN])
# 声明dropout占位符变量
keep_prob = tf.placeholder(tf.float32)  # dropout


# 定义CNN
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):

    # 把 X reshape成 IMAGE_HEIGHT*IMAGE_WIDTH*1的格式，输入的是灰度图
    # reshape shape 中的 -1 表示数量不定，根据实际情况获取，在本例中是 每轮迭代的输入的图像数量 batchsize大小
    x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])

    # 3 conv layer 开始搭建卷积神经网络

    # shape(3,3,1,32) 前面两个参数是 卷积核的尺寸大小 patch
    # 第三个参数是通道数 第四个参数是该层卷积核的数量，有多少个卷积核就会输出多少个卷积特征图像
    w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))

    # 每个卷积核都配置一个偏置量，该层有多少个输出，就应该配置多少个偏置量
    b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))

    # 图片和卷积核卷积，并加上偏执量，卷积结果28x28x32
    # tf.nn.conv2d()实现卷积操作 其中的padding用于设置卷积操作对边缘像素的处理方式，在tf中有VALID和SAME两种模式
    # padding='SAME'会对图像边缘补0,完成图像上所有像素（特别是边缘象素）的卷积操作
    # padding='VALID'会直接丢弃掉图像边缘上不够卷积的像素
    # strides：卷积时在图像每一维的步长，是一个一维的向量，长度4，并且strides[0]=strides[3]=1
    # tf.nn.bias_add() 函数的作用是将偏置项b_c1加到卷积结果value上去

    # tf.nn.relu()函数式relu激活函数，实现输出结果的非线性转换，即features=max(features, 0)，输出tensor的形状和输入一致

    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))

    # 下面是池化层操作，选择的是最大池化，作用是 进一步提取图像的抽象特征，并且降低维度
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    # 失活层，为了防止或者减轻过拟合而使用的函数，一般用在全连接层
    conv1 = tf.nn.dropout(conv1, keep_prob)


    # 第二个卷积层
    w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)
    # 原图像HEIGHT = 60 WIDTH = 160，经过神经网络第一层后输出大小为 30*80*32
    # 经过神经网络第二层运算后输出为 16*40*64


    # 搭建第三层卷积层
    w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    # 原图像HEIGHT = 60 WIDTH = 160，经过神经网络第一层后输出大小为 30*80*32 经过第二层后输出为 16*40*64
    # 经过神经网络第二层运算后输出为 16*40*64

    # Fully connected layer 全连接层
    w_d = tf.Variable(w_alpha * tf.random_normal([8 * 20 * 64, 1024]))
    b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, keep_prob)

    # 最后的输出层
    w_out = tf.Variable(w_alpha * tf.random_normal([1024, MAX_CAPTCHA * CHAR_SET_LEN]))
    b_out = tf.Variable(b_alpha * tf.random_normal([MAX_CAPTCHA * CHAR_SET_LEN]))
    out = tf.add(tf.matmul(dense, w_out), b_out)
    # out = tf.nn.softmax(out)
    return out


# 训练
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # loss
    # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, Y))
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    # optimizer 为了加快训练 learning_rate应该开始大，然后慢慢减小
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        step = 0
        while True:
            batch_x, batch_y = get_next_batch('./train_data', image_filename_list=image_filename_list,batch_size=128)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            print(step, loss_)
            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch('./test_data',image_filename_list=image_filename_list_valid,batch_size= 128)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc)

                # 训练结束条件
                if acc > 0.94 or step > 3000:
                    saver.save(sess, "./crack_capcha.model", global_step=step)
                    break
            step += 1


def predict_captcha(captcha_image):
    output = crack_captcha_cnn()

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('.'))

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

        text = text_list[0].tolist()
        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * CHAR_SET_LEN + n] = 1
            i += 1
        return vec2text(vector)

        # 执行训练


train_crack_captcha_cnn()
print("训练完成，开始测试…")