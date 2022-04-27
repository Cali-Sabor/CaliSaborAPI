import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Attendant, Client


def request_data(body):
    return {
            "client": body.get("client"),
            "first_name": body.get("first_name"),
            "last_name": body.get("last_name"),
            "mobile": body.get("mobile"),
            "note": body.get("note", "Sin comentarios")
        }


def check_if_new_client(attendant, data):
    if data['client'] == attendant.client.client_name:
        return attendant.client
    else:
        return Client.objects.get(client_name=data['client'])


@method_decorator(csrf_exempt, name="dispatch")
class NewAttendant(APIView):
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
        # Create new attendant
        client = Client.objects.get(
            client_name=data['client']
        )
        new_attendant = Attendant.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        print(new_attendant)
        if new_attendant[1]:
            new_attendant[0].client = client
            new_attendant[0].mobile = data.get("mobile")
            new_attendant[0].note = data.get("note")
            new_attendant[0].save()
            status = codes.HTTP_200_OK
            response = {
                "id": f"{new_attendant[0].id}",
                "full name": f"{new_attendant[0].first_name} {new_attendant[0].last_name}",
                "client": f"{client}",
                "message": f"Attendant created successfully"
            }
        else:
            status = codes.HTTP_400_BAD_REQUEST
            response = {
                "id": f"{new_attendant[0].id}",
                "full name": f"{new_attendant[0].first_name} {new_attendant[0].last_name}",
                "client": f"{client}",
                "message": f"Attendant already exists"
            }

        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class EditAttendant(APIView):
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
        try:
            attendant = Attendant.objects.get(
                first_name=data['first_name'],
                last_name=data['first_name']
            )
            attendant.client = check_if_new_client(attendant, data)
            attendant.first_name = data.get("first_name")
            attendant.last_name = data.get("last_name")
            attendant.mobile = data.get("mobile")
            attendant.note = data.get("note")
            attendant.save()
            status = codes.HTTP_200_OK
            response = {"message": f"Attendant {attendant.first_name} {attendant.last_name} edited successfully"}
        except Attendant.DoesNotExist:
            status = codes.HTTP_404_NOT_FOUND
            response = {"message": f"The attendant doesn't exists"}

        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteAttendant(APIView):
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
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        try:
            attendant = Attendant.objects.get(
                first_name=first_name,
                last_name=last_name
            )
            attendant.delete()
            status = codes.HTTP_200_OK
            response = {"message": f"Attendant {first_name} {last_name} deleted successfully"}
        except Attendant.DoesNotExist:
            status = codes.HTTP_404_NOT_FOUND
            response = {"message": f"The attendant referred doesn't exists"}

        return HttpResponse(json.dumps(response), "application/json", status=status)
