# AI-Powered-Traffic-Management-System
This project uses YOLO object detection, Twilio SMS, and email alerts to automatically detect and report traffic violations from a live camera feed.

✨ Features

Detects common traffic violations:

🚫 Without Helmet

👥 More Than Two Persons on Bike

📱 Using Mobile While Driving

Sends:

📧 Email alerts (with attached image proof)

📱 SMS alerts via Twilio

Records video output with detected violations highlighted

Plays an alert sound for mobile usage violation

🛠️ Tech Stack

OpenCV
 – Video capture & processing

Ultralytics YOLO
 – Object detection

Twilio
 – SMS alerts

Pygame
 – Audio alerts

Custom email module (mail.py) – Email alerts

📂 Project Structure
.
├── best.pt              # Trained YOLO model
├── mail.py              # Email sending script
├── sound.mp3            # Alert sound
├── main.py              # Main detection script
├── output_video.mp4     # Saved detection video (auto-generated)
└── README.md

⚙️ Setup Instructions
1️⃣ Clone the repo
git clone https://github.com/your-username/traffic-violation-detection.git
cd traffic-violation-detection

2️⃣ Install dependencies
pip install ultralytics opencv-python pygame twilio python-dotenv

3️⃣ Configure Environment Variables

Create a .env file in the root folder and add:

TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
TO_PHONE_NUMBER=+919876543210


⚠️ Do not hardcode your credentials in the script. Always use environment variables.

4️⃣ Run the program
python main.py


Press q to stop the detection window.

📧 Alerts

Email: Sent with violation details & captured image (mail.py handles this).

SMS: Delivered via Twilio with violation type and fine amount.

Sound: Plays for "Using Mobile" violation.

📊 Fine Rules
Violation	Fine (INR)
Without Helmet	500
More Than Two Persons	1000
Using Mobile While Driving	300
🚨 Important Notes

Replace best.pt with your trained YOLO model file.

Make sure your mail.py is configured with correct SMTP credentials.

Do not share your Twilio SID or Auth Token publicly.

📜 License

This project is licensed under the MIT License.
