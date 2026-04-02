import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# --- Configurations ---
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-2.5-flash')

# Email details
EMAIL_USER = "rt.16apr1994@gmail.com"
EMAIL_PASS = "your-app-password"
EXPERT_EMAIL = "rt.16apr1994@gmail.com"

def send_email_to_expert(student_query):
    msg = EmailMessage()
    msg.set_content(f"A student needs help with: \n\n{student_query}")
    msg['Subject'] = "New Student Inquiry - AI Tutor"
    msg['From'] = EMAIL_USER
    msg['To'] = EXPERT_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Logic: Agar student satisfied nahi hai
    if 'not satisfied' in incoming_msg or 'email' in incoming_msg:
        # Aap chahein to last question save kar sakte hain, abhi hum generic bhej rahe hain
        send_email_to_expert(incoming_msg)
        msg.body("Aapka sawal expert ko bhej diya gaya hai. Wo jald hi contact karenge.")
    
    else:
        # AI Response logic
        ai_response = model.generate_content(incoming_msg)
        reply_text = f"{ai_response.text}\n\n---\nSatisfied nahi hain? Type 'Email' to ask an expert."
        msg.body(reply_text)

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
