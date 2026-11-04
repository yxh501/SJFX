# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(后15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(后15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['19 南丁格尔圆饼图']
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
names=col('B',3,8);vals=col('C',3,8)
header('2021年各部门人数分布','公司总人数1664，销售部人数最多451，占比29.2%','*注：数据来源于公司人力资源系统，统计日期截至2022.01.01')
cx,cy=500,435;outer=250; inner=0
colors=['#E74E69', '#F5C353', '#11A7AD', '#0070C0', '#37A2DA', '#7030A0']
start=-90
for i,(name,v,c) in enumerate(zip(names,vals,colors)):
    angle=v*360
    r=outer
    ax.add_patch(Wedge((cx,cy),r,start,start+angle,width=r-inner if inner else None,facecolor=c,edgecolor='none'))
    a=np.radians(start+angle/2); right=np.cos(a)>=0
    x=cx+(r+10)*np.cos(a);y=cy+(r+10)*np.sin(a)
    tx=750 if right else 250;ty=[260, 625, 640, 460, 315, 270][i]
    ax.plot([x,tx,tx+(110 if right else -110)],[y,ty,ty],color=c,lw=.7)
    ax.plot(x,y,'o',color=c,ms=3)
    # 原图引导线上未显示文字；沿用原图排版。
    start+=angle

finish()
