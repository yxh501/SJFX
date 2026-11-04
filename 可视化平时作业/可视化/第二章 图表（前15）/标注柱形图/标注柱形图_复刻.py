# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['4 标注柱形图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

# -*- coding: utf-8 -*-
# 第4图「标注柱形图」复刻 数据来源：《第二章 图表(前15).xlsx》工作表 '4 标注柱形图'
# 表内数据：口红9221 / 面膜5102 / 隔离6571 / 防晒5760 / 精华6321 / 面霜8612 / 眼影2645 / 气垫5321
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

BG = '#1A1E43'
GRID = '#454866'
NOTE = '#D9D9D9'

items = col('B',3,10)
sales = col('C',3,10)
colors = ['#7BBDD5', '#49A098', '#E66B4C', '#FFC000',
          '#0097E0', '#0070C0', '#4A5BD1', '#464CAC']
names = ['lip', 'mask', 'iso', 'sun', 'ess', 'cream', 'eye', 'cushion']

PX_PER_DATAY = 0.0345  # 10000 value -> 345 px


def px2x(px):
    return (px - 123.0) / 85.0 - 0.5


def py2y(py):
    return (536.0 - py) / PX_PER_DATAY


fig, ax = plt.subplots(figsize=(8.67, 6.42), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_position([0.1419, 0.1651, 0.7866, 0.5623])

fig.text(0.0646, 0.9330, '2021年商品销量情况', fontsize=27, fontweight='bold',
         color='#FFFFFF', ha='left', va='top')
fig.text(0.0657, 0.8364, '口红销量最好达9221，是眼影最低值2645近3.5倍',
         fontsize=18, color='#FFFFFF', ha='left', va='top')

for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(left=False, bottom=False, colors='#FFFFFF', labelsize=13)
ax.set_xticks(range(8))
ax.set_xticklabels(items)
ax.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
ax.set_yticklabels(['0', '2000', '4000', '6000', '8000', '10000'])
ax.set_xlim(-0.5, 7.52)
ax.set_ylim(0, 10463)
ax.tick_params(axis='x', pad=9.5)
ax.tick_params(axis='y', pad=7.5)

# gridlines: exact dash segments scanned from target (x0, x1, edgeL, edgeR)
SEGS = [
    (123, 131, '#2F3354', '#3F4361'), (135, 143, '#272B4E', '#272B4E'),
    (187, 189, '#1F2347', '#1F2347'), (192, 200, '#3A3E5D', '#353859'),
    (203, 212, '#25284C', '#1D2145'), (215, 223, '#3D405F', '#2F3354'),
    (226, 234, '#2A2E50', '#2A2E50'), (238, 246, '#3F4361', '#2D3052'),
    (249, 257, '#2D3052', '#3F4361'), (261, 269, '#2A2E50', '#2A2E50'),
    (272, 280, '#2F3354', '#3D405F'), (283, 292, '#1D2145', '#25284C'),
    (295, 303, '#353859', '#3A3E5D'), (306, 315, '#1F2347', '#222649'),
    (318, 326, '#373B5B', '#353859'), (329, 338, '#25284C', '#1F2347'),
    (341, 349, '#3A3E5D', '#323656'), (352, 360, '#272B4E', '#272B4E'),
    (364, 372, '#3F4361', '#2F3354'), (375, 383, '#2A2E50', '#424563'),
    (387, 395, '#424563', '#2A2E50'), (398, 406, '#2F3354', '#3F4361'),
    (410, 418, '#272B4E', '#272B4E'), (421, 429, '#323656', '#3A3E5D'),
    (432, 441, '#1F2347', '#25284C'), (444, 452, '#353859', '#373B5B'),
    (455, 464, '#222649', '#1F2347'), (467, 475, '#3A3E5D', '#353859'),
    (478, 487, '#25284C', '#1D2145'), (490, 498, '#3D405F', '#2F3354'),
    (501, 509, '#2A2E50', '#2A2E50'), (513, 521, '#3F4361', '#2D3052'),
    (524, 532, '#2D3052', '#3F4361'), (536, 544, '#2A2E50', '#2A2E50'),
    (547, 555, '#2F3354', '#3D405F'), (558, 567, '#1D2145', '#25284C'),
    (570, 570, '#353859', '#353859'), (613, 613, '#1F2347', '#1F2347'),
    (616, 624, '#3A3E5D', '#323656'), (627, 635, '#272B4E', '#272B4E'),
    (639, 647, '#3F4361', '#2F3354'), (650, 658, '#2A2E50', '#424563'),
    (662, 670, '#424563', '#2A2E50'), (673, 681, '#2F3354', '#3F4361'),
    (685, 693, '#272B4E', '#272B4E'), (696, 704, '#323656', '#3A3E5D'),
    (707, 716, '#1F2347', '#25284C'), (719, 727, '#353859', '#373B5B'),
    (730, 739, '#222649', '#1F2347'), (742, 750, '#3A3E5D', '#353859'),
    (753, 762, '#25284C', '#1D2145'), (765, 773, '#3D405F', '#2F3354'),
    (776, 784, '#2A2E50', '#2A2E50'), (788, 796, '#3F4361', '#2D3052'),
    (799, 804, '#2D3052', '#2F3354'),
]

def add_dash(gy, y_bot):
    """draw grid dash segments at row gy; y_bot = pixel row of segment bottom"""
    for x0, x1, el, er in SEGS:
        if x1 == x0:
            ax.add_patch(Rectangle((px2x(x0), py2y(y_bot)),
                                   px2x(x1 + 1) - px2x(x0),
                                   py2y(gy) - py2y(y_bot),
                                   facecolor=GRID, edgecolor='none', zorder=1,
                                   clip_on=False))
            continue
        # left edge, body, right edge
        ax.add_patch(Rectangle((px2x(x0), py2y(y_bot)),
                               px2x(x0 + 1) - px2x(x0),
                               py2y(gy) - py2y(y_bot),
                               facecolor=el, edgecolor='none', zorder=1,
                               clip_on=False))
        if x1 - x0 > 1:
            ax.add_patch(Rectangle((px2x(x0 + 1), py2y(y_bot)),
                                   px2x(x1) - px2x(x0 + 1),
                                   py2y(gy) - py2y(y_bot),
                                   facecolor=GRID, edgecolor='none', zorder=1,
                                   clip_on=False))
        ax.add_patch(Rectangle((px2x(x1), py2y(y_bot)),
                               px2x(x1 + 1) - px2x(x1),
                               py2y(gy) - py2y(y_bot),
                               facecolor=er, edgecolor='none', zorder=1,
                               clip_on=False))

for gy in [191, 260, 329, 398, 467]:
    add_dash(gy, gy + 1)
# X axis dashed at y536 (same segments)
add_dash(536, 537)

# bars (extend 1px below axis so bottom row 536 renders as bar color)
for i, v in enumerate(sales):
    x0 = px2x(145 + i * 85)
    w = px2x(145 + i * 85 + 42) - x0
    y0 = -1.0 / PX_PER_DATAY
    ax.add_patch(Rectangle((x0, y0), w, v - y0, facecolor=colors[i],
                           edgecolor='none', zorder=5, clip_on=False))

# bubbles: name -> (x0, y0, x1, y1) pixel
BUBBLES = {
    'lip': (146, 181, 192, 207), 'mask': (229, 318, 275, 344),
    'iso': (313, 272, 359, 298), 'sun': (401, 300, 448, 326),
    'ess': (486, 285, 532, 311), 'cream': (571, 204, 617, 230),
    'eye': (656, 405, 702, 431), 'cushion': (744, 313, 790, 339),
}
# tails: name -> [(y, x0, x1), ...]
TAILS = {
    'lip': [(208, 153, 165), (209, 154, 165), (210, 155, 165), (211, 156, 164),
            (212, 157, 164), (213, 157, 164), (214, 158, 164), (215, 159, 164),
            (216, 160, 163), (217, 161, 163), (218, 161, 163)],
    'mask': [(345, 256, 268), (346, 256, 266), (347, 255, 265), (348, 255, 264),
             (349, 255, 263), (350, 255, 262), (351, 255, 260), (352, 255, 259),
             (353, 254, 258), (354, 254, 256), (355, 254, 255), (356, 254, 254)],
    'iso': [(299, 320, 332), (300, 322, 333), (301, 323, 333), (302, 324, 333),
            (303, 325, 333), (304, 326, 333), (305, 327, 334), (306, 328, 334),
            (307, 330, 334), (308, 331, 334), (309, 332, 334)],
    'sun': [(327, 427, 440), (328, 427, 437), (330, 426, 433), (331, 425, 431),
            (332, 425, 428), (333, 425, 426)],
    'ess': [(312, 493, 506), (313, 496, 506), (314, 498, 506), (315, 501, 507),
            (316, 503, 507), (317, 506, 508)],
    'cream': [(231, 578, 591), (232, 580, 592), (233, 582, 591), (234, 584, 592),
              (235, 585, 592), (236, 587, 593), (237, 589, 593), (238, 591, 594),
              (239, 593, 594)],
    'eye': [(432, 663, 675), (433, 665, 676), (434, 667, 677), (435, 669, 678),
            (436, 671, 679), (437, 673, 680), (438, 675, 681), (439, 677, 682),
            (440, 679, 683), (441, 681, 684), (442, 683, 684), (443, 684, 684)],
    'cushion': [(340, 752, 764), (341, 754, 766), (342, 756, 767), (343, 758, 767),
                (344, 760, 767), (345, 760, 767), (346, 762, 767), (347, 764, 768),
                (348, 765, 768), (349, 765, 765)],
}

for i, nm in enumerate(names):
    bx0, by0, bx1, by1 = BUBBLES[nm]
    ax.add_patch(Rectangle((px2x(bx0), py2y(by1)),
                           px2x(bx1 + 1) - px2x(bx0),
                           py2y(by0) - py2y(by1),
                           facecolor=colors[i], edgecolor='none', zorder=4))
    for ty, tx0, tx1 in TAILS[nm]:
        ax.add_patch(Rectangle((px2x(tx0), py2y(ty + 1)),
                               px2x(tx1 + 1) - px2x(tx0),
                               py2y(ty) - py2y(ty + 1),
                               facecolor=colors[i], edgecolor='none', zorder=4))
    cx = px2x((bx0 + bx1 + 1) / 2.0)
    cy = py2y((by0 + by1) / 2.0)
    ax.text(cx, cy, str(sales[i]), ha='center', va='center',
            fontsize=12, color='#FFFFFF', zorder=5)

fig.text(0.0566, 0.0281, '*注：数据来源于公司销售系统，统计日期截至2022.08.31',
         fontsize=11, color=NOTE, ha='left', va='bottom')

plt.savefig(str(HERE / '标注柱形图_复刻.png'),
            dpi=100, facecolor=BG)
plt.close()
print('done')
