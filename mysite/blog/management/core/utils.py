from blog import models
from django.contrib.auth import get_user_model
import hashlib
from django.core.exceptions import ObjectDoesNotExist

UserModel = get_user_model()


def get_user(username: str, create_if_not_exists=True):
    try:
        user = UserModel.objects.get(username=username)
    except ObjectDoesNotExist:
        user = UserModel.objects.create_user(username=username, password="MyPassword")

    return user
