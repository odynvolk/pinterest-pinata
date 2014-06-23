pinterest-pinata
================
A Python client for Pinterest. There's at this point in time no API for Pinterest that one can use, so this client
consist of somewhat clumsy code.

Supports the following operations: login, pin, repin, boards, like, comment, search_pins, follow board, create board, 
follow user, search users, search boards.

# INSTALL

If you have downloaded the source code:

```bash
python setup.py install
```

Pip

```bash
pip install pinterest-pinata
```


# USAGE

## bash

``` bash
python pinterest_pinata.py youremail yourpassword yourusername
```

## python

``` python
from pinata.client import PinterestPinata

pinata = PinterestPinata(email='youremail', password='yourpassword', username='yourusername')
pinata.create_board(name='my test board', category='food_drink', description='my first board')
```

# TODO

We need some tests...