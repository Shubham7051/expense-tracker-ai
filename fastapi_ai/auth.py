import os
import sys
import django


# fastapi_ai/auth.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

DJANGO_ROOT = os.path.join(PROJECT_ROOT, "drf_backend")

sys.path.append(DJANGO_ROOT)


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "drf_backend.settings"
)

django.setup()


from rest_framework_simplejwt.tokens import AccessToken


def verify_token(token: str):
    try:
        decoded_token = AccessToken(token)
        return decoded_token

    except Exception as e:
        print("JWT Error:", e)
        return None