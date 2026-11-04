# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['8 数值百分比']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第8图「数值百分比」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '8 数值百分比'
# 华东2109/-5.8% 西南1369/-17.9% 西北1872/-15.9% 东北1536/-9.3% 华南1946/-20.8% 华北4321/-13.6%
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
DBLUE = '#09387E'
LBLUE = '#82ADD7'
DRED = '#9B3D4F'
NOTE = '#D9D9D9'

W, H = 867, 613

regions = col('B',3,8)[::-1]
sales = col('C',3,8)[::-1]
pct = [f'{v:.1%}' for v in col('F',3,8)[::-1]]

ROW_CY = [203, 265, 327, 389, 451, 513]
BAR_H = 48
BAR_LEFT = 110
BAR_RIGHT = 619
PX_PER = (BAR_RIGHT - BAR_LEFT) / 4321.0
RED_X0 = 620
RED_X1 = 747

fig = plt.figure(figsize=(W/100, H/100), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.set_facecolor(BG)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

for i in range(6):
    cy = ROW_CY[i]
    ytop = cy - BAR_H/2 + 1
    # dark blue = sales
    dbw = sales[i] * PX_PER
    ax.add_patch(Rectangle((BAR_LEFT, ytop), dbw, BAR_H, facecolor=DBLUE, edgecolor='none', zorder=3))
    # light blue = remainder
    lbw = (BAR_RIGHT - BAR_LEFT) - dbw
    if lbw > 0:
        ax.add_patch(Rectangle((BAR_LEFT+dbw, ytop), lbw, BAR_H, facecolor=LBLUE, edgecolor='none', zorder=3))
    # dark red block
    ax.add_patch(Rectangle((RED_X0, ytop), RED_X1-RED_X0, BAR_H, facecolor=DRED, edgecolor='none', zorder=3))
    # region label left
    ax.text(95, cy, regions[i], color='white', fontsize=16, ha='right', va='center', zorder=5)
    # sales number inside dark blue, right-aligned near end
    ax.text(BAR_LEFT + dbw - 12, cy, str(sales[i]), color='white', fontsize=15, ha='right', va='center', zorder=5)
    # pct in red block centered
    ax.text((RED_X0+RED_X1)/2, cy, pct[i], color='white', fontsize=15, ha='center', va='center', zorder=5)

# title
ax.text(55, 55, '2021年各区域销量及同比情况', color='white',
        fontsize=29, fontweight='bold', ha='left', va='top', zorder=5)
# subtitle
ax.text(55, 114, '各区域商品销量同比去年均有下降，其中华南下降最多，同比下降20.8%',
        color='white', fontsize=17, ha='left', va='top', zorder=5)
# note
ax.text(55, 580, '*注：数据来源于公司销售系统，统计日期截至2022.01.01', color=NOTE,
        fontsize=12, ha='left', va='center', zorder=5)

out = str(HERE / '数值百分比_复刻.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
