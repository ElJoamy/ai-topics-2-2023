import numpy as np
from ultralytics import YOLO
import cv2

MODEL_PATH = "/Users/pepe/dev/upb/topics/ai-topics-2-2023/2.computer_vision_deployment/2.2.training/runs/classify/train12/weights/best.pt"

class CatsPredictor:
    def __init__(self, model_path: str = MODEL_PATH):
        print("Creando predictor...")
        self.model = YOLO(model_path)
    
    def predict_file(self, file_path: str):
        results = self.model([file_path])
        pred_data = []
        for i, res in enumerate(results):
            pred_data.append(
                {
                    "category": res.names[res.probs.top1],
                    "confidence":res.probs.data[res.probs.top1].item()
                }
            )
        return pred_data
    
    def predict_image(self, image_array: np.ndarray):
        results = self.model(image_array)[0]

        return {
            "class": results.names[results.probs.top1],
            "confidence": results.probs.data[results.probs.top1].item()
        }
    
if __name__ == "__main__":
    image_file = "/Users/pepe/dev/upb/topics/ai-topics-2-2023/2.computer_vision_deployment/2.2.training/puma2.jpg"
    img = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
    predictor = CatsPredictor()
    prediction = predictor.predict_image(img)
    print(prediction)

