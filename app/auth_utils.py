import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
from decouple import config

JWT_KEY = config('JWT_KEY')

class AuthJwtCsrf():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_KEY

    def generate_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
    
    def encode_jwt(self, email) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "sub": email,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    def decoded_jwt(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="The JWT has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    def verify_jwt(self, request) -> bool:
        token = request.cookies.get("access_token")
        # print(token)
        if not token:
            raise HTTPException(status_code=401, detail="No JWT exist: may not set yet or deleted")
        _, _, value = token.partition(" ")
        subject = self.decoded_jwt(value)
        return subject
    
    def verify_update_jwt(self, request):
        subject = self.verify_jwt(request)
        new_token = self.encode_jwt(subject)
        return new_token, subject
    
    def verify_csrf_update_jwt(self, request, csrf_protect, headers) -> str:
        csrf_token = csrf_protect.get_csrf_from_headers(headers)
        csrf_protect.validate_csrf(csrf_token)
        subject = self.verify_jwt(request)
        new_token = self.encode_jwt(subject)
        return new_token