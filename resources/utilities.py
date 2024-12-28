from werkzeug.security import generate_password_hash,check_password_hash


# Example function for hashing a password
def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Hash a user's password before saving
hashed_password = hash_password("test")
print(hashed_password)


# Example function for verifying a password
def verify_password(stored_hash, input_password):
    return check_password_hash(stored_hash, input_password)

stored_hash = "pbkdf2:sha256:1000000$o6kteqWbjVqLiSRO$70f0859b4f511f99e6dc6ffe7500dab9b6a4a334c1ab859056f8367d5e9bf7dd"
input_password = "test"
if verify_password(stored_hash, input_password):
    print("Password is correct!")
else:
    print("Invalid password!")