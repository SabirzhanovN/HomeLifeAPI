from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .service import Cart
from .serializers import CartSerializer


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    def get(self, request):
        cart = Cart(request)

        return Response({
                "cart": list(cart.__iter__()),
                "cart_total_price": cart.get_total_price()
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        if "clear" not in request.data:
            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()
        else:
            product = request.data
            try:
                cart.add(
                    product=product["product"],
                    quantity=product["quantity"],
                    override_quantity=product["override_quantity"] if "override_quantity" in product else False
                )
            except ValueError:
                return Response({"error": "Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            except IndexError as e:
                return Response({"error": "Field 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
            except KeyError as e:
                return Response({"error": f"Field {e} is required"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)

#{"product": {"id":12}, "quantity": 2}