from rest_framework import status
from django.test import TestCase


class ViewTest(TestCase):

    def test_GET_company_2(self):
        response = self.client.get('/schedule/2022/FALL/2', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_GET_company_1(self):
        response = self.client.get('/schedule/2022/FALL/1', format='json')
        self.assertIsNotNone(response)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
