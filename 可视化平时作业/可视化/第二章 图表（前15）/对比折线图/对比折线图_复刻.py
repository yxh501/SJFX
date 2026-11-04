# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['13 对比折线图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge, Polygon, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
BG='#1A1E43'; BLUE='#0070C0'; RED='#E74E69'; YELLOW='#F5C353'; TEAL='#11A7AD'
def canvas(h=740):
    global fig,ax,H
    H=h
    fig=plt.figure(figsize=(10,h/100),dpi=120,facecolor=BG)
    ax=fig.add_axes([0,0,1,1],xlim=(0,1000),ylim=(h,0),facecolor=BG)
    ax.set_axis_off()
def text(x,y,s,size=13,color='white',ha='left',**kw):
    return ax.text(x,y,str(s),fontsize=size,color=color,ha=ha,va='center',**kw)
def rect(x,y,w,h,color,**kw):
    ax.add_patch(Rectangle((x,y),w,h,facecolor=color,edgecolor='none',**kw))
def header(title,subtitle='',note='*注：数据来源于公司销售系统，统计日期截至2022.06.30'):
    t=text(62,72,title,30,fontweight='bold')
    fig.canvas.draw()
    width=t.get_window_extent(fig.canvas.get_renderer()).width
    if width>fig.bbox.width*.9:t.set_fontsize(30*fig.bbox.width*.9/width)
    if subtitle:
        t=text(62,126,subtitle,18)
        fig.canvas.draw()
        width=t.get_window_extent(fig.canvas.get_renderer()).width
        if width>fig.bbox.width*.9:t.set_fontsize(18*fig.bbox.width*.9/width)
    if note: text(48,H-30,note,11,color='#D9D9D9')
def baseline(y=620,x0=95,x1=910):
    ax.plot([x0,x1],[y,y],color='#686A80',lw=.7)
def bar(x,v,scale,base=620,width=38,color=BLUE,label=True):
    rect(x-width/2,base-v*scale,width,v*scale,color)
    if label:text(x,base-v*scale-18,f'{v:g}',12,ha='center')
def finish():
    wb.close()
    fig.savefig(HERE/(Path(__file__).stem+'.png'),dpi=120,facecolor=BG)
    plt.close(fig)
if False:  # 此文件所有数值均来自上面的 ws/col，未嵌入 Excel 截图。
    pass

canvas(750)
months=col('B',3,8); v21=col('C',3,8);v22=col('D',3,8)
header('2022年上半年各月同比去年销量','上半年同比去年增长明显，5月份同比增长最多，增长近40%')
xs=np.linspace(195,885,6);base=630;scale=.12
for v in range(0,3001,500):
    y=base-v*scale;ax.plot([115,955],[y,y],color='#454866',lw=.6,ls='--');text(100,y,v,11,ha='right')
for vals,other,c in [(v21,v22,RED),(v22,v21,BLUE)]:
    ys=base-np.array(vals)*scale
    ax.plot(xs,ys,color=c,lw=1.5,marker='o',ms=4)
    for x,y,v,o in zip(xs,ys,vals,other):text(x,y+(-25 if v>o else 25),v,12,ha='center')
for x,m in zip(xs,months):text(x,base+30,m,13,ha='center')
for x,c,label in [(665,RED,'2021年'),(810,BLUE,'2022年')]:
    ax.plot([x,x+40],[218,218],color=c,lw=1.5,marker='o',ms=3);text(x+47,218,label,12)

finish()
