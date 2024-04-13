# Notes about lecture 4 in genral


1. Django models are a level of abstraction over SQL 
2. To make the models show up on the admin page import them then add the followinr line to `admin.py`
    ```python
    admin.site.register(ClassName)
    ```

this is how you are checking if an element is already included 
```python
        if user.watchlist.filter(id=listing_id).exists():
```