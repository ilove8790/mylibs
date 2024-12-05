# myCommon.py

import numpy as np
from datetime import datetime
from collections import Counter


class GrayScale22:
    """ Grayscale 대응 상대휘도(Gamma=2.2기준)

        Args:
        ----
            bit (int): bit depth (8 or 10, default=8)
    """
    def __init__(self, bit: int=8):
        self.bit = bit
        if bit == 10: #(1023)
            self._g = np.array([0,63,127,191,255,319,383,447,511,575,639,703,767,831,895,959,1023])
        else:  # 8bit(255)
            self._g = np.array([0,15,31,47,63,79,95,111,127,143,159,175,191,207,223,239,255])

        self._lmin = np.array([0,0.02,0.1,0.59,1.58,3.25,5.42,8.34,11.9,15.7,21.5,28,36.9,46.7,59.4,75.6,100])
        self._ltyp = np.array([0.001,0.2,0.97,2.42,4.61,7.59,11.4,16,21.6,28,35.4,43.7,53,63.2,74.5,86.7,100])
        self._lmax = np.array([0.22,0.59,2.08,4.55,7.91,11.89,16.9,23.43,31.59,39.8,48.32,58.53,69.27,79.45,89.5,96.5,100])
        self._func_gray_lmin = np.interp(self._g, self._g, self._lmin)
        self._func_gray_ltyp = np.interp(self._g, self._g, self._ltyp)
        self._func_gray_lmax = np.interp(self._g, self._g, self._lmax)


    def get(self, gray: int):
        ''' Get Relative Luminance Value(%) by Grayscale

            Args:
            ----
                gray (int): graylevel to get value (0~255, 0~1023)
                maxgray (int): max-graylevel (255 or 1023)
            Returns:
                ltyp (float): relative luminance value (%)
        '''
        if 0 <= gray <= (2**self.bit - 1):
            result = np.interp(gray, self._g, self._func_gray_ltyp)
        else:
            result = 0.
        return result


    def get_minmax(self, gray: int):
        ''' Get Relative Luminance Value(%) by Grayscale

            Args:
            ----
                gray (int): graylevel to get value (0~255, 0~1023)
            Returns:
                lmin, lmax (float): relative luminance value (%)
        '''
        if 0 <= gray <= (2**self.bit - 1):
            lmin = np.interp(gray, self._g, self._func_gray_lmin)
            lmax = np.interp(gray, self._g, self._func_gray_lmax)
        else:
            lmin, lmax = 0., 0.
        return lmin, lmax



def get_colorname_from_wavelength(wave: float) -> str:
    """ 파장값으로부터 색상문자를 반환한다.
        (infrared, red, yellow, green, cyan, blue, violet, ultraviolet)
    Args:
        wave (float): 파장
    Returns:
        colorname (str): 칼라이름
    """
    if wave < 380.:
        colorname = 'ultraviolet'
    elif 380. < wave < 450.:
        colorname = 'violet'
    elif 450. < wave < 475.:
        colorname = 'blue'
    elif 475. < wave < 495.:
        colorname = 'cyan'
    elif 495. < wave < 570.:
        colorname = 'green'
    elif 570. < wave < 600.:
        colorname = 'yellow'
    elif 600. < wave < 750.:
        colorname = 'red'
    elif 750. < wave:
        colorname = 'infrared'
    else:
        colorname = ""
    return colorname


def get_colorname_from_filename(filename: str, colornames: list) -> str:
    """
    주어진 색상명 리스트에서 파일명에 포함된 색상명을 추출하여 반환한다.

    Args:
    filename (str): 파일명
    colornames_list (list): 색상명 리스트

    Return:
    colorname (str): 파일명에 포함된 색상명
    """
    if not colornames:
        colornames = ['Red', 'Green', 'Blue', 'White', 'Cyan', 'Magenta', 'Yellow']

    fnlist = filename.replace(' ','_').replace('.','_').replace('-','_').split('_')
    cnames = []
    for key in colornames:
        indices = [i for i, x in enumerate(fnlist) if str(x).lower() == key.lower()]
        if indices:
            cnames.append(key)
    if len(cnames) == 1:
        return cnames[0]
    elif len(cnames) > 1:
        return cnames[-1]
    else:
        return ""



def get_mode_count(data):
    """ 리스트내에서 동일 값이 몇번 반복되는지를 반환한다.

    Args:
        data (array): 배열
    Returns:
        mode_count (array): (배열내 값 종류, 돗수)
    """
    count = Counter(data)
    mode_count = count.most_common()
    return mode_count


def printlog(txt):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_datetime}] {txt}")


def convert_data_to_indexed_array(a: np.ndarray) -> np.ndarray:
    """ convert array having float-values to indexed array

        ex) [-10, 10, 1, 5, -5] >> [0, 4, 2, 3, 1]
    """
    a = np.array(a)
    a_shape = a.shape
    a_flat = a.flatten()
    a_set = sorted(set(a_flat))
    a_dict = {}

    # create index dict
    for i, x in enumerate(a_set):
        a_dict[x] = i
    # a_zero_index = a_dict[0.0]

    a_indexed_flat = np.empty(a.size)

    for i, x in enumerate(a_flat):
        # a_indexed_flat[i] = a_dict[x] - a_zero_index
        a_indexed_flat[i] = a_dict[x]

    result = a_indexed_flat.reshape(a_shape)
    return result


def get_central_trimmed_image(a: np.ndarray, med: float, jnd: float) -> np.ndarray:
    """ 히스토그램상 메디안값 주변을 없애고, 음수부와 양수부를 각각 6등분 규격화한 이미지를 만든다.
        음수, 양수가 0에서 먼 값이면 이미지의 칼라맵 색상이 최소,최대값으로만 표시되는 것을 방지함.
    """
    a2 = np.where(a > 0, a - med, a)
    result = a2 / (jnd/2) * 4
    return result


# def get_central_trimmed_image(a: np.ndarray) -> np.ndarray:
#     """ 히스토그램상 메디안값 주변을 없애고, 음수부와 양수부를 각각 6등분 규격화한 이미지를 만든다.
#         음수, 양수가 0에서 먼 값이면 이미지의 칼라맵 색상이 최소,최대값으로만 표시되는 것을 방지함.
#     """
#     a = np.array(a)
#     negatives = a[a<0]
#     positives = a[a>0]
#     negatives_max = np.nanmax(negatives) if negatives.size > 0 else 0
#     positives_min = np.nanmin(positives) if positives.size > 0 else 0
#     a2 = np.where(a<0, a-negatives_max*0.99, np.where(a>0, a-positives_min*0.99, a))
#     a2_step = np.max([abs(np.nanmin(a2)), abs(np.nanmax(a2))]) / 6
#     result = a2 / a2_step
#     return result


# 이미지를 80x80으로 축소
def downsampled_image(image, new_shape=(20, 20)):
    old_rows, old_cols = image.shape[0], image.shape[1]
    new_rows, new_cols = new_shape
    row_factor = old_rows // new_rows
    col_factor = old_cols // new_cols
    result = np.zeros(new_shape, dtype=image.dtype)
    for i in range(new_rows):
        for j in range(new_cols):
            result[i, j] = np.nanmean(image[i * row_factor:(i + 1) * row_factor, j * col_factor:(j + 1) * col_factor])
    return result



# 리스트에서 중복된 문자열은 첫번째 등장 이후의 요소들에 대해 문자열 끝에 .1, .2, .3 처럼 추가한다.
def rename_duplicates(strings: list) -> list:
    seen = {}
    result = []
    for s in strings:
        if s == '':
            result.append(s)
        else:
            if s not in seen:
                seen[s] = 0
                result.append(s)
            else:
                seen[s] += 1
                new_name = f"{s}.{seen[s]}"
                result.append(new_name)
    return result


def dummy_function():
    pass


def null_function():
    pass


def average_dicts(a: dict, b: dict) -> dict:
    result = {}
    for key in a:
        if key in b:
            result[key] = (a[key] + b[key]) / 2
        else:
            result[key] = a[key]

    for key in b:
        if key not in result:
            result[key] = b[key]

    return result


