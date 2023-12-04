from django.test import TestCase
from LittlelemonAPI.models import Category, Booking

# Create your tests here.
class CategoryTest(TestCase):
    def test_get_item(self):
        item = Category.objects.create(slug="italian", title="Italian")
        self.assertEqual(str(item), "Italian")

class BookingTest(TestCase):
    def test_get_item(self):
        item = Booking.objects.create(first_name="savindu", reservation_date="2023-12-05", reservation_slot=5)
        self.assertEqual(str(item), "savindu")