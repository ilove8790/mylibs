# myColorVision.py

import numpy as np


class Luminous_Efficiency:
    ''' 파장별 밝기 민감도
    '''
    def __init__(self):
        self._wave = np.arange(390, 830+1, 5)
        self._luminous_2deg = np.array([
            0.000414616,0.00105965,0.00245219,0.00497172,0.00907986,0.0142938,0.0202737,0.0261211,0.0331904,0.0415794,0.0503366,
            0.0574339,0.0647235,0.0723834,0.0851482,0.106014,0.129896,0.153507,0.178805,0.206483,0.237916,0.285068,0.348354,
            0.42776,0.520497,0.620626,0.718089,0.794645,0.85758,0.907135,0.954468,0.981411,0.989023,0.999461,0.996774,0.990255,
            0.973261,0.942457,0.896361,0.85872,0.811587,0.754479,0.691855,0.627007,0.558375,0.489595,0.42299,0.360924,0.298086,
            0.24169,0.194312,0.15474,0.119312,0.0897959,0.0667104,0.048997,0.0355998,0.0255422,0.0180794,0.0126157,0.00866128,
            0.00602768,0.00419594,0.00291086,0.00199556,0.00136702,0.000944727,0.000653705,0.000455597,0.000317974,0.000221745,
            0.000156557,0.000110393,7.82744E-05,5.57886E-05,3.98188E-05,2.86018E-05,2.05126E-05,1.48724E-05,0.0000108,7.86392E-06,
            5.73694E-06,4.2116E-06,3.10656E-06,2.28679E-06,1.69315E-06,1.26256E-06,9.42251E-07,7.05386E-07 ])
        # self._luminous_func_2deg = np.interp(self._wave, self._wave, self._luminous_2deg)
        self._luminous_10deg = np.array([
            0.000407678, 0.00107817, 0.00258977, 0.00547421, 0.010413, 0.0171297, 0.0257613, 0.0352955, 0.0469823, 0.0604743,
            0.0746829, 0.0882054, 0.103903, 0.119539, 0.141459, 0.170137, 0.199986, 0.231243, 0.268227, 0.310944, 0.355402,
            0.414823, 0.478048, 0.549134, 0.62483, 0.701229, 0.77882, 0.837636, 0.882955, 0.923386, 0.966532, 0.988689,
            0.99075, 0.999778, 0.99443, 0.984813, 0.964055, 0.928649, 0.877536, 0.837084, 0.786995, 0.727231, 0.662904,
            0.597037, 0.52823, 0.460131, 0.395076, 0.335179, 0.275181, 0.221956, 0.177688, 0.14102, 0.1084, 0.0813769,
            0.0603398, 0.0442538, 0.0321185, 0.0230257, 0.0162884, 0.0113611, 0.00779746, 0.00542539, 0.00377614, 0.00261937,
            0.0017956, 0.00122998, 0.00084999, 0.000588138, 0.000409893, 0.000286072, 0.000199495, 0.000140847, 0.0000993144,
            0.0000704188, 0.0000501893, 0.0000358222, 0.0000257308, 0.0000184535, 0.0000133795, 0.0000097158, 0.00000707442,
            0.00000516095, 0.00000378873, 0.00000279463, 0.00000205715, 0.00000152311, 0.00000113576, 0.000000847617, 0.000000634538 ])
        # self._luminous_func_10deg = np.interp(self._wave, self._wave, self._luminous_10deg)


    def get(self, wave, fov: str="2deg"):
        ''' Luminous Efficiency Function

            Args:
                wave (float): wavelength(nm)
                fov (str): field of viewing (2deg or 10deg, default=2deg if fov="")
            Returns:
                luminous efficiency at given wavelength and fov
        '''
        wave = np.array(wave)
        _shape = wave.shape
        if fov == "10deg":
            # efficiency = np.interp(wave.flatten(), self._wave, self._luminous_func_10deg)
            efficiency = np.interp(wave.flatten(), self._wave, self._luminous_10deg)
        else:
            # efficiency = np.interp(wave.flatten(), self._wave, self._luminous_func_2deg)
            efficiency = np.interp(wave.flatten(), self._wave, self._luminous_2deg)
        efficiency_reshaped = efficiency.reshape(_shape)
        return efficiency_reshaped
        # return efficiency



class Wavelength_JND_by_pokorny_1970:
    """ Wavelength_Discrimination_Threshold by Pokorny and Smith(1970)
        References:
            [1] Joel Pokorny and Vivianne C. Smith,
                "Wavelength Discrimination in the Presence of Added Chromatic Fields",
                Journal Of The Optical Society Of America, Vol. 60, Number 4, 1970
    """

    def __init__(self):
        self._wave = np.arange(440, 670+1, 10)
        self._jnd = np.array([
            3.75, 3.25, 2.125, 1.375, 1.125, 0.875, 1.0, 1.625, 2.375, 2.875, 3.0, 2.75,
            2.0, 1.5, 1.0, 0.875, 1.375, 1.875, 2.875, 3.875, 5.0, 6.667, 8.0, 9.0, ])
        # self._jnd_func = np.interp(self._wave, self._wave, self._jnd)


    def get(self, wave):
        """ Wavelength Discrimination

            Args:
                wave (float): wavelength(nm)
            Returns:
                luminous efficiency at given wavelength
        """
        wave = np.array(wave)
        _shape = wave.shape
        # jnd = np.interp(wave.flatten(), self._wave, self._jnd_func)
        jnd = np.interp(wave.flatten(), self._wave, self._jnd)
        jnd_reshaped = jnd.reshape(_shape)
        return jnd_reshaped
        # return jnd



class Wavelength_JND_by_zhaoping_2011:
    """ Wavelength_Discrimination_Threshold by Zhaoping(2011)
        References:
        [1] Zhaoping L, Geisler WS, May KA (2011)
            "Human Wavelength Discrimination of Monochromatic Light Explained
             by Optimal Wavelength Decoding of Light of Unknown Intensity",
             PLoS ONE 6(5): e19248.
             doi:10.1371/journal.pone.0019248
    """

    def __init__(self):
        self._wave = np.arange(415, 670+1, 5)
        self._jnd = np.array([
            25, 12, 7.5, 5, 3.7, 3.2, 2.8, 2.5, 2.3, 2, 1.6, 1.3, 1.2, 1.2, 1.25,
            1.32, 1.5, 1.7, 1.85, 1.95, 2.15, 2.45, 2.7, 2.8, 2.75, 2.65, 2.5,
            2.3, 2.1, 1.9, 1.7, 1.6, 1.4, 1.3, 1.2, 1.15, 1.15, 1.18, 1.22,
            1.35, 1.55, 1.8, 2.16, 2.6, 3.1, 4, 5.2, 7.5, 11, 17, 25, 35, ])
        # self._jnd_func = np.interp(self._wave, self._wave, self._jnd)


    def get(self, wave):
        """ Wavelength discrimination threshold(JND) at a given wavelength

            Args:
                wave (float): wavelength(nm)
            Returns:
                JND at given wavelength
        """
        wave = np.array(wave)
        _shape = wave.shape
        # jnd = np.interp(wave.flatten(), self._wave, self._jnd_func)
        jnd = np.interp(wave.flatten(), self._wave, self._jnd)
        jnd_reshaped = jnd.reshape(_shape)
        return jnd_reshaped
        # return jnd



