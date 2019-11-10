from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from api.models import Client, Wishlist


class ClientTest(TestCase):
    """
        Módulo de teste da model Client.
    """
    def setUp(self):
        Client.objects.create(name="Jorge", email="jorge@jorge.com")
        Client.objects.create(name="Pedro", email="pedro@pedro.com")

    def test_client_name(self):
        client = Client.objects.get(name="Jorge")
        self.assertEqual(client.email, "jorge@jorge.com")

    def test_client_email(self):
        client = Client.objects.get(email="pedro@pedro.com")
        self.assertEqual(client.name, "Pedro")


class WishlistTest(TestCase):
    """
        Módulo de teste da model Wishlist.
    """
    def setUp(self):
        Client.objects.create(name="Jorge", email="jorge@jorge.com")
        Client.objects.create(name="Pedro", email="pedro@pedro.com")
        Wishlist.objects.create(client_id=1, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")
        Wishlist.objects.create(client_id=1, product_id="958ec015-cfcf-258d-c6df-1721de0ab6ea")
        Wishlist.objects.create(client_id=2, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")

    def test_wishlist_product(self):
        wishlist = Wishlist.objects.get(client_id=1, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")
        self.assertEqual(wishlist.product_id, "1bf0f365-fbdd-4e21-9786-da459d78dd1f")


class TestAuthentication(APITestCase):
    """
        Módulo de teste da autenticação por token.
    """
    def setUp(self):
        self.user = User.objects.create(username="maria", email="maria@teste.com")
        self.user.set_password("123456")

        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_token_authentification(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/clients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestClientRequest(APITestCase):
    """
        Módulo de teste dos endpoints do Cliente.
    """
    def setUp(self):
        self.user = User.objects.create(username="maria", email="maria@teste.com")
        self.user.set_password("123456")

        self.token = Token.objects.create(user=self.user)
        self.token.save()
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        Client.objects.create(name="Jorge", email="jorge@jorge.com")
        Client.objects.create(name="Pedro", email="pedro@pedro.com")

    def test_client_get_all(self):
        response = self.client.get("/api/clients/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_get_by_pk(self):
        client_test = Client.objects.get(pk=1)
        response = self.client.get("/api/clients/" + str(client_test.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_create(self):
        response = self.client.post("/api/clients/", {
            "name": "Junior",
            "email": "junior@junior.com"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_create_email_duplicate(self):
        response = self.client.post("/api/clients/", {
            "name": "Jorge",
            "email": "jorge@jorge.com"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_updated(self):
        client_test = Client.objects.get(pk=1)
        response = self.client.put("/api/clients/" + str(client_test.id) + "/", {
            "name": "Jorge Amado",
            "email": "jorge@jorge.com"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_deleted(self):
        client_test = Client.objects.get(pk=1)
        response = self.client.delete("/api/clients/" + str(client_test.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_client_get_wishlist(self):
        client_test = Client.objects.get(pk=1)
        response = self.client.get("/api/clients/" + str(client_test.id) + "/wishlist/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestWishlistRequest(APITestCase):
    """
        Módulo de teste dos endpoints da Lista de Favoritos.
    """
    def setUp(self):
        self.user = User.objects.create(username="maria", email="maria@teste.com")
        self.user.set_password("123456")

        self.token = Token.objects.create(user=self.user)
        self.token.save()
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        Client.objects.create(name="Jorge", email="jorge@jorge.com")
        Client.objects.create(name="Pedro", email="pedro@pedro.com")
        Wishlist.objects.create(client_id=1, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")
        Wishlist.objects.create(client_id=1, product_id="958ec015-cfcf-258d-c6df-1721de0ab6ea")
        Wishlist.objects.create(client_id=2, product_id="1bf0f365-fbdd-4e21-9786-da459d78dd1f")

    def test_wishlist_add_product(self):
        response = self.client.post("/api/wishlist/", {
            "client": 1,
            "product_id": "6a512e6c-6627-d286-5d18-583558359ab6"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wishlist_add_product_duplicate(self):
        response = self.client.post("/api/wishlist/", {
            "client": 1,
            "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wishlist_delete_product(self):
        client_test = Client.objects.get(pk=1)
        response = self.client.delete("/api/wishlist/1bf0f365-fbdd-4e21-9786-da459d78dd1f/" + str(client_test.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
