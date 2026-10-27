# 🌿 CropCare AI

## Crop Disease Detection Using Convolutional Neural Networks

**CropCare AI** is a web-based AI application that detects common diseases in **tomato and potato leaves** from an uploaded image. The system uses a **Convolutional Neural Network (CNN)** trained using labeled leaf-image data and provides the predicted condition, confidence score, treatment information, and prevention suggestions through a simple web interface.

The project demonstrates how **deep learning, computer vision, and web development** can be combined to create a practical crop-disease detection system.

> **Current model scope:** 6 classes covering healthy leaves, early blight, and late blight for tomato and potato.

---

## 🌱 What Does CropCare AI Do?

CropCare AI follows a simple three-step process:

### 1. Upload
The user uploads a photograph of a crop leaf through the web interface. JPG, PNG, and WEBP images are supported.

### 2. Analyze
The uploaded image is processed by a trained **Convolutional Neural Network (CNN)** using TensorFlow/Keras.

### 3. Act
The application displays:

- Detected crop
- Predicted disease/healthy condition
- Prediction confidence
- Top three possible predictions
- Disease description
- Treatment suggestions
- Prevention suggestions

The application also maintains a history of recent scans directly in the user's browser.

---

## 🎯 Problem Statement

Crop diseases can significantly affect crop quality and agricultural productivity when they are not identified at an early stage. Identifying diseases manually may also require agricultural expertise that may not always be immediately available.

CropCare AI explores the use of **deep learning-based image classification** to provide preliminary identification of crop diseases from leaf images through an easy-to-use web application.

---

## 💡 Objectives

- Develop a CNN-based crop disease classification model.
- Detect selected diseases from tomato and potato leaf images.
- Provide a simple web interface for image upload and analysis.
- Display prediction confidence and alternative predictions.
- Provide treatment and prevention information for supported diseases.
- Demonstrate the integration of an AI model with a Flask web application.
- Create a foundation that can be extended to additional crops and diseases.

---

## 🧠 Machine Learning Approach

CropCare AI uses a **Convolutional Neural Network (CNN)** implemented using TensorFlow/Keras.

### Model Pipeline

```text
Input Leaf Image
       ↓
Image Resizing (128 × 128)
       ↓
Data Augmentation
       ↓
Convolutional Layers
       ↓
Batch Normalization
       ↓
Max Pooling
       ↓
Convolutional Layers
       ↓
Global Average Pooling
       ↓
Dense Layer
       ↓
Dropout
       ↓
Softmax Classification
       ↓
Predicted Crop Disease
```

### Training Configuration

| Parameter | Value |
|---|---|
| Image Size | 128 × 128 |
| Batch Size | 32 |
| Validation Split | 20% |
| Epochs | Up to 20 |
| Random Seed | 42 |
| Framework | TensorFlow / Keras |
| Model Type | CNN |
| Output | 6-class classification |

### Data Augmentation

The model uses augmentation techniques to improve generalization:

- Random horizontal flipping
- Random rotation
- Random zoom

---

## 🌿 Supported Classes

The current model is trained on six classes:

| Crop | Condition |
|---|---|
| Potato | Early Blight |
| Potato | Healthy |
| Potato | Late Blight |
| Tomato | Early Blight |
| Tomato | Healthy |
| Tomato | Late Blight |

The current implementation therefore focuses specifically on these **six classes** rather than claiming to detect every crop or plant disease.

---

## 📊 Model Performance

The trained model achieved approximately:

### **93.46% Validation Accuracy**

This is the validation accuracy obtained during training on the current six-class dataset.

The result demonstrates that the CNN can effectively distinguish between the supported crop-health categories within the project dataset.

> Validation accuracy should not be interpreted as guaranteed accuracy on arbitrary real-world photographs. Performance can vary depending on image quality, lighting, background, camera conditions, and similarity to the training data.

---

## 🖥️ Web Application

The web application is developed using **Flask** as the backend with HTML, CSS, and JavaScript on the frontend.

### Main Features

- 🌿 CropCare AI landing page
- 📷 Leaf image upload
- 🖱️ Drag-and-drop image upload
- 👁️ Image preview
- 🤖 CNN-based disease prediction
- 📈 Confidence score visualization
- 🩺 Healthy/disease status
- 💊 Treatment recommendations
- 🛡️ Prevention recommendations
- 🔎 Top-three prediction results
- 🕘 Recent scan history
- 🧹 Clear history option
- ⚠️ Low-confidence warning
- 📱 Responsive user interface

---

## 🔄 Application Workflow

```text
User uploads a leaf image
          ↓
Frontend validates the image
          ↓
Image is sent to Flask /predict endpoint
          ↓
Flask preprocesses the image
          ↓
Trained CNN analyzes the image
          ↓
Model generates class probabilities
          ↓
Top prediction and confidence are selected
          ↓
Disease information is retrieved
          ↓
Result is returned to the frontend
          ↓
User sees disease/health status
          ↓
Treatment and prevention information is displayed
          ↓
Scan is stored in browser history
```

---

## 🗂️ Project Structure

```text
crop-disease-detection/
│
├── app.py
├── train_model.py
├── disease_info.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── model/
│   ├── crop_model.keras
│   ├── class_names.json
│   └── training_curves.png
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    └── index.html
```

The training dataset is kept separately and is not included in the GitHub repository.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| TensorFlow | Machine learning framework |
| Keras | CNN development and training |
| Flask | Backend web framework |
| HTML | Webpage structure |
| CSS | User interface design |
| JavaScript | Frontend interaction and API communication |
| Pillow | Image processing |
| NumPy | Numerical computation |
| Matplotlib | Training visualization |
| PlantVillage | Leaf-image dataset |

---

## 📁 Main Project Files

### `app.py`

The Flask backend of CropCare AI.

It:

- Loads the trained CNN model.
- Loads the class names.
- Receives uploaded leaf images.
- Preprocesses images.
- Performs predictions.
- Calculates confidence.
- Retrieves disease information.
- Sends the prediction back to the frontend.

---

### `train_model.py`

Responsible for training the CNN.

It:

- Loads images from the dataset.
- Creates training and validation datasets.
- Applies image augmentation.
- Builds the CNN architecture.
- Trains the model.
- Evaluates validation performance.
- Saves the trained model.
- Saves class names.
- Generates training curves.

---

### `disease_info.py`

Contains information associated with supported crop conditions, including:

- Disease descriptions
- Treatment suggestions
- Prevention suggestions

---

### `templates/index.html`

Contains the main structure of the CropCare AI web interface, including:

- Navigation bar
- Hero section
- Image upload section
- Prediction result section
- Scan history
- How-it-works section
- Footer

---

### `static/script.js`

Handles frontend functionality such as:

- Image selection
- Drag-and-drop
- Image preview
- Upload validation
- Sending images to Flask
- Displaying prediction results
- Confidence visualization
- Recent scan history

---

### `static/style.css`

Controls the visual appearance of the application, including:

- Colors
- Layout
- Cards
- Buttons
- Upload area
- Result section
- History cards
- Responsive design
- Animations

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/crop-disease-detection.git
cd crop-disease-detection
```

### 2. Create a virtual environment

Python 3.10 or 3.11 is recommended.

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model

Place the dataset inside the appropriate class folders and run:

```bash
python train_model.py
```

The training process generates:

```text
model/crop_model.keras
model/class_names.json
model/training_curves.png
```

### 5. Run the web application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 📷 Image Requirements

The application accepts:

- JPG / JPEG
- PNG
- WEBP

Maximum frontend upload size:

**5 MB**

For better predictions, use:

- A clear image
- Good lighting
- A single leaf
- A relatively plain background
- A leaf similar to the type of images used during training

---

## ⚠️ Limitations

The current prototype has several limitations:

- The model supports only six classes.
- It is primarily designed for leaf images similar to its training data.
- The classifier can still produce a prediction for an unrelated image because it is a closed-set classifier.
- High confidence does not guarantee real-world correctness.
- Performance may decrease on field photographs with complex backgrounds, poor lighting, damaged leaves, or unseen disease patterns.
- Treatment and prevention information is provided for informational purposes and should not replace professional agricultural advice.
- Scan history is currently stored in browser `localStorage` rather than a server-side database.
- The current implementation is a prototype and requires broader datasets and real-world field testing before production deployment.

---

## 🔮 Future Scope

CropCare AI can be further improved by:

- Adding more crops and disease classes.
- Training with larger and more diverse field images.
- Adding a dedicated invalid-image/non-leaf detection mechanism.
- Improving robustness to different lighting and backgrounds.
- Adding multilingual support for farmers.
- Developing a Progressive Web App (PWA).
- Adding persistent cloud/database-based scan history.
- Adding voice-based interaction.
- Integrating weather and crop-condition information.
- Deploying the application to a cloud platform.
- Providing more personalized recommendations based on crop and location.

---

## 📌 Dataset

The project uses labeled crop-leaf images for training the CNN.

The current model contains six classes covering tomato and potato leaves.

The complete dataset is **not included in this repository** because of its size. The repository contains the implementation, trained model files, and documentation required to understand the project.

---

## 📈 Example Prediction

For a healthy potato leaf, CropCare AI can produce an output such as:

```text
Crop: Potato
Condition: Healthy
Confidence: 99.98%
Status: Healthy
```

The application also displays alternative predictions and relevant prevention information.

---

## 🎓 Project Significance

CropCare AI demonstrates the practical application of **Artificial Intelligence and Computer Vision in agriculture**.

Instead of requiring a user to understand the underlying machine-learning model, the system provides a simple interface:

```text
Leaf Image → AI Analysis → Disease Prediction → Actionable Information
```

This makes the project a practical demonstration of integrating a trained deep-learning model into a usable software application.

---

## 📚 References

- PlantVillage Dataset
- TensorFlow / Keras Documentation
- Flask Documentation
- Python Documentation

---

## ⭐ Conclusion

**CropCare AI** combines deep learning, image classification, and web development to create a crop-disease detection prototype.

The current CNN model is capable of classifying six tomato and potato leaf conditions, while the Flask-based application provides an accessible interface for uploading images and receiving predictions, confidence scores, treatment information, and prevention guidance.

The project provides a foundation for developing a larger agricultural AI system by expanding the dataset, increasing the number of supported crops and diseases, and testing the model on diverse real-world field images.