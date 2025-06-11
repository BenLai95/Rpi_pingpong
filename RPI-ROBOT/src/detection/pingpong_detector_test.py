import cv2
import numpy as np

class PingPongDetector2:
    def __init__(self):
        # 設定橘色乒乓球的HSV顏色範圍（可依實際球顏色調整）
        self.lower_orange = np.array([10, 139, 203])
        self.upper_orange = np.array([25, 255, 255])

    def on_trackbar(self, x):
        # 空的回調函數
        pass

    def create_hsv_trackbar(self):
        cv2.namedWindow("HSV 調整")

        # 建立6個trackbar控制H, S, V的上下界
        cv2.createTrackbar("H Lower", "HSV 調整", 10, 179, self.on_trackbar)
        cv2.createTrackbar("H Upper", "HSV 調整", 25, 179, self.on_trackbar)
        cv2.createTrackbar("S Lower", "HSV 調整", 139, 255, self.on_trackbar)
        cv2.createTrackbar("S Upper", "HSV 調整", 255, 255, self.on_trackbar)
        cv2.createTrackbar("V Lower", "HSV 調整", 203, 255, self.on_trackbar)
        cv2.createTrackbar("V Upper", "HSV 調整", 255, 255, self.on_trackbar)

    def get_trackbar_values(self):
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

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)

        # 消除雜訊
        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        blurred = cv2.GaussianBlur(mask, (9, 9), 2)

        output = image.copy()
        selected_center = None
        selected_radius = None

        # === 方法 1：輪廓外接圓 ===
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50:
                continue
            
            # 計算輪廓的重心（質心）
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # 用外接圓估算半徑，但以重心為中心
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                
                if area > largest_area and radius > 5:
                    largest_area = area
                    selected_center = (cx, cy)  # 使用重心而非外接圓圓心
                    selected_radius = int(radius)
                    selected_color = (255, 0, 0)  # 藍色

        # === 方法 2：如果找不到大輪廓，改用霍夫圓 ===
        if selected_center is None:
            circles = cv2.HoughCircles(
                blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                param1=50, param2=15, minRadius=5, maxRadius=200
            )
            if circles is not None:
                circles = np.uint16(np.around(circles))
                max_r = 0
                for c in circles[0, :]:
                    if c[2] > max_r:
                        selected_center = (c[0], c[1])
                        selected_radius = c[2]
                        selected_color = (0, 255, 0)  # 綠色

        # === 方法 3：如果還是找不到，用整個 mask 的重心 ===
        if selected_center is None:
            # 計算整個 mask 的重心
            M = cv2.moments(mask)
            if M["m00"] > 500:  # 確保有足夠的白色像素
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # 估算半徑（用 mask 面積開根號）
                estimated_radius = int(np.sqrt(M["m00"] / np.pi))
                
                selected_center = (cx, cy)
                selected_radius = max(10, estimated_radius)  # 最小半徑 10
                selected_color = (0, 255, 255)  # 黃色

        # 若找到球，畫出圓形並計算偏移
        if selected_center is not None:
            detected = True
            cv2.circle(output, selected_center, selected_radius, selected_color, 2)
            cv2.circle(output, selected_center, 2, (0, 0, 255), 3)
            delta_x = selected_center[0] - center_x
            
            # 加上重心十字線
            cv2.line(output, (selected_center[0]-10, selected_center[1]), 
                    (selected_center[0]+10, selected_center[1]), (0, 0, 255), 2)
            cv2.line(output, (selected_center[0], selected_center[1]-10), 
                    (selected_center[0], selected_center[1]+10), (0, 0, 255), 2)
        else:
            detected = False
            delta_x = None
            selected_radius = None

        if visualize:
            cv2.line(output, (center_x, 0), (center_x, height), (255, 255, 255), 1)  # 畫中心線
            return delta_x, detected, output, blurred

        return delta_x, selected_radius


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

    def detect_ball_contour(self, image, visualize=False):
        height, width = image.shape[:2]
        center_x = width // 2
        
        # 轉灰階並模糊
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # 使用自適應閾值，對光線變化更穩定
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # 尋找輪廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        output = image.copy()
        selected_center = None
        selected_radius = None
        best_score = 0
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 100:  # 過濾太小的輪廓
                continue
                
            # 計算輪廓的凸包
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            
            # 計算輪廓的外接圓
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            circle_area = np.pi * (radius ** 2)
            
            # 計算輪廓長度
            perimeter = cv2.arcLength(cnt, True)
            
            # === 多重特徵評分 ===
            # 1. 面積比例：實際面積 vs 外接圓面積
            area_ratio = area / circle_area if circle_area > 0 else 0
            
            # 2. 凸性：輪廓面積 vs 凸包面積（越接近1越凸）
            convexity = area / hull_area if hull_area > 0 else 0
            
            # 3. 圓度：基於周長的圓度計算
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            
            # 4. 長寬比：檢查是否接近圓形
            rect = cv2.minAreaRect(cnt)
            w, h = rect[1]
            aspect_ratio = min(w, h) / max(w, h) if max(w, h) > 0 else 0
            
            # === 綜合評分（權重可調整） ===
            score = (area_ratio * 0.3 +      # 30% 面積比例
                    convexity * 0.2 +        # 20% 凸性
                    circularity * 0.3 +      # 30% 圓度
                    aspect_ratio * 0.2)      # 20% 長寬比
            
            # 條件：半徑合理 + 綜合評分夠高
            if 10 < radius < 200 and score > 0.4 and score > best_score:
                best_score = score
                
                # 使用重心作為中心
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    selected_center = (cx, cy)
                    selected_radius = int(radius)
                    
                    if visualize:
                        # 畫出評分資訊
                        cv2.putText(output, f"Score:{score:.2f}", (cx-50, cy-30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # 結果處理
        if selected_center is not None:
            detected = True
            delta_x = selected_center[0] - center_x
            
            if visualize:
                # 畫圓和重心
                cv2.circle(output, selected_center, selected_radius, (0, 255, 0), 2)
                cv2.circle(output, selected_center, 2, (0, 0, 255), 3)
                # 畫十字線
                cv2.line(output, (selected_center[0]-15, selected_center[1]), 
                        (selected_center[0]+15, selected_center[1]), (0, 0, 255), 2)
                cv2.line(output, (selected_center[0], selected_center[1]-15), 
                        (selected_center[0], selected_center[1]+15), (0, 0, 255), 2)
                # 畫中心線
                cv2.line(output, (center_x, 0), (center_x, height), (255, 255, 255), 1)
                
                return delta_x, detected, output, thresh
        else:
            detected = False
            delta_x = None
            if visualize:
                cv2.line(output, (center_x, 0), (center_x, height), (255, 255, 255), 1)
                return delta_x, detected, output, thresh
        
        return delta_x, selected_radius

    def detect_ball_edge(self, image, visualize=False):
        height, width = image.shape[:2]
        center_x = width // 2
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1.5)
        
        # Canny 邊緣檢測，參數可調整
        edges = cv2.Canny(blurred, 30, 100)
        
        # 尋找輪廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        output = image.copy()
        selected_center = None
        selected_radius = None
        
        for cnt in contours:
            if len(cnt) < 5:  # 至少需要5個點才能擬合橢圓
                continue
                
            area = cv2.contourArea(cnt)
            if area < 50:
                continue
            
            try:
                # 擬合橢圓（即使是不完整弧段也能擬合）
                ellipse = cv2.fitEllipse(cnt)
                (cx, cy), (w, h), angle = ellipse
                
                # 檢查橢圓是否接近圓形
                aspect_ratio = min(w, h) / max(w, h) if max(w, h) > 0 else 0
                avg_radius = (w + h) / 4  # 平均半徑
                
                if aspect_ratio > 0.7 and 10 < avg_radius < 200:
                    selected_center = (int(cx), int(cy))
                    selected_radius = int(avg_radius)
                    
                    if visualize:
                        # 畫橢圓
                        cv2.ellipse(output, ellipse, (0, 255, 0), 2)
                        break
                        
            except cv2.error:
                continue
    
        # 結果處理同上...
        if selected_center is not None:
            detected = True
            delta_x = selected_center[0] - center_x
            
            if visualize:
                cv2.circle(output, selected_center, 2, (0, 0, 255), 3)
                cv2.line(output, (center_x, 0), (center_x, height), (255, 255, 255), 1)
                return delta_x, detected, output, edges
        else:
            detected = False
            delta_x = None
            if visualize:
                return delta_x, detected, output, edges
    
        return delta_x, selected_radius