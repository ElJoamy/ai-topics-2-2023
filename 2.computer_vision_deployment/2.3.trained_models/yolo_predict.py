import argparse
from predictor import CatsPredictor
import pathlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")

    args = parser.parse_args()

    target_path = pathlib.Path(args.image_path)

    if not target_path.exists():
        print("Imagen no existe")
        return

    print("cargando predictor")
    predictor = CatsPredictor()
    print("prediciendo...")
    results = predictor.predict_file(args.image_path)
    print(f"resultados: {results}")

if __name__ == "__main__":
    main()