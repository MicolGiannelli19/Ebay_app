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