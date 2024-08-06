import django
import os

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commerce.settings')
django.setup()

# Now you can import Django models
from auctions.models import Listing

print("Printing Lisings: \n")
print(Listing.objects.all())


current = Listing.objects.values_list('category', flat=True).distinct()
print("categories")
print(list(current))
