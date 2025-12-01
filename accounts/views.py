from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
import json

def register_user(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        username = body.get("username")
        email = body.get("email")
        password = body.get("password")

        # create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # send welcome email
        send_mail(
            subject="Welcome!",
            message=f"Hello {username}, your account was created successfully.",
            from_email="your_email@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({"status": "success", "message": "User created and email sent"}, status=201)

    return JsonResponse({"error": "POST request required"}, status=400)
