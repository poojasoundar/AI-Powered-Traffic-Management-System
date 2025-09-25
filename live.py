import cv2 
import time 
from ultralytics import YOLO 
from mail import report_send_mail 
from pygame import mixer 
from twilio.rest import Client  # Twilio SMS 
from datetime import datetime, timedelta 

# Load the YOLO11 model 
model = YOLO("best.pt") 

# Twilio credentials 
twilio_account_sid = "yourid" 
twilio_auth_token = "yourtoken" 
twilio_phone_number = "+19342204528" 


# Initialize Twilio client 
twilio_client = Client(twilio_account_sid, twilio_auth_token) 

# Function to send SMS using Twilio 
def send_sms_violation_alert(violation, amount): 
    try: 
        message = f"Alert: Violation Detected - {violation}. Fine Rs. {amount}. Please check your email for further details." 
        twilio_client.messages.create( 
            body=message, 
            from_=twilio_phone_number, 
            to=to_phone_number 
        ) 
        print(f"SMS sent: {message}") 
    except Exception as e: 
        print(f"Failed to send SMS: {e}") 

# Open the default camera (index 0) 
cap = cv2.VideoCapture(0) 

# Check if the camera opened successfully 
if not cap.isOpened(): 
    print("Error: Unable to open camera.") 
    exit() 

# Get the camera's width and height 
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height = int
