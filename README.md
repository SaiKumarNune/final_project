# 🌿 LeafCheck – Crop and Land Health Detection

LeafCheck is a Django-based web app that uses deep learning models to analyze crop images and predict:
- Leaf diseases
- Crop types
- Suitable land usage

## 🚀 Features

- Upload a leaf image to detect diseases
- Predict crop or land type using trained models
- User-friendly web interface built with Django templates

## 🛠️ Tech Stack

- Python, Django
- TensorFlow/Keras & PyTorch
- HTML/CSS (Jinja templates)
- SQLite3

## 🧠 Models Used

- `plant_disease_model.pth`
- `crop_classification_model.h5`
- `land_classification_model.h5`


## 🧪 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/SaiKumarNune/final_project.git
cd final_project

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver 127.0.0.1:8001
