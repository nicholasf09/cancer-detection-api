from google.cloud import firestore

db = firestore.Client()

def save_to_firestore(prediction_id, prediction_data):
    """
    Save prediction data to Firestore.
    """
    doc_ref = db.collection('predictions').document(prediction_id)
    doc_ref.set(prediction_data)

def get_prediction_histories():
    """
    Retrieve prediction histories from Firestore.
    """
    predictions_ref = db.collection('predictions')
    docs = predictions_ref.stream()
    histories = []
    for doc in docs:
        histories.append({
            "id": doc.id,
            "history": doc.to_dict()
        })
    return histories
