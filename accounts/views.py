from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        body = json.loads(request.body.decode("utf-8"))
        username = body.get("username")
        email = body.get("email")
        password = body.get("password")

        # Validate fields
        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Check duplicates
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        # ---------------------------
        # SEND BEAUTIFUL HTML EMAIL
        # ---------------------------
        subject = " Welcome to Our Platform!"
        from_email = "your_email@gmail.com"
        text_content = f"Hello {username}, welcome!"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background:#f5f6fa; padding:20px;">
            <div style="max-width:600px; margin:auto; background:white; padding:30px; 
                        border-radius:10px; box-shadow:0px 4px 14px rgba(0,0,0,0.1);">

                <h2 style="color:#4b7bec; text-align:center;">Welcome, {username}! </h2>

                <p style="font-size:15px; color:#333;">
                    Your account has been created successfully!  
                    We're excited to have you onboard — your journey starts now.
                </p>

                <div style="margin-top:20px;">
                    <p style="font-size:15px; color:#555;">
                        ✔ Username: <b>{username}</b><br>
                        ✔ Email: <b>{email}</b>
                    </p>
                </div>

                <p style="margin-top:30px; color:#555;">
                    If you didn’t sign up, please ignore this message.
                </p>

                <p style="margin-top:40px; text-align:center; color:#4b7bec; font-weight:bold;">
                    — The Support Team
                </p>
            </div>
        </body>
        </html>
        """

        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # fallback text for very old clients
            from_email=from_email,
            to=[email],
        )

        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        return JsonResponse({"status": "success", "message": "User created & email sent"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
