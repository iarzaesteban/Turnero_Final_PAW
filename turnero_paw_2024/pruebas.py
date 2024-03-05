import hashlib

password = "12345"
print(hashlib.sha256(password.encode()).hexdigest())