import cv2
import numpy as np
from keras import models
from base64 import b64decode
import execjs

emotion_dict = {0: "Angry", 1: "Disgust", 2: "Anxious", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Relaxed"}

with open('./emotion_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()

emotion_model = models.model_from_json(loaded_model_json)
emotion_model.load_weights('./emotion_model.weights.h5')
print("Emotion model loaded successfully!")
def detect_emotion():
    cap = cv2.VideoCapture(0)
    while True:
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))
        if not ret:
            break
        face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

        print("Press S to show song list")
        

    cap.release()
    cv2.destroyAllWindows()
    return maxindex
# def capture_frame():
#     """
#     Capture a frame using the webcam or another input source.
#     Returns a base64-encoded image string.
#     """
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if not ret:
#         raise Exception("Unable to capture frame from webcam")
#     cap.release()

#     _, buffer = cv2.imencode('.jpg', frame)
#     img_base64 = f"data:image/jpeg;base64,{buffer.tobytes().hex()}"
#     return img_base64

# def detect_emotion():
#     """
#     Detect the user's emotion based on their facial expression.
#     Returns:
#         detected_emotion (str): The predicted emotion label.
#     """
#     # Capture a frame
#     image_data = capture_frame()
#     header, encoded = image_data.split(",", 1)
#     img_bytes = b64decode(encoded)
#     frame = np.frombuffer(img_bytes, dtype=np.uint8)
#     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

#     # Convert to grayscale for face detection
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

#     # Detect faces and emotions
#     for (x, y, w, h) in faces:
#         roi_gray_frame = gray_frame[y:y + h, x:x + w]
#         cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

#         # Predict the emotion
#         emotion_prediction = emotion_model.predict(cropped_img)
#         maxindex = int(np.argmax(emotion_prediction))
#         detected_emotion = emotion_dict[maxindex]
#         return detected_emotion  # Return the first detected emotion

#     # No face detected
#     return None