import asyncio
from faker import Faker
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import sessionmanager
from src.database.models import User, Contact
from src.services.auth import Hash

fake = Faker()


def generate_valid_phone():
    while True:
        phone = fake.phone_number()
        clean_phone = ''.join(c for c in phone if c.isdigit() or c in '+- ')
        if len(clean_phone) <= 15:
            return clean_phone


async def seed_db(user_count: int = 3, contacts_per_user: int = 10):
    async with sessionmanager.session() as session:
        result = await session.execute(select(func.count()).select_from(User))
        total_users = result.scalar_one()

        if total_users > 0:
            print("Users already exist. Skipping seeding.")
            return

        hash_service = Hash()  # <- Створюємо екземпляр класу

        for _ in range(user_count):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = hash_service.get_password_hash(
                "testpassword")  # <- Виклик через екземпляр
            user = User(
                username=username,
                email=email,
                hashed_password=password,
                avatar=fake.image_url(),
            )
            session.add(user)
            await session.flush()

            for _ in range(contacts_per_user):
                contact = Contact(
                    name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    phone=generate_valid_phone(),
                    birthday=fake.date_of_birth(
                        minimum_age=18, maximum_age=90),
                    additional_info=fake.sentence(nb_words=6),
                    user_id=user.id
                )
                session.add(contact)

        await session.commit()
        print(
            f"Seeded {user_count} users × {contacts_per_user} contacts each.")

if __name__ == "__main__":
    asyncio.run(seed_db())
