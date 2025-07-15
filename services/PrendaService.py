
from typing import Optional
from models.PrendaModel import Prenda
from repository.PrendaRepository import PrendaRepository
from beanie import PydanticObjectId
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from enums.PrendaCategoria import PrendaCategoria

class PrendaService:

    @staticmethod
    def predict_model (model, image_base64:str) -> str:
        class_names = [e.value for e in PrendaCategoria]
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


    @staticmethod
    async def create_prenda(new_prenda: Prenda) -> Prenda:
        return await PrendaRepository.create_prenda(new_prenda)
    
    @staticmethod
    async def find_prenda_by_id(id: PydanticObjectId) -> Prenda:
        try:
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return exist_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_usuario_id(usuario_id: PydanticObjectId) -> list[Prenda]:
        try: 
            exist_prenda_usuario_id = await PrendaRepository.find_prenda_by_usuario_id(usuario_id)
            if not exist_prenda_usuario_id:
                raise Exception("No existen prendas asociadas a ese usuario ID")
            return exist_prenda_usuario_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_tipo_prenda_id(tipo_prenda_id: PydanticObjectId) -> list[Prenda]:
        try:
            exist_prenda_tipo_prenda_id = await PrendaRepository.find_prenda_by_tipo_prenda_id(tipo_prenda_id)
            if not exist_prenda_tipo_prenda_id:
                raise Exception("No existen una prendas asociadas a ese tipo de prenda ID")
            return exist_prenda_tipo_prenda_id
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_prenda_by_name(name: str) -> list[Prenda]:
        try: 
            exist_prenda_name = await PrendaRepository.find_prenda_by_name(name)
            if not exist_prenda_name:
                raise Exception("No existe una prenda con ese nombre")
            return exist_prenda_name
        except Exception as error:
            raise error
    
    @staticmethod
    async def delete_prenda(id: PydanticObjectId) -> Optional[Prenda]:
        try: 
            exist_prenda_id = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda_id:
                raise Exception("No existe una prenda con ese ID")
            return await PrendaRepository.delete_prenda(id)
        except Exception as error:
            raise error
    
    @staticmethod
    async def find_all_prendas() -> list[Prenda]:
        try:
            prendas = await PrendaRepository.find_all_prendas()
            if not prendas:
                raise Exception("No existen prendas registradas")
            return prendas
        except Exception as error:
            raise error
    
    @staticmethod
    async def update_prenda(id: PydanticObjectId, update_prenda: dict) -> Prenda:
        try:
            exist_prenda = await PrendaRepository.find_prenda_by_id(id)
            if not exist_prenda:
                raise Exception("No existe una prenda con ese ID")
            
            return await PrendaRepository.update_prenda(id, update_prenda)
        except Exception as error:
            raise error