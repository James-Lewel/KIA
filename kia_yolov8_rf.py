import cv2
from roboflow import Roboflow
from kia_meals import get_meals

# Example usage:
classNames = get_meals()

# Load YOLO model
rf = Roboflow(api_key="7gqyul75jvef76MNUFCI")
project = rf.workspace("kia-qemlp").project("kitchen-intelligent-assistant")
model = project.version(2).model

def process_yolov8(frame):
    frame = cv2.resize(frame, (640, 480))
    
    # YOLO object detection code
    results = model.predict(frame, confidence=20, overlap=30)
    predictions = results.json()
    
    for prediction in predictions['predictions']:
        x = prediction['x']
        y = prediction['y']
        width = prediction['width']
        height = prediction['height']
        class_name = prediction['class']
        confidence = prediction['confidence']
        
        # Calculate box coordinates
        x1 = int(x - (width / 2))
        y1 = int(y - (height / 2))
        x2 = int(x + (width / 2))
        y2 = int(y + (height / 2))
        
        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
        
        # Display class label and confidence
        label = f'{class_name} {confidence:.2f}'
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
    return frame

if __name__ == "__main__":
    # Load image
    image_file = "Kitchen-Intelligent-Assistant-2/test/images/day_3_dinner-135-_png.rf.bcdff052d877bd76fff44adf67c0b3ae.jpg"
    image = cv2.imread(image_file)
    
    while True:
        predictions = process_yolov8(image)
        cv2.imshow("YOLOv8", predictions)

        if cv2.waitKey(int(1000/32)) & 0xFF == ord('q'):
                break
    
    cv2.destroyAllWindows()