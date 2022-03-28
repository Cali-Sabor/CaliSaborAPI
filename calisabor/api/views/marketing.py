from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name="dispatch")
class NewSell(APIView):
    """

    """
    pass

# Mercadeo necesitaria
#
# la tabla de mercadeo y su llenado con los datos que se requieran