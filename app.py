#flask --app index run --debug

from PIL import Image, UnidentifiedImageError
import numpy as np
import io, base64
from flask import Flask, request, jsonify
from deepface import DeepFace
import time
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.post("/")
def start():
    start_time = time.time()
    if request.json:
        ref_img_data = request.json.get('refImg')
        compare_img_base64 = request.json.get('compareImg')
        
        compare_img_base64 = compare_img_base64.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(compare_img_base64)
            
            image = Image.open(io.BytesIO(image_bytes))
            
            numpy_array = np.array(image)
            
            result = DeepFace.verify(
                img1_path='../back_end' + ref_img_data['refImage'],
                img2_path=numpy_array,
                model_name="facenet"
            )
            end_time = time.time() 
            execution_time = end_time - start_time

            
            if result["verified"]:
                return jsonify({
                    "message": "YEAYY BERHASIL ANDA TERVERIFIKASI MAMANK",
                    "success": result['verified'],
                    "waktu eksekusi": execution_time
                }), 200
            else:
                return jsonify({
                    "message": "LU SAPEE????",
                    "success": result['verified'],
                    "waktu eksekusi": execution_time
                }), 403
            
            
        except ValueError as e:
            end_time = time.time() 
            execution_time = end_time - start_time
            return jsonify({
                "message": "Muka Kamu gak Keliatan, gak punya muka kah?",
                "success": False,
                "waktu eksekusi": execution_time
            }), 400
    
    else:
        end_time = time.time() 
        execution_time = end_time - start_time
        return jsonify({
            "message": "MANA FILENYA KAMPRET", 
            "waktu eksekusi": execution_time
        }), 403

if __name__ == '__main__':
    app.run(debug=True)
