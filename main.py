import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras

# Load the pre-trained MobileNet V2 model from TensorFlow Hub
feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(224, 224, 3),
                                         trainable=False)

# Define the model architecture
model = keras.Sequential([
    keras.layers.InputLayer(input_shape=(224, 224, 3)),
    keras.layers.Lambda(lambda x: feature_extractor_layer(x)),
    keras.layers.Dense(9, activation='softmax')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Load the trained weights
model.load_weights("C:/Users/Hp/Downloads/skin/my_model.weights.h5")

# Define disease labels
disease_labels = {
    0: 'cellulitis',
    1: 'impetigo',
    2: 'athlete-foot',
    3: 'nail-fungus',
    4: 'ringworm',
    5: 'cutaneous-larva-migrans',
    6: 'chickenpox',
    7: 'shingles',
    8: 'normal'
}

# Function to preprocess image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize pixel values
    return img

# Function to predict disease
def predict_disease(image_path):
    img = preprocess_image(image_path)
    prediction = model.predict(img)
    predicted_label = disease_labels[np.argmax(prediction)]
    return predicted_label

# Function to handle file selection
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        canvas.image = photo
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        result_label.config(text="")
        global selected_image_path
        selected_image_path = file_path

def predict():
    if selected_image_path:
        disease_label = predict_disease(selected_image_path)
        result_label.config(text="Predicted Disease: " + disease_label)
    else:
        result_label.config(text="Please select an image first")

# Create the main window
root = tk.Tk()
root.title("Skin Disease Predictor")

# Create widgets
label = tk.Label(root, text="Select an image of a skin lesion:")
label.pack(pady=10)

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

predict_button = tk.Button(root, text="Predict", command=predict)
predict_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Run the application
root.mainloop()
