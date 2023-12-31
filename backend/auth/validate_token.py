from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError

# Initialize Firebase Admin SDK
cred = credentials.Certificate("backend/config/salafifatawa-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Initialize FastAPI app
app = FastAPI()

# Create HTTPBearer instance for handling Authorization header
security = HTTPBearer()


# Create a dependency for checking Firebase authentication
def validate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        user = auth.get_user(decoded_token['uid'])
        return user
    except ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired authentication token")
    except InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")