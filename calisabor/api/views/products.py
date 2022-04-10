import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status as codes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..models import Products


def request_data(body):
    return {
        "name": body.get("name"),
        "code": body.get("code"),
        "size": body.get("size"),
        "measure": body.get("measure"),
        "picture": body.get("picture"),
        "pricing": body.get("pricing")
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
        # Create new user with new password
        new_product = Products.objects.get_or_create(
            name=data['name']
        )
        print(new_product)
        if new_product[1]:
            new_product[0].code = data.get("code")
            new_product[0].size = data.get("size")
            new_product[0].measure = data.get("measure")
            new_product[0].picture = data.get("picture")
            new_product[0].pricing = data.get("pricing")
            new_product[0].save()
            response = {"message": f"Product {new_product[0].name} created successfully"}
        else:
            response = {"message": f"Product {new_product[0].name} (Code: {new_product[0].code}) already exists"}

        # Create Profile
        status = codes.HTTP_200_OK
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
            response["message"] = f"Product {product.name} created successfully"
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
