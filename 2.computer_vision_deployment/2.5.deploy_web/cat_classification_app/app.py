import io
import csv
import cv2
from fastapi import (
    FastAPI, 
    UploadFile, 
    File, 
    HTTPException, 
    status,
    Depends
)
from fastapi.responses import Response
import numpy as np
from PIL import Image, UnidentifiedImageError
from predictor import CatsPredictor

app = FastAPI(title="Cats classification API")

predictor = CatsPredictor()

def get_predictor():
    return predictor


def predict_uploadfile(predictor, file):
    img_stream = io.BytesIO(file.file.read())
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 
            detail="Not an image"
        )
    # convertir a una imagen de Pillow
    img_obj = Image.open(img_stream)
    # crear array de numpy
    img_array = np.array(img_obj)
    return predictor.predict_image(img_array), img_array

@app.post("/predict_cat")
def predict_cat(
    file: UploadFile = File(...), 
    predictor: CatsPredictor = Depends(get_predictor)
):
    results, _ = predict_uploadfile(predictor, file)
    
    return results

@app.post("/annotate", responses={
    200: {"content": {"image/jpeg": {}}}
})
def predict_and_annotate(
    file: UploadFile = File(...), 
    predictor: CatsPredictor = Depends(get_predictor)
) -> Response:
    results, img = predict_uploadfile(predictor, file)
    # anotacion
    new_img = cv2.putText(
        img,
        results["class"],
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 0, 0),
        2,
        )
    # new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(new_img)
    image_stream = io.BytesIO()
    img_pil.save(image_stream, format="JPEG")
    image_stream.seek(0)
    # return {"success": True}
    return Response(content=image_stream.read(), media_type="image/jpeg")


@app.get("/reports", responses={
    200: {"content": {"text/csv": {}}}
})
def download_report() -> Response:
    data = [
        {"image": "test1.jpg", "score": 0.7},
        {"image": "test2.jpg", "score": 0.1},
        {"image": "test3.jpg", "score": 0.99},
    ]
    csv_stream = io.StringIO()
    writer = csv.DictWriter(
        csv_stream, 
        fieldnames=["image", "score"],
        quoting=csv.QUOTE_ALL
        )
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    
    text = csv_stream.getvalue()
    return Response(content=text, media_type="text/csv")
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)