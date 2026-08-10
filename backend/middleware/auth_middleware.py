import hashlib
from datetime import datetime

from models.session_model import get_session_by_token_hash

def authenticate_token(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    session = get_session_by_token_hash(token_hash)

    if session is None:
        return None

    expires_at = datetime.fromisoformat(session["expires_at"])
    if expires_at <= datetime.now():
        return None
    
    return session["user_id"]
