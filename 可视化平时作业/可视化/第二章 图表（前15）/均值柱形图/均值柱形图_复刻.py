# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['2 带均值柱形图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

regions = col('B',3,8)
sales = col('C',3,8)
mean_v = sum(sales)/len(sales)

BG = '#1A1E43'
TEXT = '#FFFFFF'
NOTE = '#D9D9D9'
BAR = '#0070C0'
MEAN = '#FFC000'
AXIS = '#86889A'

fig, ax = plt.subplots(figsize=(8.66, 6.19), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_position([0.0572, 0.1696, 0.9076, 0.5961])

fig.text(0.0554, 0.9435, '3月各区域销量分布', fontsize=27, fontweight='bold',
         color=TEXT, ha='left', va='top')
fig.text(0.0554, 0.8433, '东北销量最多占比总销量的22%，华南销量最低',
         fontsize=18, color=TEXT, ha='left', va='top')

x = np.arange(len(regions))
width = 0.313
y_max = 4000

for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=True,
               colors=TEXT, labelsize=13)
ax.set_xticks(x)
ax.set_xticklabels(regions)
ax.set_ylim(0, y_max)
ax.set_yticks([])
ax.set_xlim(-0.5, 5.5)

for i, v in enumerate(sales):
    rect = Rectangle((i - width / 2, 0), width, v,
                     facecolor=BAR, edgecolor='none', zorder=1)
    ax.add_patch(rect)
    if i == 5:
        label_y = v - 107
    else:
        label_y = v + 220
    ax.text(i, label_y, str(v), ha='center', va='center',
            fontsize=14, color=TEXT, fontweight='bold', zorder=4)

ax.plot([-0.0076, 5.2824], [mean_v, mean_v], color=MEAN,
        linewidth=2.5, zorder=3)
ax.text(4.84, 2851, '平均值：2656', ha='center', va='center',
        fontsize=13, color=MEAN, zorder=4)

ax.spines['bottom'].set_visible(True)
ax.spines['bottom'].set_color(AXIS)
ax.spines['bottom'].set_position(('outward', 1))

fig.text(0.0554, 0.0388, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=12, color=NOTE, ha='left', va='bottom')

plt.savefig(str(HERE / '均值柱形图_复刻.png'),
            dpi=150, facecolor=BG)
plt.close()
print('done')
