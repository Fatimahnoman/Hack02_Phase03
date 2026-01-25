from passlib.context import CryptContext

# Test bcrypt functionality
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    # Test with a short password
    password = "shortpass123"
    hashed = pwd_context.hash(password)
    print(f"Hashing successful: {hashed[:20]}...")

    # Verify the password
    verified = pwd_context.verify(password, hashed)
    print(f"Verification successful: {verified}")

except Exception as e:
    print(f"Bcrypt error: {e}")