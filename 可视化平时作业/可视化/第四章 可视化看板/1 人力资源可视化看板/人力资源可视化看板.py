# -*- coding: utf-8 -*-
"""从教材明细读取数据，生成公司人员结构看板。依赖 openpyxl、matplotlib。"""
from collections import Counter
from pathlib import Path
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import font_manager
import openpyxl

HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第四章 人力资源可视化看板.xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('未找到教材中的第四章 人力资源可视化看板.xlsx')
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    book = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
    rows = [r[:8] for r in book['202203人员基础信息'].iter_rows(min_row=2, values_only=True) if r[0] is not None]
    book.close()
counts = {i: Counter(r[i] for r in rows) for i in range(2, 8)}
assert all(sum(counts[i].values()) == len(rows) for i in [2, 3, 4, 5, 7])
fonts = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams['font.sans-serif'] = [f for f in ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'Arial Unicode MS'] if f in fonts] or ['sans-serif']
plt.rcParams['axes.unicode_minus'] = False
BG, PANEL, WHITE, LIGHT = '#303D7A', '#1F2549', '#F5F5FA', '#77D4F7'
fig = plt.figure(figsize=(12, 6.5), facecolor=BG)

def text(x, y, value, size=12, align='center', weight='normal'):
    fig.text(x/1200, 1-y/650, str(value), color=WHITE, fontsize=size,
             ha=align, va='center', fontweight=weight)

def panel(x, y, w, h):
    fig.patches.append(Rectangle((x/1200, 1-(y+h)/650), w/1200, h/650,
                                 transform=fig.transFigure, facecolor=PANEL, edgecolor='none', zorder=-1))

def donut(x, y, labels, values, colors, legend_x, legend_y, spacing=29):
    ax = fig.add_axes([(x-60)/1200, 1-(y+60)/650, 120/1200, 120/650])
    ax.pie(values, colors=colors, startangle=90, counterclock=False, radius=1,
           wedgeprops={'width':.25, 'edgecolor':'none'}, autopct=lambda p:f'{p:.0f}%',
           pctdistance=1.32, textprops={'color':WHITE, 'fontsize':10.5})
    ax.set_aspect('equal')
    for i,(label,color) in enumerate(zip(labels,colors)):
        yy=legend_y+i*spacing
        fig.patches.append(Rectangle((legend_x/1200,1-(yy+4)/650),8/1200,8/650,transform=fig.transFigure,facecolor=color,edgecolor='none'))
        text(legend_x+12,yy,label,10.5,'left')

def horizontal(x, y, labels, values, width, step):
    limit=max(values)*1.12
    for i,(label,v) in enumerate(zip(labels,values)):
        yy=y+i*step;bar=width*v/limit
        text(x-13,yy,label,10.5,'right')
        fig.patches.append(Rectangle((x/1200,1-(yy+7)/650),bar/1200,14/650,transform=fig.transFigure,facecolor=LIGHT,edgecolor='none'))
        text(x+bar+12,yy,v,10.5,'left')

text(600,35,'公司人员结构看板',22,weight='bold')
for x,w in [(24,361),(412,368),(806,362)]:
    panel(x,69,w,220);panel(x,312,w,312)
for x,title in [(204,'年龄'),(596,'性别'),(987,'婚姻状况')]:text(x,100,title,16,weight='bold')
age=['18-24','25-29','30-34','35-39','40=<']
donut(165,205,age,[counts[7][v] for v in age],['#00B0E0','#F27F2D',LIGHT,'#F5AE25','#0070B8'],304,137)
donut(568,205,['男','女'],[counts[2]['男'],counts[2]['女']],['#F5AE25','#0070B8'],748,190,30)
donut(953,205,['单身','已婚','离异'],[counts[4][v] for v in ['单身','已婚','离异']],['#F5AE25','#0070B8',LIGHT],1108,175,32)
text(204,346,'学历',16,weight='bold')
# 教材汇总 K24/K25 的 COUNTIFS 条件互换；此处按员工明细的实际学历计数。
education=['博士研究生','硕士研究生','本科','专科','专科以下']
horizontal(123,407,education,[counts[3][v] for v in education],195,43)
text(596,351,f'总人数：{len(rows)}',17,weight='bold')
text(596,402,'入转调',16,weight='bold')
for x,label in zip([484,591,698],['入职','转入','转出']):
    v=counts[6][label];height=113*v/max(counts[6][k] for k in ['入职','转入','转出'])
    fig.patches.append(Rectangle(((x-17)/1200,1-576/650),34/1200,height/650,transform=fig.transFigure,facecolor=LIGHT,edgecolor='none'))
    text(x,576-height-20,v,10.5);text(x,600,label,11)
text(987,346,'部门',16,weight='bold')
departments=['财务部','人力资源部','行政部','信息技术部','研发部','销售部']
horizontal(904,404,departments,[counts[5][v] for v in departments],216,36)
output=HERE/(Path(__file__).stem+'.png')
fig.savefig(output,dpi=200,facecolor=BG)
plt.close(fig)
print(output)
