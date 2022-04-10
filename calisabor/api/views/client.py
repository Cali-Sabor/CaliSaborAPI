import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Client


def request_data(body):
    return {
            "client_name": body.get("client_name"),
            "nit": body.get("nit"),
            "ceo_name": body.get("ceo_name"),
            "ceo_phone": body.get("ceo_phone", "Pendiente"),
            "ceo_mobile": body.get("ceo_mobile"),
            "cco_name": body.get("cco_name"),
            "cco_phone": body.get("cco_phone", "Pendiente"),
            "cco_mobile": body.get("cco_mobile"),
            "address": body.get("address", "Pendiente"),
            "email": body.get("email"),
            "logo": body.get("logo", "Pendiente")
        }


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
        response = {}
        body = request.data
        data = request_data(body)
        # Create new user with new password
        new_client = Client.objects.get_or_create(
            client_name=data['client_name']
        )
        print(new_client)
        if new_client[1]:
            new_client[0].nit = data.get("nit")
            new_client[0].ceo_name = data.get("ceo_name")
            new_client[0].ceo_phone = data.get("ceo_phone")
            new_client[0].ceo_mobile = data.get("ceo_mobile")
            new_client[0].cco_name = data.get("cco_name")
            new_client[0].cco_phone = data.get("cco_phone")
            new_client[0].cco_mobile = data.get("cco_mobile")
            new_client[0].address = data.get("address")
            new_client[0].logo = data.get("logo")
            new_client[0].save()
            response = {"message": f"Client {new_client[0].client_name} created successfully"}
        else:
            response = {"message": f"The client {new_client[0].client_name} (Nit: {new_client[0].nit}) already exists"}

        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class EditClient(APIView):
    """
        Documentation
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
        response = {}
        body = request.data
        data = request_data(body)
        try:  # Create new user with new password
            client = Client.objects.get(
                nit=data['nit']
            )
            client.nit = data.get("nit")
            client.ceo_name = data.get("ceo_name")
            client.ceo_phone = data.get("ceo_phone")
            client.ceo_mobile = data.get("ceo_mobile")
            client.cco_name = data.get("cco_name")
            client.cco_phone = data.get("cco_phone")
            client.cco_mobile = data.get("cco_mobile")
            client.address = data.get("address")
            client.logo = data.get("logo")
            client.save()
            response = {"message": f"Client {client.client_name} edited successfully"}
        except Client.DoesNotExist:
            response = {"message": f"The client doesn't exists"}

        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteClient(APIView):
    """
        Documentation
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
        response = {}
        body = request.data
        nit = body.get("nit")
        print(f"Nit: {nit}")
        try:
            client = Client.objects.get(
                nit=nit
            )
            print(client)
            name = client.client_name
            client.delete()
            response = {"message": f"Client {name} deleted successfully"}
        except Client.DoesNotExist:
            response = {"message": f"The client doesn't exists"}

        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)
