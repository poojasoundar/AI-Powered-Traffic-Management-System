
import os
import cv2
import time
from ultralytics import YOLO
from mail import report_send_mail
from pygame import mixer
from twilio.rest import Client  # Twilio SMS
from datetime import datetime, timedelta

# Load the YOLO model
model = YOLO("best.pt")

# Read Twilio credentials & phone numbers from environment variables
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
to_phone_number = os.getenv("TO_PHONE_NUMBER")

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
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output_video.mp4", fourcc, 30, (width, height))

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from camera.")
        break

    # Perform object detection on the frame
    results = model.predict(frame)

    # Initialize a list to store detected violations
    detected_violations = []

    # Draw the detection results on the frame
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = results[0].names[int(box.cls[0])]
        confidence = round(box.conf[0].item(), 2)

        # Draw bounding box and label on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} {confidence}", cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Collect detected violations
        detected_violations.append(label)

    # Handle detected violations and apply fines
    fine_details = []
    for violation in detected_violations:
        if violation == 'WITHOUT_HELMET':
            print('Violation Detected! WITHOUT_HELMET')
            fine_amount = 500
            fine_details.append(('WITHOUT_HELMET', fine_amount))
            time.sleep(2)
            cv2.imwrite('image.jpg', frame)
            report_send_mail('WITHOUT_HELMET', 'image.jpg', fine_amount)
            send_sms_violation_alert('WITHOUT_HELMET', fine_amount)

        elif violation == 'MORE_THAN_TWO_PERSONS':
            print('Violation Detected! MORE_THAN_TWO_PERSONS')
            fine_amount = 1000
            fine_details.append(('MORE_THAN_TWO_PERSONS', fine_amount))
            time.sleep(2)
            cv2.imwrite('image.jpg', frame)
            report_send_mail('MORE_THAN_TWO_PERSONS', 'image.jpg', fine_amount)
            send_sms_violation_alert('MORE_THAN_TWO_PERSONS', fine_amount)

        elif violation == 'USING_MOBILE':
            print('Violation Detected! USING_MOBILE')
            fine_amount = 300
            fine_details.append(('USING_MOBILE', fine_amount))
            time.sleep(2)
            cv2.imwrite('image.jpg', frame)
            report_send_mail('USING_MOBILE', 'image.jpg', fine_amount)
            send_sms_violation_alert('USING_MOBILE', fine_amount)

            # Play sound for mobile usage violation
            try:
                mixer.init()
                mixer.music.load("sound.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()
            except:
                print('Issues in Speaker')

    # Display total fine amount for the frame
    total_fine = sum([fine for _, fine in fine_details])
    print(f"Total fine amount for detected violations: {total_fine}")

    # Display the frame
    cv2.imshow("Object Detection", frame)

    # Write the frame to the output video
    out.write(frame)

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()
