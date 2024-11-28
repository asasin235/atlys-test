from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends

security = HTTPBearer()

def authenticate(token: HTTPAuthorizationCredentials = Depends(security)):
    if token.credentials != "static_token":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return True