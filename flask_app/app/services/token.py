from itsdangerous import URLSafeTimedSerializer
from config import Config


class TokenService:
    @staticmethod
    def generate_token(email):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(
                token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration
            )
            return email
        except Exception:
            return False
