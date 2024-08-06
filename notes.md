# Notes about lecture 4 in genral


1. Django models are a level of abstraction over SQL 

2. To make the models show up on the admin page import them then add the following line to `admin.py`

    ```python
    admin.site.register(ClassName)
    ```

this is how you are checking if an element is already included 

```python
        if user.watchlist.filter(id=listing_id).exists():
```

TODO LIST
3. Present user with error message if the bid is not big enough []
4. Check the Django admin app works with this website []
5. Make the categories thing [] (you will have to use the filter through categories option to make this work note that you want the category to be selectable through a dropdown menu not a  text input)


Step By step guide to how I am writing Category migration

1. Creating empty migration 

`python manage.py makemigrations yourapp --empty`



THIS IS AN EXAMPLE OF A RUNNABOE SCRIPT I MADE INSIDE AUCTIONS called script .py 

```python
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

```

that I run using:

```BASH
poetry run python -m auctions.script
```

I don't like the way this is done at all I think categories shoudl maybe be its own module 