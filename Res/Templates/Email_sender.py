import smtplib

def sender(email, otp):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('aiassistant002@gmail.com', 'dqbtzttmpvrleycd')
    subject = "Verify your email"
    content = f"""Hello,

Thank you for signing up to Fly Messenger. We will be sending an email to the email address you provided. Please verify your email and we'll send instructions on how to proceed.

To verify your account,

OTP :- {otp}

Please do not share this OTP with anyone to avoid fraudulent activities. If you're not receiving any emails from us, please check your spam folder and add us as a contact in your email account settings.

Best regards,

The Fly Messenger Team"""
    msg = f"Subject: {subject}\n\n{content}"
    server.sendmail('assistantadv00@gmail.com', email, msg)
    print("Sent successfully")
    server.quit()

def register_sender(email, name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('aiassistant002@gmail.com', 'dqbtzttmpvrleycd')
    subject = f"Registration Successful"
    content = f"""Hi {name},

We are so very happy to hear that you have successfully registered. We know how important it is for our clients to be able to get started quickly, and we've here to help you do just that.

Please take a moment to go through our getting-started guides and tutorials, as well as any other resources we may have in the sidebar of your account dashboard.

We are available by email if you need any help or support.

Thank you for choosing Assistant! We look forward to supporting your business growth in the days, weeks and months ahead.

Best regards, Artificial Assistant team"""
    msg = f"Subject: {subject}\n\n{content}"
    server.sendmail('aiassistant00@gmail.com', email, msg)
    print("Sent successfully")
    server.quit()
