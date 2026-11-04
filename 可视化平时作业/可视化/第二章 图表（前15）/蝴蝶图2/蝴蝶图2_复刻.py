# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['7 蝴蝶图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第7图「蝴蝶图」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '7 蝴蝶图'
# 华东36%/42% 西北31%/26% 东北18%/19% 华北13%/12% 华南9%/5%
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
BLUE_DARK = '#005799'
RED = '#E74E69'
RED_DARK = '#A94E69'
NOTE = '#D9D9D9'

W, H = 676, 391

regions = col('B',3,7)
v2022 = [round(v*100) for v in col('C',3,7)]
v2021 = [round(v*100) for v in col('D',3,7)]

# measured bar geometry
row_cy = [158, 190, 222, 254, 286]
BAR_H = 20
BLUE_RIGHT = 289
RED_LEFT = 404
blue_left = [BLUE_RIGHT-v*4.95 for v in v2022]
red_right = [RED_LEFT+v*4.95 for v in v2021]

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

def textured_bar(x0, x1, y0, y1, light, dark):
    # base light fill
    ax.add_patch(Rectangle((x0, y0), x1-x0, y1-y0, facecolor=light, edgecolor='none', zorder=3))
    # dark vertical stripes every 3px, 1px wide
    x = x0 + 1
    while x < x1:
        ax.add_patch(Rectangle((x, y0), 1, y1-y0, facecolor=dark, edgecolor='none', zorder=4))
        x += 3

for i in range(5):
    cy = row_cy[i]
    ytop = cy - BAR_H/2
    # blue bar (leftwards from BLUE_RIGHT)
    textured_bar(blue_left[i], BLUE_RIGHT, ytop, ytop+BAR_H, BLUE, BLUE_DARK)
    # red bar (rightwards from RED_LEFT)
    textured_bar(RED_LEFT, red_right[i], ytop, ytop+BAR_H, RED, RED_DARK)

# percentage labels outside bars
for i in range(5):
    cy = row_cy[i]
    # left pct: right-aligned just left of blue bar
    ax.text(105, cy, str(v2022[i]) + '%', color='white',
            fontsize=13, ha='right', va='center', zorder=5)
    # right pct: left-aligned just right of red bar
    ax.text(618, cy, str(v2021[i]) + '%', color='white',
            fontsize=13, ha='left', va='center', zorder=5)

# region names in center column
for i in range(5):
    ax.text(346, row_cy[i], regions[i], color='white',
            fontsize=14, ha='center', va='center', zorder=5)

# title
ax.text(40, 30, '2022年第一季度销售目标完成情况', color='white',
        fontsize=22, fontweight='bold', ha='left', va='top', zorder=5)

# subtitle
ax.text(40, 76, '华东区域完成率最高达到36%，但是相比去年的42%有所下降', color='white',
        fontsize=14, ha='left', va='top', zorder=5)

# note
ax.text(30, 368, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', color=NOTE,
        fontsize=11, ha='left', va='bottom', zorder=5)

out = str(HERE / '蝴蝶图2_复刻.png')
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
