import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Client


@method_decorator(csrf_exempt, name="dispatch")
class NewClient(APIView):
    """

    """
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)
    HEADERS = {"CONTENT_TYPE": "application/json"}
    BODY_TYPE = "dict"

    def post(self, request, *args, **kwargs):
        """
        Description
        ----------
        Post method used to register new clients

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
            "client_name": body["client_name"],
            "nit": body["nit"],
            "ceo_name": body["ceo_name"],
            "ceo_phone": body["ceo_phone"],
            "ceo_mobile": body["ceo_mobile"],
            "cco_name": body["cco_name"],
            "cco_phone": body["cco_phone"],
            "cco_mobile": body["cco_mobile"],
            "address": body["address"],
            "email": body["email"],
            "logo": body["logo"]
        }
        # Create new user with new password
        new_client = Client.objects.get_or_create(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        new_client.set_password(data['password1'])
        if data['position'] == 'superuser':
            new_client.is_superuser = True
            new_client.is_staff = True
        new_client.save()
        response = {}
        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


