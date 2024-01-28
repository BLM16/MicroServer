from models.user import User
import uuid

users: dict[str, User] = {}
sessions: dict[str, User] = {}

def new_guid():
    return str(uuid.uuid4())

def get_user_from_session_cookie(morsel) -> User | None:
    if morsel is None:
        return None
    return sessions.get(morsel.value)
