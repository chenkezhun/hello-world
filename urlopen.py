#!/usr/bin/python3
# -*- coding:UTF-8 -*-


from bs4 import BeautifulSoup
from urllib.request import urlopen
from pyecharts.charts import Map, Geo
from pyecharts import options as opts 
from pyecharts.globals import ThemeType

html = urlopen(
	"https://3g.dxy.cn/newh5/view/pneumonia_peopleapp"
).read().decode('utf-8')
# 获取html网页的源代码
bs = BeautifulSoup(html,"html.parser")
print(bs.body)

str1=bs.body.text
print(str1)
str1=str1[str1.find('window.getAreaStat = '):] # 查找字符串中指定国内省份对应数据的关键字，进行截取
data = str1[str1.find('[{'):str1.find('}catch')]
data_list = eval(data)  # 字符串转字典数组
print(type(data_list))
print(data_list)
new_dict = {} # 省份现存确诊数
new_dict1 = {} # 省份累计确诊数

# 循环遍历data_list取数据{省份：确诊数}
for province in data_list:
	# 将省份现存确诊数放入new_dict字典，处理不合格的省份名称replace
	new_dict[province['provinceName'].replace('自治区','').replace('回族','').replace('维吾尔','').replace('省','').replace('市','').replace('壮族','')] = province['currentConfirmedCount']
	# 省份累计确诊数
	new_dict1[province['provinceName'].replace('自治区','').replace('回族','').replace('维吾尔','').replace('省','').replace('市','').replace('壮族','')] = province['confirmedCount']

print(new_dict)
print(new_dict1)

province=list(new_dict.keys()) # 将字典中的省份key以列表的形式取出来
values=list(new_dict.values()) # 将字典中确诊数values以列表形式取出来
list1 = [[province[i],values[i]] for i in range(len(province))] # 此处用到了列表生成式
map_1 = Map() #Map()中，init_opts=opts.InitOpts(theme=ThemeType.ROMANTIC)设置主题，bg_color="#EBEBEB"设置地图背景颜色
map_1.set_global_opts(
	title_opts=opts.TitleOpts(title="中国nCoV肺炎疫情现存确诊",pos_left="left"),
	# visualmap_opts=opts.VisualMapOpts(max_=50),#最大数据范围
	visualmap_opts=opts.VisualMapOpts(
	is_piecewise=True, # 设置是否分段显示
	# 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式。例如
	pieces=[
	{"max":0, "label": "0人", "color": "#FFFFFF"},
	{"min": 1, "max": 9, "label": "1-10人", "color": "#FFEBCD"},
	{"min": 10, "max": 99, "label": "10-99人", "color": "#FFA07A"},
	{"min": 100, "max": 499, "label": "100-499人", "colr": "#FF4040"},
	{"min": 500, "max": 500, "label": "500-999人", "color": "#CD2626"},
	{"min": 1000, "max": 10000, "label": "100-10000人", "color": "#B22222"},
	{"min": 10000, "label": ">10000人", "color": "#8B1A1A"} # 不指定 max，表示 max 为无限大
	])
)
# maptype='china' 只显示全国直辖市和省级
# 数据只能是省名和直辖市的名称
map_1.add("中国现存确诊数据", list1, maptype="china", is_map_symbol_show=False)# is_map_symbol_show设置是否显示地图上的小红点
map_1.render("D:/疫情地图-中国累计确诊.html")

province1=list(new_dict1.keys()) # 将字典中的省份key以列表形式取出来
values1=list(new_dict1.values()) # 将字典中确诊数values以列表形式取出来
list2 = [[province1[i],values1[i]] for i in range(len(province1))] # 次处用到了列表生成式
map_2 = Map() # Map()中，init_opts=opts.InitOpts(theme=ThemeType.ROMANTIC)设置主题，bg_color="#EBEBEB"设置地图背景颜色
map_2.set_global_opts(
	title_opts=opts.TitleOpts(title="中国nCoV肺炎疫情确诊图",pos_left="left"),
	visualmap_opts=opts.VisualMapOpts(
	is_piecewise=True, # 设置是否分段显示
	# 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式。例如：
	pieces=[
	{"max":0,"label":"0人","color":"#FFFFFF"},
	{"min":1,"max":9,"label":"1-10人","color":"#FFFEBCD"},
	{"min":10,"max":99,"label":"10-99人","color":"#FFA07A"},
	{"min":100,"max":499,"label":"100-499人","color":"#EE5C42"},
	{"min":500,"max":999,"label":"500-999人","color":"#CD3333"},
	{"min":1000,"max":10000,"label":"1000-10000人","color":"#A52A2A"},
	{"min":10000,"label":">10000人","color":"#8B0000"} # 不指定 max，表示 max 为无限大
	])
)
map_2.add("中国确诊数据", list2,maptype="china", is_map_symbol_show=True) # is_map_symbol_show设置是否显示地图上的小红点
map_2.render("D:/疫情/中国地图-确诊.html")

