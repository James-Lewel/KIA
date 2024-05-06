import cv2
import numpy as np
from kia_depth import Midas_Depth
from roboflow import Roboflow
from inference_sdk import InferenceHTTPClient
from kia_meals import days_dictionary

client = InferenceHTTPClient(
    api_url="http://localhost:9001",
    api_key="7gqyul75jvef76MNUFCI"
)

class ObjectDetection:
    def __init__(self):
        self.rf = Roboflow(api_key="7gqyul75jvef76MNUFCI")
        #self.project = self.rf.workspace("stust-k-lab").project("kitchen-intelligent-assistant")
        #self.model = self.project.version(14).model
        self.main_dish_count = 0
        self.side_dish_count = 0
        self.width = 960
        self.height = 540
        self.depth_model = Midas_Depth()

    def get_class_color(self, class_name):
        if "-m-" in class_name:
            self.main_dish_count += 1
            if self.main_dish_count == 1:
                return (0, 0, 255)  # Red
        elif "-s-" in class_name:
            self.side_dish_count += 1
            if self.side_dish_count == 1:
                return (0, 255, 0)  # Green
            elif self.side_dish_count == 2:
                return (255, 165, 0)  # Blue
            elif self.side_dish_count == 3:
                return (0, 255, 255)  # Yellow
        return (255, 255, 255)  # Default to white for unknown classes

    def estimate_proportions(self, frame):
        # Perform edge detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_frame, 100, 200)

        # Obtain depth map
        depth_map = self.depth_model.get_depth_image(frame)
        threshold = np.percentile(depth_map, 50) 

        # Apply a mask using the depth map to focus only on relevant areas
        masked_depth_map = np.where(depth_map < threshold, 1, 0)
        masked_edges = cv2.bitwise_and(edges, edges, mask=(masked_depth_map * 255).astype(np.uint8))

        kernel = np.ones((5, 5), np.uint8)
        dilated_edges = cv2.dilate(masked_edges, kernel, iterations=1)

        filled_areas = dilated_edges
        filled_pixels = cv2.countNonZero(filled_areas)
        total_pixels = frame.shape[0] * frame.shape[1]
        proportion = 100 * (filled_pixels / total_pixels)

        cv2.imshow('filled', filled_areas)
        cv2.imshow('depth map', (depth_map * 255).astype(np.uint8))
        cv2.waitKey()

        return proportion

    
    def process_yolov8(self, frame):
        frame = cv2.resize(frame, (self.width, self.height))
        #results = self.model.predict(frame, confidence=50, overlap=50)
        #predictions = results.json()
        with client.use_model(model_id="kitchen-intelligent-assistant/53"):
            predictions = client.infer(frame)
            
        print('------')
        relevant_classes = days_dictionary[14]['lunch']
        print('------')    
        
        filtered_predictions = [prediction for prediction in predictions['predictions'] 
                             if prediction['confidence'] >= 0.7 and 
                             any(str(class_num) in prediction['class'] for class_num in relevant_classes)]

        for prediction in filtered_predictions:
            print(prediction['class'])
            
        for prediction in filtered_predictions:
            x = prediction['x']
            y = prediction['y']
            width = prediction['width']
            height = prediction['height']
            class_name = prediction['class']
            confidence = prediction['confidence']
            x1 = int(x - (width / 2))
            y1 = int(y - (height / 2))
            x2 = int(x + (width / 2))
            y2 = int(y + (height / 2))
            color = self.get_class_color(class_name)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 1)
            label = f'{class_name[:2].replace("-", "")} - {confidence:.2f}'
            text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, y1 - text_size[1]), (x1 + text_size[0], y1), color, -1)
            cv2.putText(frame, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            depth_map = self.depth_model.get_depth_image(frame)
            cv2.imshow('depth map - full', (depth_map * 255).astype(np.uint8))
            
            # Estimate plate proportions and print below bounding box
            plate_proportion = self.estimate_proportions(frame[y1:y2, x1:x2])
            text = f'Est.: {plate_proportion:.2f}%'
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, y2 - text_size[1]), (x1 + text_size[0], y2), color, -1)
            cv2.putText(frame, text, (x1, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        self.main_dish_count = 0
        self.side_dish_count = 0
        return frame

if __name__ == "__main__":
    yolo_processor = ObjectDetection()
    #video_file = "records\\record_20240312_135626.avi"
    #cap = cv2.VideoCapture(video_file)
    picture = cv2.imread('data\\0 degrees\day_14\lunch\day_14_lunch (1).png')
    while True:
        #ret, frame = cap.read()
        #if not ret:
        #    break
        
        predictions = yolo_processor.process_yolov8(picture)
        cv2.imshow("YOLOv8", predictions)

        if cv2.waitKey(int(1000/32)) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
