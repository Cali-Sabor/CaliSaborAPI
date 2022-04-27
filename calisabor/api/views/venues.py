import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..utilities.exceptions import ClientException, AttendantException

from ..models import Venues, Client, Attendant


def request_data(body):
    return {
            "client": body.get("client"),
            "name": body.get("name"),
            "code": body.get("code"),
            "address": body.get("address"),
            "phone": body.get("phone"),
            "mobile": body.get("mobile"),
            "attendant": body.get("attendant"),
            "products": body.get("products")
        }


def get_external_data(new_venue, data):
    try:
        client = Client.objects.get(
            client_name=data['client']
        )
    except Client.DoesNotExist:
        msg = f"The client {data['client']} does not exist. Please check or contact with database service"
        raise ClientException(msg)
    try:
        attendant = Attendant.objects.get(
            id=data['attendant']
        )
    except Attendant.DoesNotExist:
        msg = f"The attendant {data['attendant']} does not exist. Please check or contact with database service"
        raise AttendantException(msg)
    return client, attendant


@method_decorator(csrf_exempt, name="dispatch")
class NewVenue(APIView):
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
        data = request_data(body)

        new_venue = Venues.objects.get_or_create(
            name=data['name'],
            code=data['code']
        )
        print(new_venue)
        try:
            client, attendant = get_external_data(new_venue, data)
            if new_venue[1]:
                new_venue[0].client = client
                new_venue[0].name = data.get("name")
                new_venue[0].code = data.get("code")
                new_venue[0].products = data.get("products")
                new_venue[0].phone = data.get("phone")
                new_venue[0].mobile = data.get("mobile")
                new_venue[0].attendant = attendant
                new_venue[0].products = data.get("products")
                new_venue[0].save()
                response = {
                    "id": f"{new_venue[0].id}",
                    "full name": f"{new_venue[0].name}",
                    "client": f"{client}",
                    "message": f"Venue created successfully"
                }
            else:
                response = {
                    "id": f"{new_venue[0].id}",
                    "full name": f"{new_venue[0].name}",
                    "client": f"{client}",
                    "message": f"Venue already successfully"
                }
        except ClientException as e:
            response = {"error": str(e)}
        except AttendantException:
            response = {0}
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
        body = request.data
        data = request_data(body)
        try:  # Create new user with new password
            client = Client.objects.get(
                name=data['name']
            )
            client.name = data.get("name")
            client.code = data.get("code")
            client.products = data.get("products")
            client.phone = data.get("phone")
            client.mobile = data.get("mobile")
            client.attendant = data.get("attendant")
            client.cco_mobile = data.get("cco_mobile")
            client.products = data.get("products")
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
        body = request.data
        name = body.get("name")
        print(f"name: {name}")
        try:
            client = Client.objects.get(
                name=name
            )
            print(client)
            name = client.client_name
            client.delete()
            response = {"message": f"Client {name} deleted successfully"}
        except Client.DoesNotExist:
            response = {"message": f"The client doesn't exists"}

        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)
