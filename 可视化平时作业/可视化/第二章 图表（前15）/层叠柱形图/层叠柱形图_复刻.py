# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['5 层叠柱形图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第5图「层叠柱形图」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '5 层叠柱形图'
# 季度：2021Q1/Q2/Q3/Q4/2022Q1/Q2；销售额：3121/4086/4321/4601/4936/4231；利润额：1020/1421/1502/1623/1781/1432
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
BLUE = '#0070C0'
RED = '#E74E69'
NOTE = '#D9D9D9'

W, H = 866, 613
BASE_Y = 516
PX_PER_VAL = 0.0590

quarters = col('B',3,8)
sales = col('C',3,8)
profit = col('D',3,8)

# bar left x positions (pixels) measured from target
blue_x = [109, 226, 343, 460, 576, 693]
red_x = [130, 247, 364, 481, 597, 714]
BAR_W = 30

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

# bars
for i in range(6):
    bh = sales[i] * PX_PER_VAL
    ax.add_patch(Rectangle((blue_x[i], BASE_Y - bh), BAR_W, bh,
                           facecolor=BLUE, edgecolor='none', zorder=3))
    rh = profit[i] * PX_PER_VAL
    ax.add_patch(Rectangle((red_x[i], BASE_Y - rh), BAR_W, rh,
                           facecolor=RED, edgecolor='none', zorder=3))

# baseline y=517-518 (#454866, continuous)
ax.add_patch(Rectangle((76, 517), 700, 2, facecolor='#454866', edgecolor='none', zorder=2))

# bar-top numbers
for i in range(6):
    bh = sales[i] * PX_PER_VAL
    bcx = blue_x[i] + BAR_W / 2
    ax.text(bcx, BASE_Y - bh - 8, str(sales[i]), color='white',
            fontsize=13, ha='center', va='bottom', zorder=5)
    rh = profit[i] * PX_PER_VAL
    rcx = red_x[i] + BAR_W / 2
    ax.text(rcx, BASE_Y - rh - 8, str(profit[i]), color='white',
            fontsize=13, ha='center', va='bottom', zorder=5)

# x-axis labels (centered on group midpoint)
group_cx = [(blue_x[i] + red_x[i] + BAR_W) / 2 for i in range(6)]
for i in range(6):
    ax.text(group_cx[i], 548, quarters[i], color='white',
            fontsize=14, ha='center', va='center', zorder=5)

# title
ax.text(52, 54, '2021年至今季度销售额(万)和利润额(万)', color='white',
        fontsize=29, fontweight='bold', ha='left', va='top', zorder=5)

# subtitle
ax.text(50, 119, '2022年第二季度销售额首次出现下降，降幅达到15%', color='white',
        fontsize=16, ha='left', va='top', zorder=5)

# legend boxes (border + solid bg-colored interior that covers the bars behind)
# sales legend: x691-777, y315-342, blue border
ax.add_patch(Rectangle((691, 315), 86, 27, facecolor=BG, edgecolor=BLUE, linewidth=1.5, zorder=6))
ax.text(734, 328, '销售额', color='white', fontsize=13, ha='center', va='center', zorder=7)
# profit legend: x690-776, y361-388, red border
ax.add_patch(Rectangle((690, 361), 86, 27, facecolor=BG, edgecolor=RED, linewidth=1.5, zorder=6))
ax.text(733, 374, '利润额', color='white', fontsize=13, ha='center', va='center', zorder=7)

# note
ax.text(40, 588, '*注：数据来源于公司销售系统，统计日期截至2022.06.30', color=NOTE,
        fontsize=11, ha='left', va='bottom', zorder=5)

out = str(HERE / '层叠柱形图_复刻.png')
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
