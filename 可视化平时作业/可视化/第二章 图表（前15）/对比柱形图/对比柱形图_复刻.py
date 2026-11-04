# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['9 对比柱形图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第9图「对比柱形图」复刻 数据：口红3568/2569/-999 面膜4135/3241/-894 隔离4436/2965/-1471 防晒4106/3209/-897 精华4936/3541/-1395
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
DBLUE = '#0070C0'
LBLUE = '#82ADD7'
NOTE = '#D9D9D9'
GRAY = '#D9D9D9'

W, H = 867, 672

cats = col('B',3,7)
v2021 = col('C',3,7)
v2022 = col('D',3,7)
diff = col('E',3,7)

BASE = 560
PX = 0.0605
BAR_W = 32
DB_X = [108, 256, 404, 552, 701]   # center of dark blue bar
LB_X = [150, 298, 446, 595, 743]   # center of light blue bar
GROUP_CX = [129, 277, 426, 574, 722]

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

# baseline
ax.plot([55, 800], [BASE, BASE], color=GRAY, linewidth=1, zorder=2)

for i in range(5):
    h1 = v2021[i] * PX
    h2 = v2022[i] * PX
    # dark blue bar
    ax.add_patch(Rectangle((DB_X[i]-BAR_W/2, BASE-h1), BAR_W, h1,
                           facecolor=DBLUE, edgecolor='none', zorder=3))
    # light blue bar
    ax.add_patch(Rectangle((LB_X[i]-BAR_W/2, BASE-h2), BAR_W, h2,
                           facecolor=LBLUE, edgecolor='none', zorder=3))
    # value on top of dark blue (above bar)
    ax.text(DB_X[i], BASE-h1-10, str(v2021[i]), color='white',
            fontsize=14, ha='center', va='bottom', zorder=5)
    # value inside light blue bar near top
    ax.text(LB_X[i], BASE-h2+18, str(v2022[i]), color='white',
            fontsize=14, ha='center', va='center', zorder=5)
    # category label below baseline
    ax.text(GROUP_CX[i], BASE+28, cats[i], color='white',
            fontsize=16, ha='center', va='center', zorder=5)
    # arrow from dark-blue top to light-blue top (downward)
    x_arr = LB_X[i] + BAR_W/2 + 12
    y_from = BASE - h1
    y_to = BASE - h2
    ax.annotate('', xy=(x_arr, y_from+2), xytext=(x_arr, y_to-2),
                arrowprops=dict(facecolor='white', edgecolor='white',
                                width=1, headwidth=6, headlength=6),
                zorder=4)
    # diff label to the right of arrow
    ax.text(x_arr + 8, (y_from + y_to)/2 + 15, str(diff[i]), color='white',
            fontsize=13, ha='left', va='center', zorder=5)

# title
ax.text(50, 55, '2022年商品对比去年销售情况', color='white',
        fontsize=30, fontweight='bold', ha='left', va='top', zorder=5)
# subtitle
ax.text(50, 115, '商品整体比去年销量有所下降，其中隔离下降最多，下降33%',
        color='white', fontsize=18, ha='left', va='top', zorder=5)
# legend
ax.add_patch(Rectangle((55, 180), 12, 12, facecolor=DBLUE, edgecolor='none', zorder=5))
ax.text(72, 186, '2021销量', color='white', fontsize=13, ha='left', va='center', zorder=5)
ax.add_patch(Rectangle((165, 180), 12, 12, facecolor=LBLUE, edgecolor='none', zorder=5))
ax.text(182, 186, '2022销量', color='white', fontsize=13, ha='left', va='center', zorder=5)
# note
ax.text(30, 645, '*注：数据来源于公司销售系统，统计日期截至2022.01.01', color=NOTE,
        fontsize=12, ha='left', va='center', zorder=5)

out = str(HERE / '对比柱形图_复刻.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
