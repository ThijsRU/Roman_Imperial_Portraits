"""
Adaptations of the database that are called up from the (list)views in the RIPD app.
"""

from django.db import transaction
import re

# ======= imports from my own application ======
from basic.utils import ErrHandle #?

# from ripd.models import #?


