# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['11 平滑折线图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第11图「平滑折线图」复刻
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.interpolate import make_interp_spline
import os

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
ORANGE = '#E36A4C'
RED = '#E74C3C'
NOTE = '#D9D9D9'
TEAL = '#5BC0DE'
YELLOW = '#F5B041'

W, H = 866, 642

months = col('C',3,13)
sales = col('D',3,13)

X0 = 120
X1 = 790
BASE_Y = 495
PX_PER = (495-196)/3782.0  # y=196 at 3782

xs = np.linspace(X0, X1, len(months))
ys = [BASE_Y - v*PX_PER for v in sales]

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

# y axis labels (red)
for v in [0, 1000, 2000, 3000, 4000]:
    y = BASE_Y - v*PX_PER
    ax.text(70, y, format(v, ','), color=RED, fontsize=13, ha='right', va='center', zorder=5)

# x axis line
ax.plot([100, 830], [BASE_Y, BASE_Y], color='#888', linewidth=1, zorder=2)

# month labels
for i, m in enumerate(months):
    ax.text(xs[i], BASE_Y+20, m, color='white', fontsize=14, ha='center', va='center', zorder=5)

# 单调分段插值，避免旧二次样条在12月前产生虚假的下跌。
from scipy.interpolate import PchipInterpolator
xnew = np.linspace(xs[0], xs[-1], 600)
ax.plot(xnew, PchipInterpolator(xs, ys)(xnew), color=ORANGE, linewidth=1.5, zorder=4)

# peak annotation (1月)
peak_x = xs[8]
peak_y = ys[8]
ax.plot([peak_x, peak_x], [peak_y, BASE_Y], color=RED, linewidth=1, linestyle='--', zorder=3)
ax.text(peak_x, peak_y-15, '3782', color='white', fontsize=14, ha='center', va='bottom', zorder=5)

# title
ax.text(50, 30, '化妆品品类月度销量走势', color='white',
        fontsize=32, fontweight='bold', ha='left', va='top', zorder=5)
# subtitle
ax.text(50, 90, '2022年销量迅速增加，1月最高，销量达到3782',
        color='white', fontsize=19, ha='left', va='top', zorder=5)

# bottom blocks
ax.add_patch(Rectangle((80, 555), 560, 40, facecolor=TEAL, edgecolor='none', zorder=3))
ax.text(360, 575, '2021', color='white', fontsize=15, ha='center', va='center', zorder=5)
ax.add_patch(Rectangle((650, 555), 180, 40, facecolor=YELLOW, edgecolor='none', zorder=3))
ax.text(740, 575, '2022', color='white', fontsize=15, ha='center', va='center', zorder=5)

# note
ax.text(30, 620, '*注：数据来源于公司销售系统，统计日期截至2022.03.31', color=NOTE,
        fontsize=12, ha='left', va='center', zorder=5)

out = str(HERE / '平滑折线图_复刻.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
plt.savefig(out, dpi=100, facecolor=BG, bbox_inches=None, pad_inches=0)
print('saved', out)
