# RPI-ROBOT

本專案為樹莓派自走車，具備乒乓球偵測、移動、超音波測距與伺服馬達控制等功能。  
適用於自動尋找並撿拾乒乓球的機器人專題。

## 專案結構

```
RPI-ROBOT
├── src/
│   ├── main.py                # 主程式，整合所有功能
│   ├── camera/
│   │   └── pi_camera.py
│   ├── detection/
│   │   ├── pingpong_detector.py
│   │   └── pingpong_detector_test.py
│   ├── motors/
│   │   ├── dc_motor.py
│   │   └── servo.py
│   ├── sensors/
│   │   └── ultrasonic.py
│   └── utils/
│       └── image_utils.py
├── requirements.txt
└── README.md
```

## 安裝方式

1. **安裝 Python 3 與 pip**
2. **安裝套件**
   ```bash
   pip install -r requirements.txt
   ```

## 功能說明

- **乒乓球偵測**：利用 OpenCV 進行影像處理，辨識乒乓球位置。
- **自走車控制**：透過 DC 馬達控制車輛前進、轉向。
- **超音波測距**：偵測車子與乒乓球的距離，避免碰撞。
- **伺服馬達**：控制機械手臂撿拾乒乓球。

## 執行方式

主程式入口為 `src/main.py`：

```bash
python src/main.py
```

## 硬體需求

- Raspberry Pi (建議 3B 以上)
- 樹莓派相機模組或 USB 攝影機
- DC 馬達與馬達驅動板
- 超音波感測器 (HC-SR04)
- 伺服馬達 (SG90 或 MG996R)
- 乒乓球

## 貢獻

歡迎提出 issue 或 pull request，一起讓專案更完善！