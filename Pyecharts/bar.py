# -*- coding: UTF-8 -*-

"""
    Bar：柱状/条形图，通过柱形的高度/条形的宽度来表现数据的大小。
    1、user_theme('dark')
    pyecharts 支持更换主体色系
    2、add()
    主要方法，用于添加图表的数据和设置各种配置项
    3、print_echarts_options()
    打印输出图表的所有配置项
    4、render()
    默认将会在根目录下生成一个 render.html 的文件，支持 path 参数，设置文件保存位置，如 render(r"e:\my_first_chart.html")，文件用浏览器打开。

"""
from pyecharts import Bar


def iniBar():
    bar = Bar("我的第一个图表", "这里是副标题")
    bar.use_theme('dark')
    bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
    # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
    bar.render()  # 生成本地 HTML 文件
    bar.render(path='snapshot.png')


def __main__():
    iniBar()
