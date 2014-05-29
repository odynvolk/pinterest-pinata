pinterest-pinata
================
A Python client for Pinterest. There's at this point in time no API for Pinterest that one can use, so this client
consist of somewhat clumsy code.

Supports the following operations: login, pin, repin, boards, like, comment, search, follow board, create board

# Usage

## bash

```bash
python pinterest_pinata.py youremail yourpassword yourusername
```

## python

```python
pinata = PinterestPinata(email='youremail', password='yourpassword', username='yourusername')
pinata.create_board(name='my test board', category='food_drink', description='my first board')
```


# TODO

We need some tests...