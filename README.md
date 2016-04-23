# IMPORTANT
Pinterest have updated their site and it now requires the browser to support JavaScript for some functions. This has
unfortunately made things like pinning, creation of boards etc to stop working with this client. Search is still OK.
I'm not sure if/when I will do something about it. Leaving this repo as is if anyone wants to learn something from it.

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

# TESTS

```bash
python -m unittest discover tests
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

More tests...