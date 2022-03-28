import json
from rest_framework import generics
from rest_framework import status as codes
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import RegisterView
from rest_framework.authentication import TokenAuthentication
from rest_auth.views import LoginView, LogoutView
from .models import Profile, User
from .serializers import ProfileSerializer


class PeopleList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)


class Login(LoginView):
    BODY_TYPE = "dict"
    JSON_BODY_PARAMS = ["username", "password"]

    @property
    def login_headers(self):
        return {"CONTENT_TYPE": "application/json"}

    def post(self, request, *args, **kwargs):
        body = request.data
        try:
            account = User.objects.get(
                username=body["username"]
            )
            token = super().post(request, *args, **kwargs).data["key"]
            response = build_response("login", account, token)
            status = codes.HTTP_200_OK
        except User.DoesNotExist:
            response = {"error": "User not found"}
            status = codes.HTTP_400_BAD_REQUEST
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class Logout(LogoutView):
    """
    Description
    ----------
    Class used to log out from session in Platform CaliSabor

    Methods available : POST
    """
    HEADERS = {}
    BODY_TYPE = "dict"

    def post(self, request, *args, **kwargs):
        """
        Description
        ----------
        Post method

        Arguments
        ---------
        request
            request with account data
        *args
            List of variable arguments

        **kwargs
            keyword arguments

        Return
        -------
        HttpResponse
            Response object
        """
        super().post(request, *args, **kwargs)
        response = build_response("logout")
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class Register(RegisterView):
    """
    Description
    ----------
    Class used to register a new user to platform CaliSabor

    Methods available : POST
    """

    HEADERS = {"CONTENT_TYPE": "application/json"}
    BODY_TYPE = "dict"

    def post(self, request, *args, **kwargs):
        """
        Description
        ----------
        Post method used to register new users. Path: /register

        Arguments
        ---------
        request
            request with account data
        *args
            List of variable arguments

        **kwargs
            keyword arguments

        Return
        -------
        HttpResponse
            Response object
        """
        body = request.data
        data = {
            "username": body["username"],
            "first_name": body["first_name"],
            "last_name": body["last_name"],
            "password1": body["password1"],
            "password2": body["password2"],
            "email": body["email"],
            "mobile": body["mobile"],
            "position": body["position"],
            "phone": body.get("phone", ""),
            "profile_pic": body.get("profile_pic", ""),
            "birthday": body.get("birthday", ""),
            "country": body.get("country", ""),
            "city": body.get("city", "")
        }
        # Create new user with new password
        new_user = User.objects.create_user(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        new_user.set_password(data['password1'])
        if data['position'] == 'superuser':
            new_user.is_superuser = True
            new_user.is_staff = True
        new_user.save()

        # Create Profile
        status = codes.HTTP_200_OK
        new_profile = Profile(
            user=new_user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            mobile=data['mobile'],
            profile_pic="",
            position=data['position'],
            birthday=data['birthday'],
            country=data['country'],
            city=data['city']
        )
        new_profile.save()
        response = build_response('register', new_profile)
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class ResetPassword(RegisterView):
    """
    Description
    ----------
    Class used to change password for user in platform CaliSabor

    Methods available : POST
    """

    HEADERS = {"CONTENT_TYPE": "application/json"}
    BODY_TYPE = "dict"

    def post(self, request, *args, **kwargs):
        """
        Description
        ----------
        Post method used to register new users. Path: /register

        Arguments
        ---------
        request
            request with account data
        *args
            List of variable arguments

        **kwargs
            keyword arguments

        Return
        -------
        HttpResponse
            Response object
        """
        body = request.data
        data = {
            "username": body["username"],
            "old_password": body["old_password"],
            "new_password": body["new_password"]
        }
        # Check old password and change if correct
        user = User.objects.get(
            username=data['username']
        )
        if user.check_password(data['old_password']):
            user.set_password(data['new_password'])
            user.save()
            response = build_response('change_password')
        else:
            response = {"password_changed": False,
                        "message": "La contraseña no coincide"}

        # Create Response
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


def build_response(transaction, account_obj=None, usr_token=None):
    """
    Description
    ----------

    Build the response of login and logout access points.

    Arguments
    ---------
    transaction: str
        Type of transaction. Possible values: login, logout

    account_obj: User Model
        User data

    usr_token: str
        Account token. Used to give access to other functionalities of the platform

    Return
    -------
    val_response: dict
        Dictionary with response

    """

    if transaction == "login":
        first_name = account_obj.first_name if account_obj else None
        last_name = account_obj.last_name if account_obj else None
        last_login = account_obj.last_login if account_obj else None

        return {
            "first_name": first_name,
            "last_name": last_name,
            "user_token": usr_token,
            "last_login": str(last_login) if last_login else None
        }
    elif transaction == "logout":
        return {"logout": True}
    elif transaction == "register":
        return {"full_name": account_obj.first_name + " " + account_obj.last_name,
                "position": account_obj.position,
                "register_completed": True}
    elif transaction == "change_password":
        return {"password_changed": True}
    else:
        raise RuntimeError()
