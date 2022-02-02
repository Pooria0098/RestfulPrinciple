from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from contacts.views import ContactViewSet


class TestContact(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.user = self.setup_user()
        self.view = ContactViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = self.refresh_token.access_token

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test@123'
        )

    def test_contact_list(self):
        request = self.factory.get('/ContactService/', HTTP_AUTHORIZATION='Bearer  {}'.format(self.access_token))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_contact_get(self):
        request = self.factory.get('/ContactService/', HTTP_AUTHORIZATION='Bearer  {}'.format(self.access_token))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_contact_create(self):
        self.client.login(username="test", password="test@123")
        data = {
            'first_name': 'pooria',
            'last_name': 'tavana',
            'email': 'tavanapooria9731@gmail.com',
            'group': 1,
            'phone_number': '09029191775',
            'address': 'No.13, Eftekhar St, Larestan Ave, first of Motahari',
        }
        response = self.client.post(path='/ContactService/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
