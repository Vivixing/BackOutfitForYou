from tensorflow import keras
import asyncio

def load_h5_model():
    model = keras.models.load_model('deepLearning_model/cnn_model_v4.h5')
    return model

async def load_h5_model_main():
    loop = asyncio.get_event_loop()
    model = await loop.run_in_executor(None, load_h5_model)
    return model