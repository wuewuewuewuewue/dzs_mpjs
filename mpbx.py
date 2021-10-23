import sys
from time import sleep
import pyautogui
import win32gui


# 屏幕识图 成功返回坐标，失败返回False
def find_pos_form_pic(img_path, confidence):
    try:
        location = pyautogui.locateOnScreen(img_path, confidence=confidence)
        return pyautogui.center(location)
    except TypeError:
        return False


def open_mpjs_box(open_quantity, sort_count, timeout_count):
    if backpack_is_open():
        if not backpack_capacity():
            print('背包已满')
            return None
        for i in range(open_quantity):
            print(f'正在进行第{i + 1}次开宝匣')
            timeout_value = 1
            mpjs_pos = None
            while timeout_value <= timeout_count:
                find_mpjs_pos = find_pos_form_pic('./image/mpjs.bmp', confidence_value)
                if find_mpjs_pos:
                    mpjs_pos = find_mpjs_pos
                    timeout_value = 1
                    break
                else:
                    timeout_value += 1
                    if timeout_value == timeout_count:
                        print('无法找到宝匣坐标，结束执行')
                        return None
            box_pos = None
            while timeout_value <= timeout_count:
                pyautogui.rightClick(mpjs_pos)
                find_box_pos = find_pos_form_pic('./image/open_box.bmp', confidence_value)
                if find_box_pos:
                    box_pos = find_box_pos
                    timeout_value = 1
                    break
                else:
                    timeout_value += 1
                    if timeout_value == timeout_count:
                        print('无法找到展开坐标，结束执行')
                        return None
            while timeout_value <= timeout_count:
                if backpack_capacity():
                    pyautogui.leftClick(box_pos)
                    sleep(4)
                    find_box_opened_pos = find_pos_form_pic('./image/box_opened.bmp', confidence_value)
                    if find_box_opened_pos:
                        timeout_value = 1
                        if (i + 1) % sort_count == 0:
                            backpack_sort()
                            print('整理背包')
                        break
                    else:
                        timeout_value += 1
                        if timeout_value == timeout_count:
                            print('无法找到已开启坐标，结束执行')
                            return None
                else:
                    print('背包已满')
                    return None
    else:
        print('未找到背包，结束执行')


def backpack_capacity():
    backpack_box_pos = find_pos_form_pic('./image/backpack_box.bmp', confidence_value)
    if backpack_box_pos:
        return True
    else:
        return False


def backpack_sort():
    sort_btn_pos = find_pos_form_pic('./image/backpack_sort.bmp', confidence_value)
    pyautogui.leftClick(sort_btn_pos)


def backpack_is_open():
    backpack_pos = find_pos_form_pic('./image/backpack_open.bmp', confidence_value)
    if backpack_pos:
        return True
    else:
        return False


def run(open_quantity, sort_count, timeout_count):
    hwnd = win32gui.FindWindow('斗战神', None)
    print('游戏窗口：' + win32gui.GetWindowText(hwnd))
    # 窗口置顶
    win32gui.SetForegroundWindow(hwnd)
    sleep(1)
    print(f'识别容错率为：{confidence_value} (0-1，1为100%，推荐0.9)')
    print(f'开启数量：{open_quantity}，整理间隔：{sort_count},超时次数上限：{timeout_count}')
    open_mpjs_box(open_quantity, sort_count, timeout_count)
    print('结束执行')


if __name__ == '__main__':
    confidence_value = float(sys.argv[4])
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
