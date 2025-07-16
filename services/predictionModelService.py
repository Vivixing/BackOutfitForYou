from PIL import Image
import numpy as np
import base64
from io import BytesIO
from enums.PrendaCategoria import PrendaCategoria

class_names = [e.value for e in PrendaCategoria]

def predict_model(model, image_base64:str) -> str:
    try: 
        image_bytes = base64.b64decode(image_base64)
        img = Image.open(BytesIO(image_bytes)).convert('RGBA')

        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                newData.append((255,255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

        img = img.convert('L')
        img = img.resize((28, 28))

        img_array = np.array(img) / 255.0
        img_array = img_array.reshape(1, 28, 28, 1)

        probs = model.predict(img_array)[0]
        entropy = -np.sum(probs * np.log(probs + 1e-10))

        if entropy < 0.5:
            pred_class = int(np.argmax(probs))
            return class_names[pred_class]
        elif 0.5 <= entropy <= 1.0:
            raise ValueError(f"⚠️ Predicción dudosa: entropía {entropy:.2f}.")
        else:
            raise ValueError(f"⚠️ Imagen fuera de distribución: entropía {entropy:.2f}.")

    except Exception as e:
        raise RuntimeError(f"Error en la predicción: {e}")
