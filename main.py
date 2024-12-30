import time
import cv2
import pyautogui
import numpy as np
from PIL import ImageGrab
from playsound import playsound

template_paths = [
    #"picture/1.jpg", #吉伊
    #"picture/8.jpg", #小八
    #"picture/mm.jpg",  #毛毛力
    "picture/Usagi.jpg",  # 乌萨奇
    "picture/Rikimanju.jpg",  # 栗子
    "picture/Shisaa.jpg",  # 狮萨
    "picture/Rakko.jpg",  # 獭师
    "picture/Crab.jpg"   # 古本
]

# 刷新按钮的位置（手动测量屏幕上的坐标值，需调整）
refresh_button_x, refresh_button_y = 195, 80  # 替换为你的刷新按钮位置

def preprocess_image(image):
    """
    对图像进行预处理（灰度化和模糊化）
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转灰度
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)    # 模糊处理
    return blurred

def capture_screen():
    """
    截取整个屏幕并返回为 OpenCV 图像
    """
    # 截取屏幕
    screenshot = ImageGrab.grab()
    # 转换为 OpenCV 格式（BGR）
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot_cv

def find_any_button_location(template_paths, threshold=0.9999):
    """
    使用模板匹配找到任意按钮的位置（宽松匹配）
    :param template_paths: 模板图像路径列表
    :param threshold: 匹配阈值
    :return: 按钮中心坐标 (x, y)，如果找不到返回 None
    """
    # 截取屏幕
    screen = capture_screen()
    # 对屏幕图像预处理
    screen_processed = preprocess_image(screen)

    # 遍历所有图像
    for template_path in template_paths:
        # 加载图像
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        template_processed = preprocess_image(template)

        # 图像匹配
        result = cv2.matchTemplate(screen_processed, template_processed, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 判断是否找到图像
        if max_val >= threshold:
            button_x, button_y = max_loc
            # 计算按钮位置
            button_center_x = button_x + template.shape[1] // 4 * 3
            button_center_y = button_y + template.shape[0] // 2
            print(f"找到匹配图像：{template_path}，相似度：{max_val:.2f}")
            return button_center_x, button_center_y

    return None

def click_button(x, y):
    """
    移动鼠标到指定位置并点击
    :param x: 按钮中心的 X 坐标
    :param y: 按钮中心的 Y 坐标
    """
    pyautogui.moveTo(x, y, duration=0.5)  # 模拟鼠标移动到按钮
    pyautogui.click()  # 点击按钮
    print(f"已点击按钮位置：({x}, {y})")

def click_refresh_button():
    """
    点击刷新按钮
    """
    pyautogui.moveTo(refresh_button_x, refresh_button_y, duration=0.5)  # 移动到刷新按钮
    pyautogui.click()  # 点击刷新按钮
    print("已点击刷新按钮")

def main():
    """
    主函数：每 1 秒检查一次是否有货，无货则点击刷新按钮并循环检查
    """
    print("程序已启动，每 1 秒检查一次按钮状态...")
    while True:
        try:
            # 查找图片位置
            button_location = find_any_button_location(template_paths)

            if button_location:
                print("找到商品，有货！准备点击...")
                click_button(*button_location)
                playsound('music/bingo.mp3')
                break  # 成功点击后退出循环
            else:
                print("未找到商品，无货。点击刷新按钮...")
                click_refresh_button()  # 点击刷新按钮

            # 每 1 秒检查一次
            time.sleep(1)

        except KeyboardInterrupt:
            print("程序已终止。")
            break

if __name__ == "__main__":
    main()
