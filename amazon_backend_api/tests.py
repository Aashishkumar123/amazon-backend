from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestRegistration(APITestCase):
    '''
    This will handle Registration Test Case
    '''

    def test_registration(self):
        '''
        This will test registration
        if registeration failed then, testcase will failed....
        otherwise it will pass the testcase....
        '''
        data = {
            "full_name" : "Aashish Kumar",
            'email' : "wek@gmail.com",
            'password' : "aakumar123"
        }
        response = self.client.post(
                reverse('amz-user-register'), data = data
                )
        self.assertEqual(
                response.status_code,
                    status.HTTP_201_CREATED, 
                        msg='test_registration'
                    )
