import depthai as dai
import cv2
import os
from datetime import datetime

# 初始化pipeline和設備
pipeline = dai.Pipeline()

# 創建彩色相機節點
colorCam = pipeline.createColorCamera()
colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
colorCam.setFps(30)

# 創建輸出
color_out = pipeline.createXLinkOut()
color_out.setStreamName("color")
colorCam.video.link(color_out.input)

# 定義圖片的ROI
whole_image_roi = (0, 0, 1280, 720)  # 調整為整張圖片的大小

# 使用pipeline開始擷取
with dai.Device(pipeline) as device:
    color_queue = device.getOutputQueue("color", maxSize=1, blocking=False)

    while True:
        # 獲取彩色影像
        color_frame = color_queue.get().getCvFrame()

        # 擷取整張圖片
        whole_image = color_frame[whole_image_roi[1]:whole_image_roi[3], whole_image_roi[0]:whole_image_roi[2]]

        # 顯示整張圖片
        cv2.imshow("Whole Image", whole_image)

        key = cv2.waitKey(1) & 0xFF

        # 如果按下 's' 鍵，保存整張圖片
        if key == ord('s'):
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(screenshot_dir, f'whole_image_{timestamp}.png')
            cv2.imwrite(save_path, whole_image)
            print(f"Whole image saved at {save_path}.")

        # 按 'q' 鍵退出
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
