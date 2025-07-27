import json
import os

# Attempt was made to use https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#oauth2passwordrequestform
# ...but it was too complex


# Password is hashed on the client side
class AuthService:
    def __init__(self, users_file="server/api/users.json"):
        self.users_file = users_file
        self._initialize_db()
        print("AuthService initialized at", self.users_file)

    def _initialize_db(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)

    def _read_users(self):
        with open(self.users_file, "r") as f:
            return json.load(f)

    def _write_users(self, users):
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def create_user(self, username, password):
        users = self._read_users()
        if username in users:
            return {"success": False, "reason": "User already exists"}
        users[username] = password
        self._write_users(users)
        return {"success": True, "username": username}

    def authenticate_user(self, username, password):
        users = self._read_users()
        if username not in users:
            return {"success": False, "reason": "User not found"}
        if users[username] != password:
            return {"success": False, "reason": "Incorrect password"}
        return {"success": True, "username": username}


if __name__ == "__main__":
    auth_service = AuthService()
    print(auth_service.create_user("testuser", "testpassword"))
    print(auth_service.authenticate_user("testuser", "testpassword"))
    print(auth_service.authenticate_user("testuser2", "testpassword"))  # Does not exist
