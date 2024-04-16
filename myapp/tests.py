from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Friendship
from rest_framework.test import APITestCase
from rest_framework import status
from .models import MyUser
from django.urls import reverse


class TestURLs(APITestCase):
    def setUp(self):
        self.user1 = MyUser.objects.create_user(
            email="user121@example.com", password="password"
        )
        self.user2 = MyUser.objects.create_user(
            email="user222@example.com", password="password"
        )
        self.client.force_authenticate(user=self.user1)

    def test_friend_list_url(self):
        url = reverse("search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_search_url(self):
        url = reverse("search")
        data = {"search": "user"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pending_requests_url(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse("search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


##############################################################################################################


class TestFriendRequest(APITestCase):
    def setUp(self):
        self.user1 = MyUser.objects.create_user(
            email="user1@example.com", password="password"
        )
        self.user2 = MyUser.objects.create_user(
            email="user2@example.com", password="password"
        )
        self.client.force_authenticate(user=self.user1)

    def test_send_friend_request(self):
        url = reverse("friend-request")
        data = {"to_user": self.user2.id}  # Corrected field to user id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Friendship.objects.filter(from_user=self.user1, to_user=self.user2).exists()
        )

    def test_send_friend_request_to_self(self):
        url = reverse("friend-request")
        data = {"to_user": self.user1.id}  # Corrected field to user id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Friendship.objects.filter(from_user=self.user1, to_user=self.user1).exists()
        )

    def test_send_duplicate_friend_request(self):
        Friendship.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse("friend-request")
        data = {"to_user": self.user2.id}  # Corrected field to user id
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Friendship.objects.filter(from_user=self.user1, to_user=self.user2).count(),
            1,
        )
