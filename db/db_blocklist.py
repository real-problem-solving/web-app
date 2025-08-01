"""
# db_blocklist.py
This module contains the blocklist for JWT tokens.
It is used to keep track of revoked tokens.
It will be imported by app/app.py and resources/user.py so tokens can added
to the blocklist when the user logouts.
"""

BLOCKLIST = set()