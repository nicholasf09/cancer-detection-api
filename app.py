from flask import Flask, request, jsonify
import uuid
import datetime
from firestore_utils import save_to_firestore, get_prediction_histories

app = Flask(__name__)

MAX_FILE_SIZE = 1_000_000  # 1 MB


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image file is sent
        if 'image' not in request.files:
            return jsonify({"status": "fail", "message": "No file provided"}), 400
        
        image = request.files['image']
        
        # Check file size
        image.seek(0, 2)  # Move the cursor to the end of the file
        file_size = image.tell()
        image.seek(0)  # Reset the cursor to the beginning
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                "status": "fail",
                "message": "Payload content length greater than maximum allowed: 1000000"
            }), 413
        
        # Mock prediction
        result, suggestion = predict_image(image)

        # Generate response
        prediction_id = str(uuid.uuid4())
        created_at = datetime.datetime.utcnow().isoformat()

        prediction_data = {
            "id": prediction_id,
            "result": result,
            "suggestion": suggestion,
            "createdAt": created_at
        }

        # Save to Firestore
        save_to_firestore(prediction_id, prediction_data)

        return jsonify({
            "status": "success",
            "message": "Model is predicted successfully",
            "data": prediction_data
        })

    except Exception as e:
        return jsonify({
            "status": "fail",
            "message": "Terjadi kesalahan dalam melakukan prediksi"
        }), 400


@app.route('/predict/histories', methods=['GET'])
def histories():
    try:
        histories = get_prediction_histories()
        return jsonify({
            "status": "success",
            "data": histories
        })
    except Exception as e:
        return jsonify({
            "status": "fail",
            "message": "Gagal mengambil data riwayat"
        }), 500


if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8080))  # Gunakan port 8080
    app.run(host='0.0.0.0', port=port, debug=True)
