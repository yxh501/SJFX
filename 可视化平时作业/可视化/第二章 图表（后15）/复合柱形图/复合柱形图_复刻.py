# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(后15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(后15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['28 复合柱形图']
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

canvas(730)
rows=[r for r in range(3,18) if ws[f'B{r}'].value is not None]
months=[ws[f'B{r}'].value for r in rows];monthly=[ws[f'C{r}'].value for r in rows]
quarter=[ws[f'D{rows[i]}'].value for i in range(0,12,3)]
assert len(months)==12
assert all(sum(monthly[i*3:i*3+3])==quarter[i] for i in range(4))
header('2021年各月化妆品销量走势','2021年第三季度销量最多9673，9月单月销量最大3621','*注：数据来源于公司销售系统，统计日期截至2021.12.31')
base=610;scale=.04
colors=['#5158C3','#E87032','#F5B81D','#8C428E']
for q,(total,c) in enumerate(zip(quarter,colors)):
    x=120+q*212
    rect(x,base-total*scale,163,total*scale,c,alpha=.18)
    text(x+81.5,base-total*scale-20,total,12,ha='center')
    for j in range(3):
        idx=q*3+j;cx=x+28+j*54
        bar(cx,monthly[idx],scale,base,20,c);text(cx,base+30,months[idx],12,ha='center')
baseline(base,105,940)

finish()
