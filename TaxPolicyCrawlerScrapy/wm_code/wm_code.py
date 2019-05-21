'''
created on 2018年9月13日

@author: administrator
'''
from ctypes import *
import os
import win32api

WM_CODE_DLL_NAME = 'WmCode.dll'
WM_CODE_DLL_FILE = WM_CODE_DLL_NAME

WM_CODE_DLL = None


def set_wm_library_path(path = None):
    global WM_CODE_DLL_FILE
    if path is None:
        WM_CODE_DLL_FILE = os.path.join(os.getcwd(), WM_CODE_DLL_FILE)
    else:
        WM_CODE_DLL_FILE = os.path.join(path, WM_CODE_DLL_FILE)


def load_wm_library():
    global WM_CODE_DLL
    if WM_CODE_DLL is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), WM_CODE_DLL_NAME)
        if not os.path.isfile(path):
            path = WM_CODE_DLL_FILE
            if path[1:3] != ':\\':
                path = os.path.join(os.getcwd(), WM_CODE_DLL_FILE)
                if not os.path.exists(path):
                    path = WM_CODE_DLL_FILE
        WM_CODE_DLL = WinDLL(path)
        return not (WM_CODE_DLL is None)
    else:
        return True


def free_wm_library():
    global WM_CODE_DLL
    global WM_CODE_DLL_FILE
    if (WM_CODE_DLL is None) and win32api.FreeLibrary(WM_CODE_DLL):
        WM_CODE_DLL = None
        WM_CODE_DLL_FILE = WM_CODE_DLL_NAME


def load_wm_from_file(cds_file, password):
    if WM_CODE_DLL is None:
        return False
    else:
        if not os.path.exists(cds_file):
            return False
        WM_CODE_DLL.LoadWmFromFile.argtypes = [c_char_p, c_char_p]
        return WM_CODE_DLL.LoadWmFromFile(cds_file.encode('ansi'), password.encode('ansi'))


'''**********************************************************************************
函数功能说明：设定识别库选项。设定成功返回真，否则返回假。
函数参数说明：
optionindex ：整数型，选项索引，取值范围1～10
optionvalue ：整数型，选项数值。

参数详解：
    optionindex    optionvalue
1.    返回方式    取值范围：0～1     默认为0,直接返回验证码,为1返回验证码字符和矩形范围形如：s,10,11,12,13|a,1,2,3,4 表示识别到文本 s 左边横坐标10,左边纵坐标11,右边横坐标,右边纵坐标12

2.      识别方式        取值范围：0～4     默认为0,0整体识别,1连通分割识别,2纵分割识别,3横分割识别,4横纵分割识别。可以进行分割的验证码，建议优先使用分割识别，因为分割后不仅能提高识别率，而且还能提高识别速度

3.    识别模式    取值范围：0～1     默认为0,0识图模式,1为识字模式。识图模式指的是背景白色视为透明不进行对比，识字模式指的是白色不视为透明，也加入对比。绝大多数我们都是使用识图模式，但是有少数部分验证码，使用识字模式更佳。

4.    识别加速    取值范围：0～1     默认为0,0为不加速,1为使用加速。一般我们建议开启加速功能，开启后对识别率几乎不影响。而且能提高3-5倍识别速度。

5.    加速返回    取值范围：0～1     默认为0,0为不加速返回,1为使用加速返回。使用加速返回一般用在粗体字识别的时候，可以大大提高识别速度，但是使用后，会稍微影响识别率。识别率有所下降。一般不是粗体字比较耗时的验证码，一般不用开启

6.    最小相似度    取值范围：0～100   默认为90

7.      字符间隙        取值范围：-10～0   默认为0,如果字符重叠,根据实际情况填写,如-3允许重叠3像素,如果不重叠的话,直接写0，注意：重叠和粘连概念不一样，粘连的话，其实字符间隙为0.
*******************************************************************************'''


def set_wm_option(option_index, option_value):
    if load_wm_library():
        WM_CODE_DLL.SetWmOption.argtypes = [c_int, c_int]
        return WM_CODE_DLL.SetWmOption(option_index, option_value)


def get_image_from_buffer(img_buffer, img_buflen):
    if load_wm_library():
        WM_CODE_DLL.GetImageFromBuffer.argtypes = [c_int, c_int]
        return WM_CODE_DLL.GetImageFromBuffer(img_buffer, img_buflen)


def load_wm_from_file_ex(cds_file, password):
    if load_wm_library():
        if not os.path.exists(cds_file):
            return -1
        WM_CODE_DLL.LoadWmFromFileEx.ArgTypes = [c_char_p, c_char_p]
        return WM_CODE_DLL.LoadWmFromFileEx(cds_file.encode('ansi'), password.encode('ansi'))
    return -1


'''**********************************************************************************
函数功能说明：设定识别库选项。设定成功返回真，否则返回假。
函数参数说明：
id :  标识库id
optionindex ：整数型，选项索引，取值范围1～10
optionvalue ：整数型，选项数值。

参数详解：
    optionindex    optionvalue
1.    返回方式    取值范围：0～1     默认为0,直接返回验证码,为1返回验证码字符和矩形范围形如：s,10,11,12,13|a,1,2,3,4 表示识别到文本 s 左边横坐标10,左边纵坐标11,右边横坐标,右边纵坐标12

2.      识别方式        取值范围：0～4     默认为0,0整体识别,1连通分割识别,2纵分割识别,3横分割识别,4横纵分割识别。可以进行分割的验证码，建议优先使用分割识别，因为分割后不仅能提高识别率，而且还能提高识别速度

3.    识别模式    取值范围：0～1     默认为0,0识图模式,1为识字模式。识图模式指的是背景白色视为透明不进行对比，识字模式指的是白色不视为透明，也加入对比。绝大多数我们都是使用识图模式，但是有少数部分验证码，使用识字模式更佳。

4.    识别加速    取值范围：0～1     默认为0,0为不加速,1为使用加速。一般我们建议开启加速功能，开启后对识别率几乎不影响。而且能提高3-5倍识别速度。

5.    加速返回    取值范围：0～1     默认为0,0为不加速返回,1为使用加速返回。使用加速返回一般用在粗体字识别的时候，可以大大提高识别速度，但是使用后，会稍微影响识别率。识别率有所下降。一般不是粗体字比较耗时的验证码，一般不用开启

6.    最小相似度    取值范围：0～100   默认为90

7.      字符间隙        取值范围：-10～0   默认为0,如果字符重叠,根据实际情况填写,如-3允许重叠3像素,如果不重叠的话,直接写0，注意：重叠和粘连概念不一样，粘连的话，其实字符间隙为0.
*******************************************************************************'''


def set_wm_option_ex(id, option_index, option_value):
    if load_wm_library():
        WM_CODE_DLL.SetWmOptionEx.argtypes = [c_int, c_int, c_int]
        return WM_CODE_DLL.SetWmOptionEx(id, option_index, option_value)
    return False


def get_image_from_buffer_ex(id, img_buffer):
    if load_wm_library():
        # fpsbdll.GetImageFromBufferEx.argtypes = [c_int, c_void_p, c_long]
        p_img_buffer = cast(img_buffer, POINTER(c_ubyte))
        img_buf_len = len(img_buffer)
        result = create_string_buffer(1024)
        # sresult = "u".encode("ansi")
        # presult = cast(sresult, pointer(c_byte))
        if WM_CODE_DLL.GetImageFromBufferEx(id, p_img_buffer, img_buf_len, result):
            return result.value.decode("ansi") #.value.strip()
    return ''

def get_image_from_file_ex(id, file_path):
    if load_wm_library():
        WM_CODE_DLL.GetImageFromFileEx.argtypes = [c_int, c_char_p, c_char_p]
        sresult = create_string_buffer(1024)
        if WM_CODE_DLL.GetImageFromFileEx(id, file_path.encode('ansi'), sresult):
            return sresult.value.decode("ansi")
    return ''

def calculator(expression):
    if load_wm_library():
        WM_CODE_DLL.Calculator.argtypes = [c_char_p, c_char_p]
        sresult = create_string_buffer(255)
        if WM_CODE_DLL.Calculator(expression.encode('ansi'), sresult):
            return sresult.value.decode("ansi")
    return ''