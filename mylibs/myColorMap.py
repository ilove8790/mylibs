# myColorMap.py

import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from PySide6.QtGui import QColor

# 백색 기준 광원
MY_STANDARD_WHITE_SOURCE = "E"

MY_STYLE_QLINEEDIT = "QLineEdit { border: 0px solid #b3b3b3; background-color: #e6e6e6; }" # lightgray=d3=(211)
MY_STYLE_QTABLE_HEADER = "QHeaderView::section {background-color: whitesmoke;}"# lightgray, whitesmoke, gainsboro

MY_COLOR_MAPPING = {
    'Red': QColor(255, 0, 0), 'red': QColor(255, 0, 0),
    'Green': QColor(0, 255, 0), 'green': QColor(0, 255, 0),
    'Blue': QColor(0, 0, 255), 'blue': QColor(0, 0, 255),
    'Cyan': QColor(0, 200, 255), 'cyan': QColor(0, 200, 255),
    'Magenta': QColor(255, 0, 255), 'magenta': QColor(255, 0, 255),
    'Yellow': QColor(255, 200, 0), 'yellow': QColor(255, 200, 0),
    'Black': QColor(0, 0, 0), 'black': QColor(0, 0, 0),
    'White': QColor(255, 255, 255), 'white': QColor(255, 255, 255),
    'LightRed': QColor(240, 128, 128), 'lightred': QColor(240, 128, 128), #'lightcoral'
    'LightGreen': QColor(144, 238, 144), 'lightgreen': QColor(144, 238, 144), #'lightgreen'
    'LightBlue': QColor(173, 216, 240), 'lightblue': QColor(173, 216, 240), #'lightblue'
    'Redish': QColor(255, 200, 200), 'redish': QColor(255, 200, 200), #'lightcoral'
    'Greenish': QColor(200, 255, 200), 'greenish': QColor(200, 255, 200), #'lightgreen'
    'Bluish': QColor(200, 200, 255), 'bluish': QColor(200, 200, 255), #'lightblue'
}
MY_COLOR_QTABLE_BACKGROUND = {
    'Red': QColor(240, 128, 128), 'red': QColor(240, 128, 128), #'lightcoral'
    # 'Red': QColor(255, 200, 200), #'lightcoral'
    'Green': QColor(144, 238, 144), 'green': QColor(144, 238, 144), #'lightgreen'
    # 'Green': QColor(200, 255, 200), #'lightgreen'
    'Blue': QColor(173, 216, 230), 'blue': QColor(173, 216, 230), #'lightblue'
    # 'Blue': QColor(200, 200, 255),
}


class Colormap_Wavelength():
    def __init__(self):
        ''' 가시광선 영역의 파장을 색상으로 표시하는 칼라맵
        '''
        self._gamma = 1.0
        self._wavelengths = np.array([])
        self._wave_start, self._wave_end, self._wave_step = 380., 780., 0.2
        self._colors = []
        self._cmap = []

    def set_gamma(self, value: float):
        ''' 감마값 지정(default=1.0)
        '''
        self._gamma = value


    def set_wavelengths(self, wstart, wend, wstep):
        ''' 파장 범위 지정
        Params: (기본값: 380~780nm)
        '''
        self._wave_start, self._wave_end = wstart, wend
        if wstep is None:
            self._wave_step = wstep = 0.2
        self._wavelengths = np.arange(wstart, wend + wstep, wstep)


    def colormap(self, waves=None, gamma=None) -> ListedColormap:
        wstep = self._wave_step
        if gamma is None:
            gamma = self._gamma
        if waves is not None:
            self._wavelengths = np.arange(waves[0], waves[1] + wstep, wstep)
        else:
            self._wavelengths = np.arange(self._wave_start, self._wave_end + self._wave_step, self._wave_step)
        self._colors = [wavelength_to_rgb(w, gamma) for w in self._wavelengths]
        self._cmap = ListedColormap(np.array(self._colors))
        return self._cmap



def wavelength_to_rgb(w: float, gamma: float=2.4):
    ''' 가시광선 영역의 파장에 해당하는 RGB 색상을 [0~1] 범위의 RGB 값으로 반환

    Parameters:
        w (float): wavelength(nm)
        gamma (float): gamma value (defalut=2.4)
    Returns:
        (R,G,B): 0~1 사이값
    '''
    if 380 <= w < 440:
        a = 0.3 + 0.7 * (w - 380) / (440 - 380)
        R = (-(w - 440) / (440 - 380)*a)**gamma
        G = 0.0
        B = a**gamma
    elif 440 <= w < 490:
        R = 0.0
        G = ((w - 440) / (490 - 440))**gamma
        B = 1.0
    elif 490 <= w < 510:
        R = 0.0
        G = 1.0
        B = (-(w - 510) / (510 - 490))*gamma
    elif 510 <= w < 580:
        R =((w - 510) / (580 - 510))**gamma
        G = 1.0
        B = 0.0
    elif 580 <= w < 645:
        R = 1.0
        G = (-(w - 645) / (645 - 580))**gamma
        B = 0.0
    elif 645 <= w <= 780:
        a = 0.3 + 0.7 * (780-w) / (780 - 645)
        R = (1.0*a)**gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    R = 1 if R > 1 else R
    G = 1 if G > 1 else G
    B = 1 if B > 1 else B
    return (R, G, B)

    # R = int(R * intensity_max)
    # G = int(G * intensity_max)
    # B = int(B * intensity_max)

    # return (R, G, B)


def wavelength_to_rgb_by_Glynn(w, gamma) -> tuple[int, int, int]:
    """ 가시광선 파장을 RGB 값으로 변환

    Parameters:
        w (float): wavelength in visible range (380~780 nm)
        gamma (float): gamma correction

    Returns:
        rgb (tuple): (R, G, B) gray (0~255)

    Reference:
        https://www.baeldung.com/cs/rgb-color-light-frequency
    """
    def gamma_correction(value, factor):
        # gamma correction
        return round(255*(value*factor)**0.8)
    # Simplified Mapping
    # This heuristic works by breaking the entire range of wavelengths into sections,
    # each of which maps colors in a different way:
    if 645 < w <= 780:
        r, g, b = 1.0, 0.0, 0.0
    elif 580 < w <= 645:
        r, g, b = 1.0, -(w - 645)/(645/580), 0.0
    elif 510 < w <= 580:
        r, g, b = (w - 510)/(580 - 510 ), 1.0, 0.0
    elif 490 < w <= 510:
        r, g, b = 0.0, 1.0, -(w - 510)/(510 - 490)
    elif 440 < w <= 490:
        r, g, b = 0.0, (w - 440)/(490 - 440), 1.0
    elif 380 < w <= 440:
        r, g, b = -(w - 440)/(440 - 380), 0.0, 1.0
    else:
        r, g, b = 0.0, 0.0, 0.0

    # generate a fading factor to reduce the intensity
    # of the generated color at the extreme ends of the spectrum
    if 700 < w <= 780:
        factor = 0.3 + 0.7*(780 - w)/(780 - 700)
    elif 420 < w <= 700:
        factor = 1.0
    elif 380 < w <= 420:
        factor = 0.3 + 0.7*(w - 380)/(420 - 380)
    else:
        factor = 0.0

    return gamma_correction(r, factor), gamma_correction(g, factor), gamma_correction(b, factor)



def wavelength_to_rgb_cie(w: float, gamma: float=2.4, gamut: int=0, rgbmax: float=255) -> tuple[int, int, int]:
    """ 가시광선 파장을 RGB gray 값으로 변환
        (wavelength -> XYZ -> rgb -> RGB^gamma)

    Parameters:
        w (float): wavelength (380~780nm)
        gamma (float): gamma correction (default=2.4)
        gamut (str): color-gamut (0:'srgb', 1:'rec2020', 2:'dci-p3', 3:'byMtbWLD', 4:'user1',...)
    Returns:
        rgb (tuple): (R,G,B) gray code (0~255)
    Reference:
        https://www.baeldung.com/cs/rgb-color-light-frequency
    """
    Xt1 = (w - 442.0) * (0.0624 if w < 442.0 else 0.0374)
    Xt2 = (w - 599.8) * (0.0264 if w < 599.8 else 0.0374)
    Xt3 = (w - 501.1) * (0.0490 if w < 501.1 else 0.0382)
    X = 0.362*np.exp(-0.5*Xt1**2) + 1.056*np.exp(-0.5*Xt2**2) - 0.065*np.exp(-0.5*Xt3**2)

    Yt1 = (w - 568.8) * (0.0213 if w < 568.8 else 0.0247)
    Yt2 = (w - 530.9) * (0.0613 if w < 530.9 else 0.0322)
    Y = 0.821*np.exp(-0.5*Yt1**2) + 0.286*np.exp(-0.5*Yt2**2)

    Zt1 = (w - 437.0) * (0.0845 if w < 437.0 else 0.0278)
    Zt2 = (w - 459.0) * (0.0385 if w < 459.0 else 0.0725)
    Z = 1.217*np.exp(-0.5*Zt1**2) + 0.681*np.exp(-0.5*Zt2**2)

    if gamut == 0:
        # convert XYZ to sRGB space
        r = 3.2406255*X - 1.537208*Y - 0.4986286*Z
        g = -0.9689307*X + 1.8757561*Y + 0.0415175*Z
        b = 0.0557101*X - 0.2040211*Y + 1.0569959*Z
    elif gamut == 1:
        # convert XYZ to Rec2020 space
        r = 1.71665*X - 0.35567*Y - 0.25337*Z
        g = -0.66668*X + 1.61648*Y + 0.01577*Z
        b = 0.01764*X - 0.04277*Y + 0.94210*Z
    elif gamut == 2:
        # convert XYZ to DCI-P3-D65 space
        r = 2.49350*X - 0.93138*Y - 0.40271*Z
        g = -0.82949*X + 1.716266*Y + 0.02362*Z
        b = 0.03585*X - 0.07617*Y + 0.95688*Z
    elif gamut == 3:
        # convert XYZ to CIE-max(616nm, 532nm, 461nm) space
        r = 1.99005*X - 0.5796*Y - 0.2864*Z
        g = -0.8709*X + 1.83713*Y + 0.0086*Z
        b = 0.00727*X - 0.0153*Y + 0.92596*Z
    else: # gamut==0
        # convert XYZ to sRGB space
        r = 3.2406255*X - 1.537208*Y - 0.4986286*Z
        g = -0.9689307*X + 1.8757561*Y + 0.0415175*Z
        b = 0.0557101*X - 0.2040211*Y + 1.0569959*Z

    def gamma_correction(value, gamma):
        # gamma correction
        if value <= 0.0:
            factor = 0
        elif value <= 0.0031308:
            factor = value*12.92
        elif value <= 1.0:
            factor = 1.055*value**(1/gamma) - 0.055
        else:
            factor = 1.0
        return round(rgbmax*factor)

    return gamma_correction(r, gamma), gamma_correction(g, gamma), gamma_correction(b, gamma)



class Colormap_Excel:
    """ 엑셀의 색조맵 (색순서: low_mid_high)

    Usage:
        cmap = Colormap_Excel().bwr()  # blue-white-red
    """
    def __init__(self):
        a = 255
        self.colors = {
            'bwr': [(90/a, 138/a, 198/a), (252/a, 252/a, 255/a), (248/a, 105/a, 107/a)],  }
        self.colors['bwr_r'] = list(reversed(self.colors['bwr']))

    def _colormap(self, color: str)  -> LinearSegmentedColormap:
        return LinearSegmentedColormap.from_list('custom_cmap', self.colors[color])

    def bwr(self)  -> LinearSegmentedColormap:
        """ Blue-White-Red """
        return self._colormap('bwr')

    def bwr_r(self)  -> LinearSegmentedColormap:
        """ Red-White-Blue """
        return self._colormap('bwr_r')

    def rwb(self)  -> LinearSegmentedColormap:
        """ Red-White-Blue """
        return self._colormap('bwr_r')

    # 호출시 에러 발생하는 원인 확인후 사용 결정할 예정...당장은 보류함(240512)
    # def __call__(self)  -> LinearSegmentedColormap:
    #     return self._cmap


