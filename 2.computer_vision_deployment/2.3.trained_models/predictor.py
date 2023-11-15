from ultralytics import YOLO

MODEL_PATH = "../2.2.training/runs/classify/train12/weights/best.pt"

class CatsPredictor:
    def __init__(self, model_path: str = MODEL_PATH):
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
