from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
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

        # Validate
        if not username or not email or not password:
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Check if user exists
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

        # Send confirmation email
        send_mail(
            subject="Welcome!",
            message=f"Hello {username}, your account was created successfully.",
            from_email="your_email@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"status": "success", "message": "User created & email sent"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
