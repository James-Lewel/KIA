import cv2
import math
import numpy as np
import supervision as sv
from meals import get_meals
from ultralytics import YOLO

model = YOLO("weights/yolov8n.pt")

# Example usage:
classNames = get_meals()

def process_yolov8(frame):
    # YOLO object detection code
    results = model(frame)
    day_1 = ['chicken', 'a', 'b', 'c']
    day_2 = ['pork', 'd', 'e', 'f']
    selected_class_indices = [classNames.index(cls) for cls in day_1]

    for r in results:
        detections = sv.Detections.from_ultralytics(r)
        detections = detections[np.isin(detections.class_id, selected_class_indices)]
        
        boxes = detections
        for box in boxes:
            x1, y1, x2, y2 = box[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            conf = math.ceil((box[2] * 100)) / 100
            cls = int(box[3])
            class_name = classNames[cls]
            label = f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(frame, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
            cv2.putText(frame, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
            
    return frame

if __name__ == "__main__":
        # Test code
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame
            predictions = process_yolov8(frame)
            cv2.imshow("YOLOv8", predictions)

            if cv2.waitKey(int(1000/32)) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()