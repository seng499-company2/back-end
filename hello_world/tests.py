from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import World
from .serializers import WorldSerializer

# tests for views

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_world(name="", population=0):
        if name != "" and population != 0:
            World.objects.create(name=name, population=population)

    def setUp(self):
        # add test data
        self.create_world("Mars", 1)
        self.create_world("Earth", 5)
        self.create_world("Neptune", 23)

class GetAllWorldsTest(BaseViewTest):

    def test_get_all_world(self):
        """
        This test ensures that all worlds added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("worlds", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = World.objects.all()
        serialized = WorldSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)