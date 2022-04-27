import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Products, Client


def request_data(body):
    """
        Utility for recreate the body in a dict
    """
    return {
        "client": body.get("client"),
        "name": body.get("name"),
        "code": body.get("code"),
        "size": body.get("size"),
        "measure": body.get("measure", "Pendiente"),
        "picture": body.get("picture", "Pendiente"),
        "pricing": body.get("pricing", "Pendiente")
    }


@method_decorator(csrf_exempt, name="dispatch")
class NewProduct(APIView):
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
        # Get client
        try:
            client = Client.objects.get(
                nit=data["client"]
            )
        except Client.DoesNotExist:
            status = codes.HTTP_400_BAD_REQUEST
            response = {"message": f"Client {data['client']} doesn't exist, please check"}
            return HttpResponse(json.dumps(response), "application/json", status=status)
        # Create new product
        new_product = Products.objects.get_or_create(
            name=data['name']
        )
        if new_product[1]:
            new_product[0].client = client
            new_product[0].code = data.get("code")
            new_product[0].size = data.get("size")
            new_product[0].measure = data.get("measure")
            new_product[0].picture = data.get("picture")
            new_product[0].pricing = data.get("pricing")
            new_product[0].save()
            status = codes.HTTP_200_OK
            response = {"message": f"Product {new_product[0].name} created successfully"}
        else:
            status = codes.HTTP_208_ALREADY_REPORTED
            response = {"message": f"Product {new_product[0].name} (Code: {new_product[0].code}) already exists"}

        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class EditProduct(APIView):
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
        try:
            product = Products.objects.get(
                code=data['code']
            )
            product.code = data.get("code")
            product.size = data.get("size")
            product.measure = data.get("measure")
            product.picture = data.get("picture")
            product.pricing = data.get("pricing")
            product.save()
            response["message"] = f"Product {product.name} updated successfully"
        except Products.DoesNotExist:
            response["message"] = f"The product doesn't exists"

        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteProduct(APIView):
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
            "code": body.get("code")
        }

        try:
            product = Products.objects.get(
                code=data['code']
            )
            print(product)
            name = product.name
            code = product.code
            product.delete()
            response = {"message": f"Product {code}:{name} deleted successfully"}
        except Products.DoesNotExist:
            response = {"message": f"Product doesn't exists"}
        # Create Profile
        status = codes.HTTP_200_OK
        return HttpResponse(json.dumps(response), "application/json", status=status)
