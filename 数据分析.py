import json
import random
import requests
import time
import pandas as pd
import os
from pyecharts import Bar,Geo,Line,Overlap
import jieba
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, ImageColorGenerator,STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

## 可以直接读取我们已经爬到的数据进行分析
avenger_com = pd.read_excel('D:\Python\复仇者联盟无限战争\复仇者联盟无限战争.xlsx')
grouped = avenger_com.groupby(['city'])
grouped_pct = grouped['score']

## 全国热力图
city_com = grouped_pct.agg(['mean', 'count'])
city_com.reset_index(inplace=True)
city_com['mean'] = round(city_com['mean'], 2)
data = [(city_com['city'][i], city_com['count'][i]) for i in range(0, city_com.shape[0])]
geo = Geo('《复仇者联盟无限战争》全国热力图', title_color="#fff",
          title_pos="center", width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, type="heatmap", visual_range=[0, 200],
        visual_text_color="#fff", symbol_size=10, is_visualmap=True,
        is_roam=False)
geo.render('复仇者联盟无限战争全国热力图.html')

## 主要城市评论数与评分
city_main = city_com.sort_values('count', ascending=False)[0:20]
attr = city_main['city']
v1 = city_main['count']
v2 = city_main['mean']
line = Line("主要城市评分")
line.add("城市", attr, v2, is_stack=True, xaxis_rotate=30, yaxis_min=4.2,
         mark_point=['min', 'max'], xaxis_interval=0, line_color='lightblue',
         line_width=4, mark_point_textcolor='black', mark_point_color='lightblue',
         is_splitline_show=False)

bar = Bar("主要城市评论数")
bar.add("城市", attr, v1, is_stack=True, xaxis_rotate=30, yaxis_min=4.2,
        xaxis_interval=0, is_splitline_show=False)
overlap = Overlap()
# 默认不新增 x y 轴，并且 x y 轴的索引都为 0
overlap.add(bar)
overlap.add(line, yaxis_index=1, is_add_yaxis=True)
overlap.render('主要城市评论数_平均分.html')

## 主要城市评分降序
city_score = city_main.sort_values('mean', ascending=False)[0:20]
attr = city_score['city']
v1 = city_score['mean']
line = Line("主要城市评分")
line.add("城市", attr, v1, is_stack=True, xaxis_rotate=30, yaxis_min=4.2,
         mark_point=['min', 'max'], xaxis_interval=0, line_color='lightblue',
         line_width=4, mark_point_textcolor='black', mark_point_color='lightblue',
         is_splitline_show=False)
line.render('主要城市评分.html')

## 主要城市评分全国分布
city_score_area = city_com.sort_values('count', ascending=False)[0:30]
city_score_area.reset_index(inplace=True)
data = [(city_score_area['city'][i], city_score_area['mean'][i]) for i in range(0,
                                                                                city_score_area.shape[0])]
geo = Geo('《复仇者联盟无限战争》全国主要城市打分图', title_color="#fff",
          title_pos="center", width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, visual_range=[4.4, 4.8],
        visual_text_color="#fff", symbol_size=15, is_visualmap=True,
        is_roam=False)
geo.render('复仇者联盟无限战争全国主要城市打分图.html')


## 绘制词云
avenger_str = ' '.join(avenger_com['comment'])
words_list = []
word_generator = jieba.cut_for_search(avenger_str)
for word in word_generator:
    words_list.append(word)
words_list = [k for k in words_list if len(k) > 1]
back_color = plt.imread('D:\Python\复仇者联盟无限战争\钢铁侠.jpg')  # 解析该图片
wc = WordCloud(background_color='white',  # 背景颜色
               max_words=200,  # 最大词数
               mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=300,  # 显示字体的最大值
               font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
               random_state=42,  # 为每个词返回一个PIL颜色
               )
avenger_count = Counter(words_list)
wc.generate_from_frequencies(avenger_count)
# 基于彩色图像生成相应彩色
image_colors = ImageColorGenerator(back_color)
# 绘制结果
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
plt.show
wc.to_file('词云图.jpg')