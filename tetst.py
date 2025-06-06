from datetime import date

from src.database.repositories.user_repository import UserRepository

user = UserRepository.get_user_preference('default')
print(user)