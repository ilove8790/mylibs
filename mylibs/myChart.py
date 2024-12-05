# myChart.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator


class Chart_ScatterWithHistUpRight:
    """Scatter-plot with Hist-upside and Hist-rightside
    """
    def __init__(self, figsize: tuple | None):
        _figsize = figsize if figsize else (4.8, 5.4)
        self.fig = plt.figure(figsize=_figsize, layout="constranined")
        self.grid_width_ratios = [4, 1]
        self.grid_height_ratios = [1, 4]

        self.x = np.array([])
        self.y = np.array([])
        self.title = ""
        self.color_bg = "w"  # background color
        self.color_fg = "k"  # foreground color
        self.color_eg = "k"  # edgecolor
        self.scatter_label = ""
        self.hist_up_label = ""
        self.hist_right_label = ""

        self.calc_stats_x()
        self.calc_stats_y()
        self.set_default()


    def set_default(self):
        self.set_title()
        self.set_color()
        self.set_grid_ratio()


    def calc_stats_x(self):
        if np.size(self.x) > 0:
            self.xmed = np.nanmedian(self.x)
            self.xmin = np.nanmin(self.x)
            self.xmax = np.nanmax(self.x)
            self.xavg = np.nanmean(self.x)
            self.xstd = np.nanstd(self.x)
            self.xrng = self.xmax - self.xmin
            self.x01p = np.nanpercentile(self.x, 1)
            self.x99p = np.nanpercentile(self.x, 99)
            self.x01to99 = self.x99p - self.x01p
            self.xbins = 50 if len(self.x) > 2500 else int(np.sqrt(len(self.x)))


    def calc_stats_y(self):
        if np.size(self.y) > 0:
            self.ymed = np.nanmedian(self.y)
            self.ymin = np.nanmin(self.y)
            self.ymax = np.nanmax(self.y)
            self.yavg = np.nanmean(self.y)
            self.ystd = np.nanstd(self.y)
            self.yrng = self.ymax - self.ymin
            self.y01p = np.nanpercentile(self.y, 1)
            self.y99p = np.nanpercentile(self.y, 99)
            self.y01to99 = self.y99p - self.y01p
            self.ybins = 50 if len(self.y) > 2500 else int(np.sqrt(np.size(self.y)))


    def set_x(self, x):
        self.x = np.array(x).flatten()
        self.calc_stats_x()


    def set_y(self, y):
        self.y = np.array(y).flatten()
        self.calc_stats_y()


    def set_title(self, title=None | str, fontsize=None | int):
        if title:
            self.title = title

        if fontsize:
            self.fig.suptitle(f"{self.title}", fontdict={'fontsize': fontsize})
        else:
            self.fig.suptitle(f"{self.title}")


    def set_color(self, color_bg=None | str, color_fg=None | str, color_eg=None | str):
        if color_bg:
            self.color_bg = color_bg
        if color_fg:
            self.color_fg = color_fg
        if color_eg:
            self.color_eg = color_eg


    def set_grid_ratio(self, width_ratios=None, height_ratios=None):
        if width_ratios:
            self.grid_width_ratios = width_ratios
        if height_ratios:
            self.grid_height_ratios = height_ratios


    def make_chart(self):
        # hist_color = {'red': 'lightcoral', 'green': 'lightgreen', 'blue': 'lightblue'}

        # Define the gridspec
        gs = gridspec.GridSpec(2, 2, figure=self.fig, width_ratios=self.grid_width_ratios, height_ratios=self.grid_height_ratios)

        # 산점도
        ax_scatter = self.fig.add_subplot(gs[1, 0])
        ax_scatter.scatter(self.x, self.y, color=self.color_fg, marker='.', s=10, label=self.scatter_label)
        ax_scatter.set_xlabel('Dominant Wavelength')
        ax_scatter.set_ylabel('Peak Intensity')
        ax_scatter.xaxis.set_major_locator(MultipleLocator(1.0))
        ax_scatter.yaxis.set_major_locator(MultipleLocator(0.5))
        ax_scatter.grid(True, color='gray', alpha=0.5)

        # aymin = float(yavg - ystd*sigma)
        # aymax = float(yavg + ystd*sigma)
        # if self.option_chart_radio_selected == 2:  # median-centering
        #     axmin = float(xavg - xstd*sigma)
        #     axmax = float(xavg + xstd*sigma)
        # elif self.option_chart_radio_selected == 3:
        #     axmin, axmax = self.float_xyuvab[0], self.float_xyuvab[1]
        #     aymin, aymax = self.float_xyuvab[2], self.float_xyuvab[3]
        # else:  # full-range with spec.
        #     ax_scatter.xaxis.set_major_locator(MultipleLocator(1.0))
        #     ax_scatter.yaxis.set_major_locator(MultipleLocator(0.5))
        #     axmin = np.min([np.nanmin(x), self.epispec[_color]['wmin']])
        #     axmax = np.max([np.nanmax(x), self.epispec[_color]['wmax']])

        # ax_scatter.set_xlim(axmin - 0.5, axmax + 0.5)
        # ax_scatter.set_ylim(aymin, aymax)

        # # 산점도 파장축에 Median, LSL, USL, JND_up, JND_down 표시
        # ax_scatter.axvline(x=float(xmed), color=_color, linestyle="--", linewidth=1)
        # ax_scatter.axhline(y=float(ymed), color=_color, linestyle="--", linewidth=1)
        # ax_scatter.axvline(x=self.epispec[_color]['wmin'], color='black', linestyle="--", linewidth=1.5)
        # ax_scatter.axvline(x=self.epispec[_color]['wmax'], color='black', linestyle="--", linewidth=1.5)
        # wld_med = self.epi.wld['med']
        # wld_jnd = VarJND_Function.get(wld_med)
        # ax_scatter.axvline(x=float(wld_med-wld_jnd/2), color='black', linestyle=":", linewidth=1)
        # ax_scatter.axvline(x=float(wld_med+wld_jnd/2), color='black', linestyle=":", linewidth=1)

        # # 파장 히스토그램(상단)
        # ax_histx = self.fig.add_subplot(gs[0, 0], sharex=ax_scatter)
        # ax_histx.hist(x, bins=hist_bins, color=f'{hist_color[_color]}', edgecolor='gray',
        #               label=f"Dom.Wave\nMin: {xmin:.1f}\nMed: {xmed:.1f}\nMax: {xmax:.1f}\nRng: {xrng:.1f}")
        # ax_histx.set_ylabel('Count')
        # ax_histx.legend(handlelength=0, handleheight=0)
        # ax_histx.xaxis.set_tick_params(labelbottom=True)  # x축 눈금 라벨 보이기

        # # 파장 히스토그램(우측)
        # ax_histy = self.fig.add_subplot(gs[1, 1], sharey=ax_scatter)
        # ax_histy.hist(y, bins=hist_bins, color=f'{hist_color[_color]}', edgecolor='gray', orientation='horizontal',
        #               label=f"Peak.Int\nMin: {ymin:.1f}\nMed: {ymed:.1f}\nMax: {ymax:.1f}\nRng: {yrng:.1f}")
        # ax_histy.set_xlabel('Count')
        # ax_histy.legend(handlelength=0, handleheight=0)
        # ax_histy.yaxis.set_tick_params(labelleft=False)  # x축 눈금 라벨 숨기기

        # buffer = io.BytesIO()
        # self.fig.savefig(buffer, format='png')
        # buffer.seek(0)
        # image = QPixmap.fromImage(QImage.fromData(buffer.read()))
        # self.canvas_chart.set_image(image)
        # self.show_message_stats2("* Thick Black Dash-line: Spec. Limit,  Thin Black Dot-line: JND Limit"
        #                          +"\n** Thick RGB Dash-line: Median Value")
        # self.show_time_elapsed()


    def get_chart(self) -> Figure:
        return self.fig