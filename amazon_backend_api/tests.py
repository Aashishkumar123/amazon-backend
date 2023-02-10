from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from amazon_backend_api.models import Amazonuser
from django.contrib.auth.hashers import make_password


class TestRegistration(APITestCase):
    """
    This will handle Registration Test Case
    """

    def setUp(self):
        self.url = reverse("amz-user-register")

    def test_registration(self):
        """
        This will test registration
        """

        data = {
            "full_name": "Aashish Kumar",
            "email": "wek@gmail.com",
            "password": "bwfjjwje",
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg="test_registration"
        )

    def test_without_data_registration(self):
        """
        This will test registration without data
        """

        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_without_data_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("full_name")[0],
            "This field is required.",
            msg="test_without_fullname_registration_data_fullname",
        )
        self.assertEqual(
            response.data.get("data").get("email")[0],
            "This field is required.",
            msg="test_without_fullname_registration_data_email",
        )
        self.assertEqual(
            response.data.get("data").get("password")[0],
            "This field is required.",
            msg="test_without_fullname_registration_data_password",
        )

    def test_without_fullname_registration(self):
        """
        This will test registration without fullname
        """

        data = {"email": "wek@gmail.com", "password": "bwfjjwje"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_without_fullname_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("full_name")[0],
            "This field is required.",
            msg="test_without_fullname_registration_data",
        )

    def test_without_email_registration(self):
        """
        This will test registration without email
        """

        data = {"full_name": "Aashish Kumar", "password": "bwfjjwje"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_without_email_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("email")[0],
            "This field is required.",
            msg="test_without_email_registration_data",
        )

    def test_without_password_registration(self):
        """
        This will test registration without password
        """

        data = {
            "full_name": "Aashish Kumar",
            "email": "wek@gmail.com",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_without_password_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("password")[0],
            "This field is required.",
            msg="test_without_password_registration_data",
        )

    def test_invalid_email_registration(self):
        """
        This will test invalid email address for registration...
        """

        data = {
            "full_name": "Aashish Kumar",
            "email": "wek@gmail.",
            "password": "bwfjjwje",
        }

        response = self.client.post(self.url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_invalid_email_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("email")[0],
            "Enter a valid email address.",
            msg="test_invalid_emai_registration_data",
        )

    def test_exists_email_registration(self):
        """
        This will test exist email address for registration...
        """

        data = {
            "full_name": "Aashish Kumar",
            "email": "whghg@gmail.com",
            "password": "bwfjjwje",
        }

        Amazonuser.objects.create(
            full_name=data.get("full_name"),
            email=data.get("email"),
            password=data.get("password"),
        )
        response = self.client.post(self.url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_exists_email_registration_statuscode",
        )
        self.assertEqual(
            response.data.get("data").get("email")[0],
            "user with this email address already exists.",
            msg="test_exists_email_registration_data",
        )


class TestLogin(APITestCase):
    """
    This will handle login testcases
    """

    def setUp(self):
        self.url = reverse("amz-user-sign-in")

    def test_login(self):
        """
        This will test successfull login
        """
        data = {
            "full_name": "Aashish Kumar",
            "email": "whghg@gmail.com",
            "password": "bwfjjwje",
        }

        Amazonuser.objects.create(
            full_name=data.get("full_name"),
            email=data.get("email"),
            password=make_password(data.get("password")),
        )

        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="test_login_successfull_statuscode",
        )

    def test_login_without_data(self):
        """
        This will test login without data from client
        """

        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_login_without_data_statuscode",
        )

        self.assertEqual(
            response.data.get("data").get("email")[0],
            "This field is required.",
            msg="test_login_without_data_DATA_email",
        )

        self.assertEqual(
            response.data.get("data").get("password")[0],
            "This field is required.",
            msg="test_login_without_data_DATA_password",
        )

    def test_login_with_invalid_credentials(self):
        """
        This will test login with invalid credentials
        """

        """wrong credentials"""
        data = {"email": "whghg@gmail.com", "password": "bwfjjwje"}

        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg="test_login_with_invalid_credentials_statuscode",
        )
        self.assertEqual(
            response.data.get("message"),
            "Invalid Email or Password",
            msg="test_login_with_invalid_credentials_message",
        )

    def test_login_with_empty_data(self):
        """
        This will test login with empty data from client
        """

        """empty data"""
        data = {"email": "", "password": ""}

        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="test_login_with_empty_data_statuscode",
        )

        self.assertEqual(
            response.data.get("data").get("email")[0],
            "This field may not be blank.",
            msg="test_login_with_empty_data_DATA_email",
        )

        self.assertEqual(
            response.data.get("data").get("password")[0],
            "This field may not be blank.",
            msg="test_login_with_empty_data_DATA_password",
        )
