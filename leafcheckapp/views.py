import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import load_trained_resnet18
from django.contrib.auth.decorators import login_required
from PIL import Image
from .disease import disease_dic
import io
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from markupsafe import Markup
from django.shortcuts import render
import tensorflow as tf
import json
from django.http import JsonResponse
import numpy as np
from .land_crop_recommendations import land_crop_recommendations, get_mismatch_message

disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']


# Load trained model
disease_model_path = 'models/plant_disease_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
disease_model = load_trained_resnet18(len(disease_classes), disease_model_path, device)

@login_required(login_url='login')
def disease(request):
    return render(request, 'disease.html')

def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image (bytes)
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img)).convert('RGB')
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0).to(device)

    # Get predictions from model
    with torch.no_grad():
        logps = model(img_u)
        ps = torch.exp(logps)
        top_p, top_class = ps.topk(1, dim=1)
        prediction = disease_classes[top_class[0].item()]

    return prediction

def disease_prediction(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return redirect(request.url)

        file = request.FILES['file']
        if not file:
            return render(request, 'disease.html')

        try:
            img = file.read()
            prediction_class = predict_image(img)

            # ✅ Map prediction class to user-friendly description using disease_dic
            if prediction_class in disease_dic:
                prediction = Markup(disease_dic[prediction_class])
            else:
                prediction = Markup(f"Unknown disease: {prediction_class}")

            return render(request, 'disease-result.html', context={"prediction": prediction})
        except Exception as e:
            print(f"Prediction error: {e}")
            return render(request, 'disease.html')

    return render(request, 'disease.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'index.html')


import re

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(username) < 6:
            messages.error(request, "Username must be at least 6 characters long")
            return redirect('signup')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Invalid email address")
            return redirect('signup')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('signup')

        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()
        return redirect('home')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

from django.core.mail import send_mail
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return render(request, 'contact.html')

        try:
            subject = f"New message from {name} ({email})"
            email_message = f"Name: {name}\nEmail: {email}\n\n{message}"
            from_email = 'agricultureproject.ai@gmail.com'
            recipient_list = ['agricultureproject.ai@gmail.com']
            
            send_mail(subject, email_message, from_email, recipient_list)
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send message. Error: {e}")
        
        return render(request, 'contact.html')

    return render(request, 'contact.html')

# Load models once (global loading for efficiency)
LAND_MODEL_PATH = 'models/land_classification_model.h5'
CROP_MODEL_PATH = 'models/crop_classification_model.h5'
land_model = tf.keras.models.load_model(LAND_MODEL_PATH)
crop_model = tf.keras.models.load_model(CROP_MODEL_PATH)

# Load class indices (land and crop)
with open('models/land_class_indices.json', 'r') as f:
    land_class_indices = json.load(f)

with open('models/crop_class_indices.json', 'r') as f:
    crop_class_indices = json.load(f)

land_class_names = {v: k for k, v in land_class_indices.items()}
crop_class_names = {v: k for k, v in crop_class_indices.items()}

# Image preprocessing function
def preprocess_image(img_file, img_size=(128, 128)):  # MATCH TRAINING SIZE
    img = Image.open(img_file).convert('RGB')
    img = img.resize(img_size)
    img = np.array(img) / 255.0  # Normalize to 0-1
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def ajax_predict(request):
    if request.method == 'POST':
        land_image = request.FILES.get('land_image')
        crop_image = request.FILES.get('crop_image')

        if not land_image or not crop_image:
            return JsonResponse({'error': 'Both images are required.'}, status=400)

        land_img_array = preprocess_image(land_image, (128, 128))
        crop_img_array = preprocess_image(crop_image, (128, 128))

        # Predictions
        land_prediction_array = land_model.predict(land_img_array)
        crop_prediction_array = crop_model.predict(crop_img_array)

        land_class_idx = np.argmax(land_prediction_array)
        crop_class_idx = np.argmax(crop_prediction_array)

        land_prediction = land_class_names.get(land_class_idx, 'Unknown')
        crop_prediction = crop_class_names.get(crop_class_idx, 'Unknown')

        # Suitability check and recommendation
        suitability_message = ""
        if (land_prediction, crop_prediction) in land_crop_recommendations:
            suitability_message = land_crop_recommendations[(land_prediction, crop_prediction)]
        else:
            suitability_message = get_mismatch_message(land_prediction)

        return JsonResponse({
            'land_prediction': land_prediction,
            'crop_prediction': crop_prediction,
            'suitability_message': suitability_message
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required(login_url='login')
def image_prediction(request):
    return render(request, 'prediction.html')