Literature Survey
Introduction
Road damage detection is an active computer vision research area focused on improving transportation safety through automated inspection.
Existing Approaches
Traditional methods rely on manual inspection or image processing techniques such as edge detection and thresholding, which are sensitive to lighting and road conditions.
Deep Learning Methods
Modern object detectors including Faster R-CNN, SSD, YOLOv5, YOLOv8 and YOLOv11 provide improved speed and accuracy for road damage detection.
Research Gap
Existing datasets often contain limited samples and inconsistent annotations. Performance may decrease under varying weather and illumination.
Proposed Contribution
This project uses YOLOv11 trained on a Roboflow dataset with three classes (Pothole, Crack, Normal Road) and deploys the model through a Streamlit dashboard.
References
1. Ultralytics YOLO Documentation
2. Roboflow Documentation
3. Redmon et al., YOLO: Real-Time Object Detection
4. Bochkovskiy et al., YOLOv4
5. IEEE papers on Road Damage Detection using Deep Learning
