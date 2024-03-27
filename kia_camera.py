import depthai as dai
import cv2
import os
from datetime import datetime
from kia_ai import ObjectDetection

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
whole_image_roi = (0, 0, 1600 , 900)  # 調整為整張圖片的大小
#ai = ObjectDetection()

# 使用pipeline開始擷取
with dai.Device(pipeline) as device:
    color_queue = device.getOutputQueue("color", maxSize=1, blocking=False)
    is_recording = False

    while True:
        # 獲取彩色影像
        color_frame = color_queue.get().getCvFrame()

        # 擷取整張圖片
        whole_image = color_frame[whole_image_roi[1]:whole_image_roi[3], whole_image_roi[0]:whole_image_roi[2]]
        #predictions = ai.process_yolov8(whole_image)
        
        # 顯示整張圖片
        cv2.imshow("Whole Image", whole_image)
        #cv2.imshow("Whole Image", predictions)

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
            
        if key == ord('r'):
            if is_recording:
                is_recording = False
            else:
                is_recording = True
                
            if is_recording:
                record_dir = "records"
                if not os.path.exists(record_dir):
                    os.makedirs(record_dir)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                video_filename = f'record_{timestamp}.avi'
                video_path = os.path.join(record_dir, video_filename)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(video_path, fourcc, 30.0, (whole_image.shape[1], whole_image.shape[0]))
                print(f"Recording started. Saving video at {video_path}.")

        if is_recording:
            out.write(whole_image)
        
        # 按 'q' 鍵退出
        if key == ord('q'):
            break

    if is_recording:
        out.release()

    cv2.destroyAllWindows()
