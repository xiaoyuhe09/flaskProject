import random

import matplotlib.pyplot as plt
import pandas as pd
import jieba
import jieba.analyse
import numpy as np
import xlrd
import asyncio
import math
from pyecharts import options as opts
from aiohttp import TCPConnector, ClientSession
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType
from pyecharts.charts import Pie, Bar, Map, WordCloud, Page, Liquid, Timeline, Radar, BMap, Geo, Map3D
from pyecharts.globals import CurrentConfig, NotebookType, BMapType, ChartType
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from PIL import Image
from wordcloud import wordcloud

CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

NationalForestCoverage = 23.04 / 100
MyAK = '4qoFwM1CEG9W5Q9sshA5tsh5ay0PpUwT'

# df为项目投入
df = pd.read_excel('../static/excel/项目投入丨新疆.xlsx')
df_ProjectName = df['项目']
df_StartTime = df['开始时间']
df_EndTime = df['截至统计时间']
df_ProjectInvestmentCapital = df['项目投入资金(亿元)']
df_AccumulatedAfforestationArea = df['累计造林面积(万公顷)']
df_FrontForestCoverageRate = df['森林覆盖率(%)前']
df_AfterForestCoverageRate = df['森林覆盖率(%)后']
# 投入产出得分
df_Input_Output = df_AccumulatedAfforestationArea / df_ProjectInvestmentCapital * 15.4
# 时间产出得分
df_TimeOutput = df_AccumulatedAfforestationArea / (df_EndTime - df_StartTime) / 1.657
# 森林覆盖率变化得分
df_ChangesInForestCover = (df_AfterForestCoverageRate - df_FrontForestCoverageRate) / df_FrontForestCoverageRate * 12.56

# df1
# df1为森林资源丨新疆
df1 = pd.read_excel('../static/excel/森林资源丨新疆.xls')
df1 = df1.T
# 森林资源丨新疆 统计年份
df1_Year = df1.iloc[1:, 0]
# 森林资源丨新疆 森林覆盖率
df1_Coverage = df1.iloc[1:, 3]
# 各城市名称
df1_Cities = df1.iloc[:1, 9:]
df1_Cities = df1_Cities.T
# # 森林覆盖率 水球图 新疆森林覆盖率/全国森林覆盖率
timeline1 = Timeline(init_opts=opts.InitOpts(chart_id='liquid'))

for i in range(len(list(df1_Year.index)) - 1, -1, -1):
    liquid = (
        Liquid()
        .add(df1_Year.index[i], [df1_Coverage.values[i] / 100,
                                 df1_Coverage.values[i] / 100],
             color=['#1a6840', '#1ba784'],
             background_color='#40a070',
             is_outline_show=False,
             label_opts=opts.LabelOpts(
                 font_size=40,
                 formatter=JsCode(
                     """function (param) {
                         return (Math.floor(param.value * 1000) / 10) + '%';
                     }"""
                 ),
                 position="inside"))
    )
    timeline1.add(liquid, df1_Year.index[i])

# 项目投入 雷达图
input_output = []
for i in range(len(list(df_Input_Output.values))):
    x = list(df_Input_Output.values)[i]
    input_output.append(round(x, 2))

time_output = []
for i in range(len(list(df_TimeOutput.values))):
    x = list(df_TimeOutput.values)[i]
    time_output.append(round(x, 2))

changesinforestcover = []
for i in range(len(list(df_ChangesInForestCover.values))):
    x = list(df_ChangesInForestCover.values)[i]
    changesinforestcover.append(round(x, 2))

totalscore = []
for i in range(len(list(df_Input_Output.values))):
    x = (input_output[i] + time_output[i] + changesinforestcover[i]) / 3
    totalscore.append(round(x, 2))

radar1_schema = []
for j in range(len(list(df_ChangesInForestCover.values))):
    xiao = {}
    xiao['name'] = df_ProjectName.values[j]
    xiao['max'] = 10
    xiao['min'] = 0
    radar1_schema.append(xiao)

rada1 = (
    Radar(init_opts=opts.InitOpts(chart_id='radar'))
    .set_colors(["#4587E7"])
    .add_schema(
        schema=radar1_schema,
        shape="circle",
        center=["50%", "50%"],
        radius="80%",
        angleaxis_opts=opts.AngleAxisOpts(
            min_=0,
            max_=360,
            is_clockwise=False,
            interval=5,
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        radiusaxis_opts=opts.RadiusAxisOpts(
            min_=0,
            max_=10,
            interval=2,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        polar_opts=opts.PolarOpts(),
        splitarea_opt=opts.SplitAreaOpts(is_show=False),
        splitline_opt=opts.SplitLineOpts(is_show=False),
    )
    .add(
        series_name="投入产出得分",
        data=[{"value": input_output, "name": "投入产出得分"}],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
        is_selected=False,
    )
    .add(
        series_name="时间产出得分",
        data=[{"value": time_output, "name": "时间产出得分"}],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
        is_selected=False,
    )
    .add(
        series_name="覆盖率变化得分",
        data=[{"value": changesinforestcover, "name": "覆盖率变化得分"}],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
        is_selected=False,
    )
    .add(
        series_name="总得分",
        data=[{"value": totalscore, "name": "总得分"}],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=1),
    )
)
# 城市绿化面积 地图

Bar_data = [
    ("克拉玛依", [84.77, 45.59, 100]),

]

map_3d = (
    Map3D(init_opts=opts.InitOpts(chart_id='map3d'))
    .add_schema(
        maptype="新疆",
        box_width=100,
        shading="Echarts GL",
        itemstyle_opts=opts.ItemStyleOpts(
            color="#ffd111",
            opacity=1,
            border_width=0.8,
            border_color="#1a94bc",
        ),
        map3d_label=opts.Map3DLabelOpts(
            is_show=False,
            formatter=JsCode("function(data){return data.name + " " + data.value[2];}"),
        ),
        emphasis_label_opts=opts.LabelOpts(
            is_show=False,
            color="black",
            font_size=10,
            background_color="rgba(0,23,11,0)",
        ),
        light_opts=opts.Map3DLightOpts(
            main_color="#fff",
            main_intensity=1.1,
            main_shadow_quality="ultra",
            is_main_shadow=True,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    )
    .add(
        series_name="城市绿化面积",
        data_pair=Bar_data,
        type_=ChartType.BAR3D,
        bar_size=1,
        shading="Echarts GL",
        label_opts=opts.LabelOpts(
            is_show=False,
            formatter=JsCode("function(data){return data.name + ' ' + data.value[2];}"),
        ),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title=""))
)

page = Page(layout=Page.DraggablePageLayout)
page.add(timeline1,rada1,map_3d)
page.render('presubpage.html')
Page.save_resize_html("presubpage.html", cfg_file="./json/subpage_chart_config.json", dest="subpage_charts.html")
