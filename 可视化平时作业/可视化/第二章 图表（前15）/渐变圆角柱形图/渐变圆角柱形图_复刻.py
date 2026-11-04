# -*- coding: utf-8 -*-
from pathlib import Path
import openpyxl
# 向上查找原始教材目录；只读，不修改 Excel。图形和标签共用同一组单元格值。
HERE = Path(__file__).resolve().parent
SOURCE = next((p for base in HERE.parents for p in base.glob('《*/第二章 图表(前15).xlsx')), None)
if SOURCE is None:
    raise FileNotFoundError('请把本文件夹放在教材 Excel 所在项目目录下。缺少 第二章 图表(前15).xlsx')
wb = openpyxl.load_workbook(SOURCE, data_only=True, read_only=True)
ws = wb['3 渐变圆角柱形图']
def col(letter, start, end):
    values = [ws[f'{letter}{r}'].value for r in range(start, end+1)]
    if any(v is None for v in values):
        raise ValueError(f'缺失数据：{ws.title}!{letter}{start}:{letter}{end}')
    return values

import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import PathPatch, Ellipse, Rectangle
from matplotlib.path import Path

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

items = col('B',3,8)
sales = col('C',3,8)

BG = '#1A1E43'
TEXT = '#FFFFFF'
NOTE = '#D9D9D9'
LABEL = '#C2D8E8'
NODE = '#152E5C'
NODE_HL = '#5B9BD5'
STEM = '#5B9BD5'
YAXIS_LINE = '#CFD0D6'
GRID_LINE = '#404361'


def bar_patch(x, y0, y1, w, PXDX, PXDY,
              trl_pts_px=None, trr_pts_px=None, brl_pts_px=None, brr_pts_px=None):
    """bar with corner arcs, data coords.
    x=left, y0=bottom, y1=top, w=width (data units).
    Arc profiles: (x_off inward px, d downward/upward px).
    """
    if trl_pts_px is None:
        trl_pts_px = [
            (4.5, 0.0), (4.5, 1.0),
            (2.5, 1.0), (2.5, 2.0),
            (1.5, 2.0), (1.5, 3.0),
            (0.0, 3.0), (0.0, 3.6),
        ]
    if trr_pts_px is None:
        trr_pts_px = [
            (4.5, 0.0), (4.5, 1.0),
            (1.0, 1.0), (1.0, 3.0),
            (0.0, 3.0), (0.0, 3.6),
        ]
    if brl_pts_px is None:
        brl_pts_px = [(0.05, 6.0), (0.15, 5.0), (0.5, 4.0), (1.0, 3.0),
                      (1.8, 2.0), (3.0, 1.0), (3.25, 0.0)]
    if brr_pts_px is None:
        brr_pts_px = [(4.0, 0.0), (3.0, 1.0), (1.8, 2.0), (1.0, 3.0),
                      (0.5, 4.0), (0.15, 5.0), (0.05, 6.0)]
    trl = [(px / PXDX, pd / PXDY) for px, pd in trl_pts_px]
    trr = [(px / PXDX, pd / PXDY) for px, pd in trr_pts_px]
    brl = [(px / PXDX, pd / PXDY) for px, pd in brl_pts_px]
    brr = [(px / PXDX, pd / PXDY) for px, pd in brr_pts_px]

    X0, X1 = x, x + w
    Y0, Y1 = y0, y1
    verts = []
    # left arc (top -> bottom)
    for xo, d in trl:
        verts.append((X0 + xo, Y1 - d))
    # vertical left edge down to bottom-arc start height
    verts.append((X0, Y0 + brl[0][1]))
    # bottom-left arc (top -> bottom)
    for xo, du in brl:
        verts.append((X0 + xo, Y0 + du))
    # bottom edge implicit -> bottom-right arc (bottom -> top)
    for xo, du in brr:
        verts.append((X1 - xo, Y0 + du))
    # right edge implicit -> right arc (bottom -> top)
    for xo, d in reversed(trr):
        verts.append((X1 - xo, Y1 - d))
    # implicit top edge closes back to start (X0+4.5px, Y1)

    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1) + [Path.CLOSEPOLY]
    verts = verts + [verts[0]]
    return PathPatch(Path(verts, codes), **{'facecolor': 'none', 'edgecolor': 'none'})


fig, ax = plt.subplots(figsize=(8.67, 6.43), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_position([0.135, 0.1726, 0.789, 0.535])

fig.text(0.0727, 0.9518, '3月商品销量对比', fontsize=30, fontweight='bold',
         color=TEXT, ha='left', va='top')
fig.text(0.0715, 0.8554, '防晒销量最多，3月销量856；面膜最少，3月销量523',
         fontsize=24, color=TEXT, ha='left', va='top')

x = np.arange(len(items))
width = 0.1667
y_max = 1200
PX_PER_DATAY = 344.0 / 1200.0
PX_PER_DATAX = 684.0 / 6.0

for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(left=False, bottom=False, labelleft=True, labelbottom=True,
               colors=TEXT, labelsize=13, axis='both')
ax.tick_params(axis='x', pad=7.2)
ax.tick_params(axis='y', pad=8.6)
ax.set_xticks(x)
ax.set_xticklabels(items)
ax.set_ylim(0, y_max)
ax.set_yticks([0, 200, 400, 600, 800, 1000, 1200])
ax.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'])
ax.set_xlim(-0.5, 5.5)

stops = [(0.0, '#004EA7'), (0.139, '#0060AD'), (0.29, '#0080BB'),
         (0.429, '#00A7CF'), (0.571, '#00CAE3'), (0.71, '#00E2F1'),
         (0.857, '#00ECF8'), (1.0, '#00F3FD')]
cmap = LinearSegmentedColormap.from_list('g', stops)

ry_top_d = 4.0 / PX_PER_DATAY
ry_bot_d = 6.0 / PX_PER_DATAY

# label box small corners (2 px linear)
lb_tr = [(2.0, 0.0), (1.0, 1.0), (0.0, 2.0)]
lb_brl = [(0.0, 2.0), (1.0, 1.0), (2.0, 0.0)]
lb_brr = [(2.0, 0.0), (1.0, 1.0), (0.0, 2.0)]

for i, v in enumerate(sales):
    x0 = i - width / 2 + 0.5 / PX_PER_DATAX   # +0.5px: integer pixel-aligned left edge (507.0)
    y0 = -2.0 / PX_PER_DATAY                   # bar bottom edge (extend 2px past target for imshow clip)
    v_px = 532.0 - v * PX_PER_DATAY          # bar top pixel y
    arc_top = math.floor(v_px) + 1           # arc starts on next pixel row
    y1 = (532.0 - arc_top) / PX_PER_DATAY    # arc top in data units
    patch = bar_patch(x0, y0, y1, width, PX_PER_DATAX, PX_PER_DATAY)
    patch.set_transform(ax.transData)
    patch.set_zorder(3)
    patch.set_clip_on(False)   # allow bar bottom arc below y=0 (ax bottom edge)
    ax.add_patch(patch)
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    im = ax.imshow(grad, extent=[x0, x0 + width, 0, v + ry_top_d], aspect='auto',
                   cmap=cmap, origin='lower', zorder=2)
    im.set_clip_path(patch)

    # Bottom arc: precise per-row Rectangles per bar (target pixel widths),
    # drawn over the imshow arc so y529..532 match target exactly.
    # Format: [(y_px, (bar_xl, bar_xr), (erase_x...)), ...]
    BOT_ARCS = {
        0: [(529, (165, 183), ()), (530, (167, 182), (165, 166)),
            (531, (168, 180), (165, 167, 181, 182)), (532, (169, 179), ())],
        1: [(529, (279, 297), ()), (530, (281, 296), (280, 280)),
            (531, (282, 294), (279, 281, 295, 297)), (532, (283, 293), ())],
        2: [(529, (393, 411), ()), (530, (394, 410), (393, 393)),
            (531, (396, 408), (393, 395, 409, 411)), (532, (397, 407), ())],
        3: [(529, (507, 525), ()), (530, (508, 524), (525, 525)),
            (531, (510, 522), (507, 509, 523, 525)), (532, (511, 521), ())],
        4: [(529, (621, 639), ()), (530, (623, 638), (621, 622, 639, 639)),
            (531, (624, 636), (621, 623, 637, 639)), (532, (625, 635), ())],
        5: [(529, (736, 752), (735, 735, 753, 753)), (530, (737, 751), (735, 736, 752, 753)),
            (531, (738, 750), (735, 737, 751, 753)), (532, (739, 749), ())],
    }
    def px2x(px):
        return -0.5 + (px - 117.0) * 6 / 684.0
    for y_px, (xl, xr), eras in BOT_ARCS[i]:
        dtop = (532 - y_px) / PX_PER_DATAY          # top data edge of this pixel row
        dbot = (532 - (y_px + 1)) / PX_PER_DATAY    # bottom data edge
        c = cmap(dtop / (v + ry_top_d))
        for exl, exr in [(eras[j], eras[j + 1]) for j in range(0, len(eras), 2)]:
            ax.add_patch(Rectangle((px2x(exl), dbot), px2x(exr + 1) - px2x(exl),
                                   dtop - dbot, facecolor=BG, edgecolor='none',
                                   clip_on=False, zorder=2.6))
        ax.add_patch(Rectangle((px2x(xl), dbot), px2x(xr + 1) - px2x(xl),
                               dtop - dbot, facecolor=c, edgecolor='none',
                               clip_on=False, zorder=2.6))

    # stem: solid 1px column from label box area down toward bar top arc
    # per-bar target pixels (stem center x, top px y, bottom px y) measured from target
    STEMS = [(173.5, 334, 344),   # lipstick
             (287.75, 369, 381),  # mask
             (402.0, 336, 348),   # isolation
             (517.0, 277, 290),   # sunscreen
             (633.0, 309, 330),   # essence
             (745.0, 290, 311)]   # cream
    # stem per bar, measured from target:
    #   half-pixel stems (lipstick, mask): antialiased 1px slightly-tilted line
    #   integer stems (others): solid 1px Rectangle (may extend into bar arc)
    if i == 0:      # lipstick: top-cx 173.75 -> bot-cx 174.25, y318..344
        cx_t, cx_b, sy_t, sy_b = 173.75, 174.25, 318, 344
        x_t = (cx_t - 117.0) / PX_PER_DATAX - 0.5
        x_b = (cx_b - 117.0) / PX_PER_DATAX - 0.5
        y_top = (532.0 - sy_t) / PX_PER_DATAY
        y_bot = (532.0 - (sy_b + 1)) / PX_PER_DATAY
        ln, = ax.plot([x_t, x_b], [y_top, y_bot], color=STEM, linewidth=0.72,
                      solid_capstyle='butt', zorder=6)
        ln.set_snap(False)
    elif i == 1:    # mask: top-cx 287.75 -> bot-cx 288.0, y367..381
        cx_t, cx_b, sy_t, sy_b = 287.75, 288.0, 367, 381
        x_t = (cx_t - 117.0) / PX_PER_DATAX - 0.5
        x_b = (cx_b - 117.0) / PX_PER_DATAX - 0.5
        y_top = (532.0 - sy_t) / PX_PER_DATAY
        y_bot = (532.0 - (sy_b + 1)) / PX_PER_DATAY
        ln, = ax.plot([x_t, x_b], [y_top, y_bot], color=STEM, linewidth=0.72,
                      solid_capstyle='butt', zorder=6)
        ln.set_snap(False)
    else:
        STEM_R = {2: (402, 334, 348),   # isolation
                  3: (517, 277, 290),   # sunscreen
                  4: (633, 309, 331),   # essence
                  5: (745, 298, 311)}   # cream
        sx, sy_t, sy_b = STEM_R[i]
        x_l = (sx - 0.5 - 117.0) / PX_PER_DATAX - 0.5
        y0 = (532.0 - sy_b) / PX_PER_DATAY
        y1 = (532.0 - sy_t) / PX_PER_DATAY
        ax.add_patch(Rectangle((x_l, y0), 1.0 / PX_PER_DATAX, y1 - y0,
                               facecolor=STEM, edgecolor='none', zorder=6))

    ex = i + 0.1754
    ey = v + 90
    lbx, lby = ex - 0.2807, ey - 56.5
    lbox = bar_patch(lbx, lby, lby + 115.1, 0.5614, PX_PER_DATAX, PX_PER_DATAY,
                     trl_pts_px=lb_tr, trr_pts_px=lb_tr, brl_pts_px=lb_brl, brr_pts_px=lb_brr)
    lbox.set_transform(ax.transData)
    lbox.set_zorder(5)
    lbox.set_facecolor(NODE)
    ax.add_patch(lbox)
    ax.add_patch(Ellipse((ex - 0.162, ey + 2), 0.114, 45.2, facecolor=NODE_HL,
                         edgecolor='none', zorder=5))
    ax.text(ex, ey, str(v), ha='center', va='center',
            fontsize=8, color=LABEL, zorder=6)

ax.grid(axis='y', color=GRID_LINE, linewidth=0.75, dashes=(5.76, 2.88), zorder=1.5)
# X axis: full-width dim dashed line at y=532 (px 118..800), color #404361,
# dashed pattern 7px on / 4px off, drawn as solid Rectangles for pixel control.
# Bars are drawn on top (higher zorder); bottom-arc rects cover the axis under bars.
def _px2x(px):
    return -0.5 + (px - 117.0) * 6 / 684.0

_dash_x = 118
while _dash_x < 800:
    _xl = _dash_x
    _xr = min(_dash_x + 7, 800)
    ax.add_patch(Rectangle((_px2x(_xl), -1.0 / PX_PER_DATAY),
                           _px2x(_xr) - _px2x(_xl), 1.0 / PX_PER_DATAY,
                           facecolor=GRID_LINE, edgecolor='none',
                           clip_on=False, zorder=1.0))
    _dash_x += 11
ax.tick_params(left=False, bottom=False)

fig.text(0.0634, 0.0420, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         fontsize=12, color=NOTE, ha='left', va='bottom')

plt.savefig(str(HERE / '渐变圆角柱形图_复刻.png'),
            dpi=100, facecolor=BG)
plt.close()
print('done')
