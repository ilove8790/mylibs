# myTailsMura.py

import numpy as np

from typing import Literal
from .myCommon import get_colorname_from_wavelength
from .myColorVision import (
    Wavelength_JND_by_zhaoping_2011,
    Luminous_Efficiency,
)
from .mySegmentation import (
    Segmentation,
    SegmentationWithDiagonal,
)


class TailsMura:
    """ 파장 치우침 비율 계산
        상하좌우대각연결점, 상하위 최대값 기준
    """

    def __init__(self, array=None|np.ndarray):
        self._jnd_func = Wavelength_JND_by_zhaoping_2011()

        self.percent = 25.  # 히스토그램 상하위 기준 비율
        self.cutline_both_up = 0.  # 최종 상한선(퍼센트 and 파장)
        self.cutline_both_down = 0.  # 최종 하한선(퍼센트 and 파장)
        self.cutline_percent_up = 100.  # 파장 상한선 by Percent
        self.cutline_percent_down = 0.  # 파장 하한선 by Percent
        self.cutline_jnd_up = 0.  # 파장 상한선 by JND
        self.cutline_jnd_down = 0.  # 파장 하한선 by JND

        if isinstance(array, np.ndarray):
            self.set_array(array, (1, 1))
        else:
            self._array: np.ndarray
            self.median: float = 0.
            self.jnd = 1.  # 파장인지임계값
            self.colorname = ""
            self.area = 0.  # 픽셀수
            self.flag_array = False  # 데이터 설정 여부(set_array 실행후 True)
            self.flag_cutline = False  # 상하한선 설정 여부(set_cutline 실행후 True)


    def set_array(self, array: np.ndarray, tile: tuple[int,int]=(2,2)):
        """ 치우침 계산할 데이터 설정

        Args:
            array (list): 이미지 데이터
            tile (tuple): 이미지 타일링(rows x cols), 생략시 2x2
        """
        self._array = np.array(np.tile(array, tile))
        self.median = float(np.nanmedian(self._array))  # 파장중앙값
        self.jnd = self.get_jnd(self.median)  # 파장인지임계값
        self.colorname = get_colorname_from_wavelength(self.median)
        self.area = np.size(self._array)  # 이미지 총 픽셀수
        self.flag_array = True
        self.flag_cutline = False


    def get_jnd(self, wave: float):
        return float(self._jnd_func.get(wave))

    def set_jnd(self, wave: float):
        self.jnd = float(self._jnd_func.get(wave))


    def set_cutlines(self, percent: float=25, jnd: float=-1):
        """ 히스토그램 분포에 대한 상하위 기준 비율, 파장인지 임계값을 설정한다.

        Args:
            percent (float): 퍼센트(default=25)
            jnd (float): 파장인지 임계값 지정(-1: 파장임계값함수 사용)
        """
        if jnd == -1:
            jnd = self.get_jnd(self.median)

        if self.flag_array:
            self.flag_cutline = True
            self.percent = percent

            self.cutline_percent_up = np.nanpercentile(self._array, 100 - percent)
            self.cutline_percent_down = np.nanpercentile(self._array, percent)

            self.cutline_jnd_up = self.median + jnd/2
            self.cutline_jnd_down = self.median - jnd/2

            # 'and' 조건
            self.cutline_both_up = max([float(self.cutline_percent_up), self.cutline_jnd_up])
            self.cutline_both_down = min([float(self.cutline_percent_down), self.cutline_jnd_down])


    def get_mask(self, method: Literal["percent", "jnd", "both"]="both") -> tuple[np.ndarray, np.ndarray]:
        """ 지정한 기준선을 적용한 치우침 이미지용 마스크를 반환한다.

        Args:
            method (str): 기준선 종류["percent", "jnd", "both"]
        Returns:
            mask_up (ndarray): 기준선 적용 배열(0:이하, 1:초과)
            mask_down (ndarray): 기준선 적용 배열(0:이상, 1:미만)
        """
        mask_up, mask_down = np.zeros(self._array.shape), np.zeros(self._array.shape)
        if self.flag_array and self.flag_cutline:
            A = self._array
            if method == 'percent':
                mask_up = np.where(A > self.cutline_percent_up, 1, 0)
                mask_down = np.where(A < self.cutline_percent_down, 1, 0)
            elif method == 'jnd':
                mask_up = np.where(A > self.cutline_jnd_up, 1, 0)
                mask_down = np.where(A < self.cutline_jnd_down, 1, 0)
            else:  # 'both'
                mask_up = np.where(A > self.cutline_both_up, 1, 0)
                mask_down = np.where(A < self.cutline_both_down, 1, 0)
        return mask_up, mask_down


    def get_array_tails_only_by_percent(self) -> np.ndarray:
        mask_up, mask_down = self.get_mask(method="percent")
        array_up = self._array * mask_up
        array_down = self._array * mask_down
        return array_up + array_down


    def get_array_tails_only_by_jnd(self) -> np.ndarray:
        mask_up, mask_down = self.get_mask(method="jnd")
        array_up = self._array * mask_up
        array_down = self._array * mask_down
        return array_up + array_down


    def get_array_tails_only_by_both(self) -> np.ndarray:
        mask_up, mask_down = self.get_mask(method="both")
        array_up = self._array * mask_up
        array_down = self._array * mask_down
        return array_up + array_down


    def get_array_normalized_by_jnd(self, a: np.ndarray) -> np.ndarray:
        """ JND 기준 분포 이미지
        """
        a2 = np.where(a > 0, a - self.median, a)
        result = a2 / (self.jnd/2)
        return result


    # def get_array_by_percent(self) -> tuple[np.ndarray, np.ndarray]:
    #     mask_up, mask_down = self.get_mask(method="percent")
    #     array_up = self._array * mask_up
    #     array_down = self._array * mask_down
    #     return array_up, array_down


    # def get_array_by_color(self) -> tuple[np.ndarray, np.ndarray]:
    #     mask_up, mask_down = self.get_mask(method="color")
    #     array_up = self._array * mask_up
    #     array_down = self._array * mask_down
    #     return array_up, array_down


    # def get_array_by_both(self) -> tuple[np.ndarray, np.ndarray]:
    #     mask_up, mask_down = self.get_mask(method="both")
    #     array_up = self._array * mask_up
    #     array_down = self._array * mask_down
    #     return array_up, array_down


    def get_weighted_average_ratio(self, ratio_up: float, ratio_down: float) -> float:
        """ 파장 인지 민감도를 반영한 가중 평균 계산

        Args:
            ratio_up (float): 상위 치우침 면적비율(0~100%)
            ratio_down (float): 하위 치우침 면적비율(0~100%)
        Returns:
            result (float): 가중 평균(파장 인지 민감도 반영)
        """
        result = 0
        if self.flag_array and self.flag_cutline:
            if (390 < self.cutline_both_up < 830) and (390 < self.cutline_both_down < 830):
                luminous_efficiency = Luminous_Efficiency()
                lumeff_up = float(luminous_efficiency.get(self.cutline_both_up))
                lumeff_down = float(luminous_efficiency.get(self.cutline_both_down))
                lumeff_sum = lumeff_up + lumeff_down
                weight_up, weight_down = lumeff_up/lumeff_sum, lumeff_down/lumeff_sum
            else:
                weight_up, weight_down = 1, 1
            result = weight_up*ratio_up + weight_down*ratio_down
            # print(f"get_weighted_average_ratio: "
            #     + f"weight(up,down)=({weight_up:.2f}, {weight_down:.2f})"
            #     + f"ratio(up,down)=({ratio_up:.2f}%, {ratio_down:.2f}%)")
        return result


    def get_tailsmura_index(self,
            method: Literal["percent", "jnd", "both"]="both",
            final: Literal["sum", "max", "avg"]='sum') -> tuple[float, float, float]:
        """ 상하위 비율 기준으로 치우침 지수(Tails Mura Index) 계산

        Args:
        -----
            method (str): 기준선 종류 ["percent", "jnd", "both"]
            final (str): 최종 산출 방법 ["sum", "max", "avg"], default='sum'

        Return:
        ------
            ratio (float): 치우침 종합(최대,합계,가중평균 중 택일)
            ratio_up (float): 상위 치우침(%)
            ratio_down (float): 하위 치우침(%)
        """
        if final == 'max':
            return self._get_tailsmura_index_max(method=method)
        elif final == 'avg':
            return self._get_tailsmura_index_avg(method=method)
        else: # default = 'sum'
            result = self._get_tailsmura_index_max(method=method)
            return result[1]+result[2], result[1], result[2]


    def _get_tailsmura_index_max(self, method: Literal["percent", "jnd", "both"]="both") -> tuple[float, float, float]:
        """ 상하위 비율 기준으로 치우침 지수(Tails Mura Index) 계산

        Args:
            method (str): 기준선 종류["percent", "jnd", "both"]
        Return:
            ratio (float): 상하위 치우침 최대값
            ratio_up (float): 상위 치우침(%)
            ratio_down (float): 하위 치우침(%)
        """
        mask_up, mask_down = self.get_mask(method=method)
        ratio_up, ratio_down = 0, 0
        if np.sum(mask_up) > 1:
            segment_up = SegmentationWithDiagonal(mask_up)
            area_up = segment_up.areas()
            ratio_up = np.max(area_up)/np.size(mask_up)*100
        if np.sum(mask_down) > 1:
            segment_down = SegmentationWithDiagonal(mask_down)
            area_down = segment_down.areas()
            ratio_down = np.max(area_down)/np.size(mask_down)*100

        # 가중평균(%)은 240510a 부터 사용안함
        # ratio = self.get_weighted_average_ratio(ratio_up, ratio_down)
        ratio = max(ratio_up, ratio_down)
        return ratio, ratio_up, ratio_down


    def _get_tailsmura_index_avg(self, method: Literal["percent", "jnd", "both"]="both") -> tuple[float, float, float]:
        """ 상하위 비율 기준으로 치우침 지수(Tails Mura Index) 계산

        Args:
            method (str): 기준선 종류["percent", "jnd", "both"]
        Return:
            ratio (float): 상하위 치우침 가중평균값
            ratio_up (float): 상위 치우침(%)
            ratio_down (float): 하위 치우침(%)
        """
        mask_up, mask_down = self.get_mask(method=method)
        ratio_up, ratio_down = 0, 0
        if np.sum(mask_up) > 1:
            segment_up = SegmentationWithDiagonal(mask_up)
            area_up = segment_up.areas()
            ratio_up = np.max(area_up)/np.size(mask_up)*100
        if np.sum(mask_down) > 1:
            segment_down = SegmentationWithDiagonal(mask_down)
            area_down = segment_down.areas()
            ratio_down = np.max(area_down)/np.size(mask_down)*100

        # 가중평균(%)은 240510a 부터 사용안함
        ratio = self.get_weighted_average_ratio(ratio_up, ratio_down)
        # ratio = max(ratio_up, ratio_down)
        return ratio, ratio_up, ratio_down



class TailsMura_Fixed_JND:
    """ 치우침 비율 계산
    """

    def __init__(self):
        self.color_jnds = {'red': 1.0, 'green': 1.5, 'blue': 3.0,
                           'cyan': 1.0, 'magenta': 3.0, 'yellow': 1.0, }
        self._array: np.ndarray
        self._color = 'green'
        self._percent = 25.  # 히스토그램 상하위 기준 비율
        self.color_jnd = 1.  # 파장인지임계값
        self.median = 0.  # 중앙값
        self.area = 0.  # 픽셀수
        self.cutline_both_up = 0.  # 최종 상한선(퍼센트,파장 동시 고려된)
        self.cutline_both_down = 0.  # 최종 하한선(퍼센트,파장 동시 고려된)
        self.cutline_percent_up = 0.  # 퍼센트 상한선
        self.cutline_percent_down = 0.  # 퍼센트 하한선
        self.cutline_color_up = 0.  # 파장 상한선
        self.cutline_color_down = 0.  # 파장 하한선
        self.cutline_logic = 'and'
        self.flag_array = False  # 데이터 설정 여부(set_array 실행후 True)
        self.flag_cutline = False  # 상하한선 설정 여부(set_cutline 실행후 True)


    def set_array(self, array: np.ndarray, tile: tuple[int,int]):
        """ 치우침 계산할 데이터 설정

        Args:
            array (list): 이미지 데이터
            tile (tuple): 행열 반복횟수(rows x cols), 생략시 원본과 동일
        """
        self._array = np.array(np.tile(array, tile))
        self.median = np.nanmedian(self._array)
        self.area = np.size(self._array)
        self.flag_array = True
        self.flag_cutline = False


    @property
    def array(self) -> np.ndarray:
        return self._array


    def get_percent(self) -> float:
        return self._percent
    def set_percent(self, percent: float=25):
        self._percent = percent
    percent = property(get_percent, set_percent)


    def get_color(self) -> str:
        return self._color
    def set_color(self, color: str="green"):
        self._color = color.lower()
        if self._color in self.color_jnds.keys():
            self._color = self._color
            self.color_jnd = self.color_jnds[self._color]
        else:
            self.color_jnd = 1
    color = property(get_color, set_color)


    def set_cutlines(self, percent: float=25, color: str='green', logic: str='and'):
        """ 히스토그램 분포에 대한 상하위 기준 비율, 파장인지 임계값을 설정한다.

        Args:
            percent (float): 퍼센트(default=25)
            color (str): 색상 문자(대표 파장 인지 임계값 사용, default='green')
            logic (str): 상하한선 동시 적용 방법([and, or], default='and')
        """
        if self.flag_array:
            self.flag_cutline = True
            self.set_percent(percent)
            self.cutline_percent_up = np.nanpercentile(self._array, 100 - self.percent)
            self.cutline_percent_down = np.nanpercentile(self._array, self.percent)

            self.set_color(color)
            self.median = np.nanmedian(self._array)
            self.cutline_color_up = self.median + self.color_jnd/2
            self.cutline_color_down = self.median - self.color_jnd/2

            if logic == 'or':
                self.cutline_logic = 'or'
                self.cutline_both_up = min([self.cutline_percent_up, float(self.cutline_color_up)])
                self.cutline_both_down = max([self.cutline_percent_down, float(self.cutline_color_down)])
            else:
                self.cutline_both_up = max([self.cutline_percent_up, float(self.cutline_color_up)])
                self.cutline_both_down = min([self.cutline_percent_down, float(self.cutline_color_down)])

        # print(f"set_cutlines(logic={self.cutline_logic}): "
        #       + f"percent({self.percent:.1f}%,up,down)=({self.cutline_percent_up:.2f}, {self.cutline_percent_down:.2f}),  "
        #       + f"color({self.color},up,down)=({self.cutline_color_up:.2f}, {self.cutline_color_down:.2f}),  "
        #       + f"both(up,down)=({self.cutline_both_up:.2f}, {self.cutline_both_down:.2f})")


    def get_mask(self, method: str) -> tuple[np.ndarray, np.ndarray]:
        """ 지정한 기준선을 적용한 치우침 이미지용 마스크를 반환한다.

        Args:
            method (str): 기준선 종류["percent", "color", "both"]
        Returns:
            mask_up (ndarray): 기준선 적용 배열(0:이하, 1:초과)
            mask_down (ndarray): 기준선 적용 배열(0:이상, 1:미만)
        """
        mask_up, mask_down = np.zeros(self.array.shape), np.zeros(self.array.shape)
        if self.flag_array and self.flag_cutline:
            A = self.array
            if method == 'percent':
                mask_up = np.where(A > self.cutline_percent_up, 1, 0)
                mask_down = np.where(A < self.cutline_percent_down, 1, 0)
            elif method == 'jnd':
                mask_up = np.where(A > self.cutline_color_up, 1, 0)
                mask_down = np.where(A < self.cutline_color_down, 1, 0)
            else:  # 'both'
                mask_up = np.where(A > self.cutline_both_up, 1, 0)
                mask_down = np.where(A < self.cutline_both_down, 1, 0)

            # print(f"get_mask(method={method}, logic={self.cutline_logic}): "
            #     + f"sum(up,down)=({np.sum(mask_up)}, {np.sum(mask_down)})")
        return mask_up, mask_down


    def get_array_by_percent(self) -> tuple[np.ndarray, np.ndarray]:
        mask_up, mask_down = self.get_mask(method="percent")
        array_up = self.array * mask_up
        array_down = self.array * mask_down
        return array_up, array_down


    def get_array_by_color(self) -> tuple[np.ndarray, np.ndarray]:
        mask_up, mask_down = self.get_mask(method="color")
        array_up = self.array * mask_up
        array_down = self.array * mask_down
        return array_up, array_down


    def get_array_by_both(self) -> tuple[np.ndarray, np.ndarray]:
        mask_up, mask_down = self.get_mask(method="both")
        array_up = self.array * mask_up
        array_down = self.array * mask_down
        return array_up, array_down


    def get_weighted_average_ratio(self, ratio_up: float, ratio_down: float) -> float:
        """ 파장 인지 민감도를 반영한 가중 평균 계산

        Args:
            ratio_up (float): 상위 치우침 면적비율(0~100%)
            ratio_down (float): 하위 치우침 면적비율(0~100%)
        Returns:
            result (float): 가중 평균(파장 인지 민감도 반영)
        """
        result = 0
        if self.flag_array and self.flag_cutline:
            if (390 < self.cutline_both_up < 830) and (390 < self.cutline_both_down < 830):
                luminous_efficiency = Luminous_Efficiency()
                lumeff_up = float(luminous_efficiency.get(self.cutline_both_up))
                lumeff_down = float(luminous_efficiency.get(self.cutline_both_down))
                lumeff_sum = lumeff_up + lumeff_down
                weight_up, weight_down = lumeff_up/lumeff_sum, lumeff_down/lumeff_sum
            else:
                weight_up, weight_down = 1, 1
            result = weight_up*ratio_up + weight_down*ratio_down
            # print(f"get_weighted_average_ratio: "
            #     + f"weight(up,down)=({weight_up:.2f}, {weight_down:.2f})"
            #     + f"ratio(up,down)=({ratio_up:.2f}%, {ratio_down:.2f}%)")
        return result


    def get_tailsmura_index(self, method: str) -> tuple[float, float, float]:
        """ 상하위 비율 기준으로 치우침 지수(Tails Mura Index) 계산
            연결점은 상하좌우대각 기준

        Args:
            method (str): 기준선 종류["percent", "color", "both"]
        Return:
            ratio_avg (float): 상하위 치우침 가중평균(%)
            ratio_up (float): 상위 치우침(%)
            ratio_down (float): 하위 치우침(%)
        """
        mask_up, mask_down = self.get_mask(method=method)
        ratio_up, ratio_down = 0, 0
        if np.sum(mask_up) > 1:
            segment_up = SegmentationWithDiagonal(mask_up)
            area_up = segment_up.areas()
            ratio_up = np.max(area_up)/np.size(mask_up)*100
        if np.sum(mask_down) > 1:
            segment_down = SegmentationWithDiagonal(mask_down)
            area_down = segment_down.areas()
            ratio_down = np.max(area_down)/np.size(mask_down)*100

        ratio_avg = self.get_weighted_average_ratio(ratio_up, ratio_down)
        return ratio_avg, ratio_up, ratio_down


    def get_tailsmura_index_lrud(self, method: str) -> tuple[float, float, float]:
        """ 상하위 비율 기준으로 치우침 지수(Tails Mura Index) 계산
            주의) 연결점은 상하좌우만 포함(대각은 제외함)

        Args:
            method (str): 기준선 종류["percent", "color", "both"]
        Return:
            ratio_avg (float): 상하위 치우침 가중평균(%)
            ratio_up (float): 상위 치우침(%)
            ratio_down (float): 하위 치우침(%)
        """
        mask_up, mask_down = self.get_mask(method=method)
        ratio_up, ratio_down = 0, 0
        if np.sum(mask_up) > 1:
            segment_up = Segmentation(mask_up)
            area_up = segment_up.areas()
            ratio_up = np.max(area_up)/np.size(mask_up)*100
        if np.sum(mask_down) > 1:
            segment_down = Segmentation(mask_down)
            area_down = segment_down.areas()
            ratio_down = np.max(area_down)/np.size(mask_down)*100

        ratio_avg = self.get_weighted_average_ratio(ratio_up, ratio_down)
        return ratio_avg, ratio_up, ratio_down


