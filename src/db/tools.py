from models.country import Country
from models.friend import Friend
from models.user import User
from utils.utils import hash_password
from .session import async_session
from sqlalchemy import select


async def get_countries(region: str | None = None):
    async with async_session() as session:
        if region:
            countries = (await session.scalars(select(Country).where(Country.region == region))).all()
        else:
            countries = (await session.scalars(select(Country))).all()

        return [country.to_dict() for country in countries]


async def get_country(alpha2: str):
    async with async_session() as session:
        country = await session.scalar(select(Country).where(Country.alpha2 == alpha2))
        return country.to_dict()


async def create_user(login: str, password: str, email: str, countryCode: str, isPublic: bool, image: str | None = None, phone: str | None = None):
    async with async_session() as session:
        existing_login = await session.scalar(select(User).where(User.login == login))
        if existing_login:
            return 1, {}

        existing_email = await session.scalar(select(User).where(User.email == email))
        if existing_email:
            return 2, {}

        existing_phone = await session.scalar(select(User).where(phone and User.phone == phone))
        if existing_phone:
            return 3, {}

        passwordHash = hash_password(password)
        new_user = User(login=login, passwordHash=passwordHash,
                        email=email, phone=phone, countryCode=countryCode, isPublic=isPublic, image=image)
        session.add(new_user)
        await session.commit()
        return 0, new_user.to_dict()


async def sign_in(login: str, password: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.login == login))
        passwordHash = hash_password(password)
        if user and user.passwordHash == passwordHash:
            return user.to_dict()
        return None


async def get_user_by_login(login: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.login == login))
        return user.to_dict()


async def update_user(login: str, data: dict):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.login == login))
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
        await session.commit()
        return user.to_dict()


async def get_user(login: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.login == login))
        return user.to_dict()

async def add_friend(inviter_id: int, invitee_login: str):
    async with async_session() as session:
        invitee = await session.scalar(select(User).where(User.login == invitee_login))
        if not invitee:
            return 1
        
        invitee_id = invitee.id
        if inviter_id == invitee_id:
            return 2
        
        friend_group = await session.scalar(select(Friend).where(Friend.inviter_id == inviter_id and Friend.invitee_id == invitee_id or Friend.inviter_id == invitee_id and Friend.invitee_id == inviter_id))
        if friend_group:
            return 3
        
        new_friend = Friend(inviter_id=inviter_id, invitee_id=invitee_id)
        session.add(new_friend)
        await session.commit()
        return 0
    
async def remove_friend(inviter_id: int, invitee_login: str):
    async with async_session() as session:
        invitee = await session.scalar(select(User).where(User.login == invitee_login))
        if not invitee:
            return 1
        
        invitee_id = invitee.id
        if inviter_id == invitee_id:
            return 2
        
        friend_group = await session.scalar(select(Friend).where(Friend.inviter_id == inviter_id and Friend.invitee_id == invitee_id or Friend.inviter_id == invitee_id and Friend.invitee_id == inviter_id))
        if not friend_group:
            return 3
        
        await session.delete(friend_group)
        await session.commit()
        return 0