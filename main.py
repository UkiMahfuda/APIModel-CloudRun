from flask import Flask, request, jsonify
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.efficientnet import preprocess_input
import tensorflow as tf
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

interpreter = tf.lite.Interpreter(model_path='converted_model_RIPAD_PART3.tflite')  
interpreter.allocate_tensors()

labels = ['Brown Spot', 'Bacterial Leaf Blight', 'Normal', 'Blast', 'Tungro']

disease_info = {
    "Brown Spot": {
      "gejala": "Bercak-bercak coklat pada daun dengan tepian yang kabur, sering kali menyebabkan penurunan produktivitas jika tidak segera ditangani.",
      "pengobatan": "Gunakan fungisida yang mengandung Mancozeb atau Propiconazole secara teratur, hindari kelembapan berlebih, dan pastikan rotasi tanaman dilakukan."
    },
    "Bacterial Leaf Blight": {
      "gejala": "Daun menunjukkan bercak air dengan batas yang jelas, seringkali dimulai dari ujung daun dan dapat menyebar cepat terutama di kondisi lembap.",
      "pengobatan": "Gunakan antibiotik berbasis tembaga sesuai petunjuk, perbaiki sistem drainase untuk mengurangi kelembapan, dan gunakan benih yang tahan penyakit."
    },
    "Normal": {
      "gejala": "Tidak ada gejala penyakit, tanaman dalam kondisi sehat dengan daun hijau dan produktivitas optimal.",
      "pengobatan": "Tidak diperlukan pengobatan, namun disarankan untuk tetap menjaga kesehatan tanaman melalui pemupukan rutin dan pengawasan hama secara berkala."
    },
    "Blast": {
      "gejala": "Bercak coklat dengan titik hitam kecil di tengahnya, seringkali muncul di daun dan batang. Serangan parah dapat menyebabkan kerontokan daun.",
      "pengobatan": "Gunakan fungisida berbahan aktif Tricyclazole atau Isoprothiolane segera setelah gejala muncul, dan pastikan penggunaan pupuk nitrogen tidak berlebihan."
    },
    "Tungro": {
      "gejala": "Daun menguning dengan pola yang tidak merata, tanaman kerdil, dan pertumbuhannya terhambat. Tanaman bisa mati jika serangan sangat parah.",
      "pengobatan": "Gunakan insektisida untuk mengendalikan vektor penyakit ini (nyamuk hijau) dan tanam varietas padi yang tahan tungro untuk mencegah penyebaran."
    }
  }

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        img = Image.open(io.BytesIO(image_file.read()))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img = img.resize((224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], x)

        interpreter.invoke()

        output_details = interpreter.get_output_details()
        proba = interpreter.get_tensor(output_details[0]['index'])[0]

        max_index = np.argmax(proba)
        max_label = labels[max_index]
        max_proba = proba[max_index]

        result = {
            'label': max_label,
            'probability': float(max_proba * 100),
            'gejala': disease_info[max_label]['gejala'],
            'pengobatan': disease_info[max_label]['pengobatan']
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
