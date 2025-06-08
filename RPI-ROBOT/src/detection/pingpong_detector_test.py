import cv2
import numpy as np

class PingPongDetector2:
    def __init__(self):
        # 設定橘色乒乓球的HSV顏色範圍（可依實際球顏色調整）
        self.lower_orange = np.array([10, 139, 203])
        self.upper_orange = np.array([25, 255, 255])


    def create_hsv_trackbar():
        cv2.namedWindow("HSV 調整")

        # 建立6個trackbar控制H, S, V的上下界
        cv2.createTrackbar("H Lower", "HSV 調整", 0, 179, )
        cv2.createTrackbar("H Upper", "HSV 調整", 30, 179, )
        cv2.createTrackbar("S Lower", "HSV 調整", 70, 255, )
        cv2.createTrackbar("S Upper", "HSV 調整", 255, 255, )
        cv2.createTrackbar("V Lower", "HSV 調整", 70, 255, )
        cv2.createTrackbar("V Upper", "HSV 調整", 255, 255, )

    def get_trackbar_values():
        h_lower = cv2.getTrackbarPos("H Lower", "HSV 調整")
        h_upper = cv2.getTrackbarPos("H Upper", "HSV 調整")
        s_lower = cv2.getTrackbarPos("S Lower", "HSV 調整")
        s_upper = cv2.getTrackbarPos("S Upper", "HSV 調整")
        v_lower = cv2.getTrackbarPos("V Lower", "HSV 調整")
        v_upper = cv2.getTrackbarPos("V Upper", "HSV 調整")
        lower = np.array([h_lower, s_lower, v_lower])
        upper = np.array([h_upper, s_upper, v_upper])
        return lower, upper

    def detect_ball(self, image, visualize=False):
        # 灰階 + 模糊 + 邊緣檢測
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        edges = cv2.Canny(blurred, 50, 150)

        # 尋找輪廓（只取外輪廓）
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        output = image.copy()
        detected = False

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 100:
                continue

            # 最小外接圓
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            circle_area = np.pi * (radius ** 2)

            # 比較實際輪廓面積與圓面積，篩選圓形（越接近1越像圓）
            circularity = area / circle_area if circle_area != 0 else 0

            if 0.7 < circularity < 1.2 and 5 < radius < 100:
                cv2.circle(output, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(output, (int(x), int(y)), 2, (0, 0, 255), 3)
                detected = True

        if visualize:
            cv2.imshow("邊緣圖", edges)
            cv2.imshow("輪廓結果", output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return detected


    def detect_ball_hsv(self, image, visualize=False):
        height, width = image.shape[:2]
        center_x = width // 2  # 螢幕中心 x 座標

        processed = self.preprocess_image(image)
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)

        # 消除雜訊
        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        blurred = cv2.GaussianBlur(mask, (9, 9), 2)

        output = processed.copy()
        selected_center = None

        # === 優先找藍色：輪廓外接圓 ===
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50:
                continue
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if 5 < radius < 50 and area > largest_area:
                largest_area = area
                selected_center = (int(x), int(y))
                selected_radius = int(radius)
                selected_color = (255, 0, 0)  # 藍色

        # === 若藍色找不到，再用綠色（霍夫圓） ===
        if selected_center is None:
            circles = cv2.HoughCircles(
                blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                param1=50, param2=15, minRadius=5, maxRadius=100
            )
            if circles is not None:
                circles = np.uint16(np.around(circles))
                max_r = 0
                for c in circles[0, :]:
                    if c[2] > max_r:
                        selected_center = (c[0], c[1])
                        selected_radius = c[2]
                        selected_color = (0, 255, 0)  # 綠色

        # 若找到球，畫出圓形並計算偏移
        if selected_center is not None:
            detected = True
            cv2.circle(output, selected_center, selected_radius, selected_color, 2)
            cv2.circle(output, selected_center, 2, (0, 0, 255), 3)
            delta_x = selected_center[0] - center_x
        else:
            detected = False
            delta_x = None

        if visualize:
            cv2.line(output, (center_x, 0), (center_x, height), (255, 255, 255), 1)  # 畫中心線
            #cv2.imshow("追蹤結果", output)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            return delta_x, detected, output

        return delta_x, detected


    def preprocess_image(self, image):
        # 影像前處理，可加上resize、去雜訊等（目前直接回傳原圖）
        return image

    def postprocess_detection(self, detection_result):
        # 偵測結果後處理（目前直接回傳結果本身）
        return detection_result

    def visualize_kernel_param(self, image):
        def nothing(x):
            pass

        cv2.namedWindow("Kernel調整")
        cv2.createTrackbar("Kernel", "Kernel調整", 7, 31, nothing)  # 建議最大設31

        while True:
            k = cv2.getTrackbarPos("Kernel", "Kernel調整")
            if k < 1:
                k = 1
            if k % 2 == 0:
                k += 1  # 確保是奇數

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
            kernel = np.ones((k, k), np.uint8)
            mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel)
            blurred = cv2.GaussianBlur(mask_close, (9, 9), 2)

            circles = cv2.HoughCircles(
                blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                param1=50, param2=15, minRadius=5, maxRadius=100
            )

            output = image.copy()
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)

            cv2.imshow("原圖", image)
            cv2.imshow("遮罩", mask_close)
            cv2.imshow("圓形偵測結果", output)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

        cv2.destroyAllWindows()