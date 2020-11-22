
# safe_str_cmp : better for comparing differnt kinds of strings and encodings
from werkzeug.security import safe_str_cmp
from user import User  # syntax from <file> import <class>
from typing import Union  # for potential multiple types


# return a User or None
def authenticate(username: str, password: str) -> Union[User, None]:
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


#  unique to Flask JWT - passes in JWT and extracts user_id
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
