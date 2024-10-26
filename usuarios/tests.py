import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from .models import Viaje
from django.test import TestCase

# Import necessary modules

# Setup the test class
class TestRegistrarViaje(TestCase):
    def setup_method(self):
        # Create a test client
        self.client = Client()
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            nombre='Test User',
            email='testuser@example.com',
            carrera='Engineering',
            sede='Main Campus'
        )
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

    def test_registrar_viaje_success(self):
        # Simulate a POST request with valid data
        response = self.client.post(reverse('RegistrarViaje'), {
            'origen': 'Estacionamiento A',
            'destino': 'Edificio B',
            'hora': '08:00',
            'patente': 'ABC1234',
            'cupos': 4,
            'conductor_id': self.user.id
        })
        # Check the response
        assert response.status_code == 302  # Redirect status
        # Verify the Viaje object is created
        assert Viaje.objects.filter(conductor=self.user).exists()

    def test_registrar_viaje_missing_conductor_id(self):
        # Simulate a POST request without conductor ID
        response = self.client.post(reverse('RegistrarViaje'), {
            'origen': 'Estacionamiento A',
            'destino': 'Edificio B',
            'hora': '08:00',
            'patente': 'ABC1234',
            'cupos': 4
        })
        # Check the response
        assert response.status_code == 400  # Bad request status