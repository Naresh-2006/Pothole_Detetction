# 🛣️ Pothole Detection using YOLOv11

## 📌 Overview

This project detects potholes, road cracks, and normal road surfaces using the YOLOv11 object detection model. The model is trained on a custom dataset exported from Roboflow and provides an easy-to-use Streamlit dashboard for image-based detection.

---

## 👨‍💻 Project Developed by 
- Naresh Kumar T A 

Department of Artifical Intelligence and Machine Learning

Sri Krishna College of Technology

---

## 🎯 Objectives

- Detect potholes on road surfaces
- Detect road cracks
- Identify normal road regions
- Demonstrate AI-based road damage detection

---

## 📂 Dataset

Dataset Source:
Roboflow

Classes:
- Pothole
- Crack
- Normal Road

Dataset Split:

- Training Images: 592
- Validation Images: 127
- Testing Images: 91

---

## 🛠️ Technologies Used

- Python
- YOLOv11
- Ultralytics
- Roboflow
- Streamlit
- OpenCV
- PyTorch
- NumPy
- Matplotlib

---

## 📁 Project Structure

```
Pothole_detection_Project/
│
├── app.py
├── requirements.txt
├── README.md
├── models/
│     └── best.pt
├── utils/
│     ├── detector.py
│     └── helper.py
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <repository_link>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

## 🚀 Features

- Upload road images
- Detect potholes
- Detect road cracks
- Detect normal road
- Display bounding boxes
- Detection summary
- Confidence-based predictions

---

## 📊 Model

Model:
YOLOv11

Framework:
Ultralytics

Task:
Object Detection

---

## 📷 Sample Output

(Add screenshots here after completing the project.)

---

## 🚀 Future Improvements

- Improve dataset quality
- Increase training data
- Reduce false detections
- Real-time video detection
- GPS-based pothole mapping
- Edge-device deployment

---

## 📜 License

This project is developed for academic purposes.