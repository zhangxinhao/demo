# 画一个1-5的折线图
import matplotlib.pyplot as plt
import numpy as np


def draw():
    x = np.arange(1, 6)
    y = x ** 2
    plt.plot(x, y)
    plt.show()


# 画一个柱状图，显示1-5的平方
def draw_bar():
    x = np.arange(1, 6)
    y = x ** 2
    plt.bar(x, y)
    plt.show()


if __name__ == '__main__':
    draw()
    draw_bar()
