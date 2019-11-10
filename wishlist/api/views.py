from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

import requests

from api.api_permissions import OnlyAdminCanCreate
from api.models import Client, Wishlist
from api.serializers import (
    ClientSerializer,
    WishlistSerializerOutput,
    WishlistSerializerInput
)


URL_API_PRODUTOS='http://challenge-api.luizalabs.com/api/product/'


class ClientList(APIView):
    """
        Lista todos os clientes ou cria um novo cliente.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanCreate]
    
    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetail(APIView):
    """
        Recupera, atualiza ou deleta um cliente.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanCreate]
    
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientWishlist(APIView):
    """
        Recupera lista de produtos favoritos.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanCreate]

    def get(self, request, pk, format=None):
        try:
            wishlist = Wishlist.objects.filter(client_id=pk)
        except Wishlist.DoesNotExist:
            raise Http404

        wishlist_detail = []

        for item in wishlist:
            response = []
            response = requests.get(URL_API_PRODUTOS + item.product_id)            
            if response.status_code >= 200 and response.status_code < 400:
                product_detail = response.json()
                wishlist_detail.append({
                    'id': product_detail['id'],
                    'title': product_detail['title'],
                    'price': product_detail['price'],
                    'image': product_detail['image'],
                    'brand': product_detail['brand'],
                })

        serializer = WishlistSerializerOutput(wishlist_detail, many=True)
        return Response(serializer.data)


class WishlistList(APIView):
    """
        Cria um novo produto na lista de favoritos.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanCreate]

    def post(self, request, format=None):
        response = requests.get(URL_API_PRODUTOS + request.data['product_id'])
        if response.status_code >= 200 and response.status_code < 400:
            product = response.json()
            if product['id'] == request.data['product_id']:
                serializer = WishlistSerializerInput(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Produto não existe.', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Produto não existe.', status=status.HTTP_400_BAD_REQUEST)


class WishlistDetail(APIView):
    """
        Deleta um produto da lista de favoritos.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanCreate]

    def delete(self, request, string, pk, format=None):
        wishlist = Wishlist.objects.filter(product_id=string, client_id=pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
