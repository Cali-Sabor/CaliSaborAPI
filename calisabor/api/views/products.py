from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name="dispatch")
class NewProduct(APIView):
    """

    """
    pass
