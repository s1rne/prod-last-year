import time
from models.auth import Session
from models.country import Country
from models.friend import Friend
from models.posts import Post
from models.user import User
from schemas.posts import NewPostRequest
from utils.utils import hash_password
from .session import async_session
from sqlalchemy import delete, select, update


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
            return user.to_dict(), user.id
        return None, None


async def get_user_by_login(login: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.login == login))
        return user.to_dict()


async def get_user_by_id(id: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == id))
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


async def get_friends(user_id: int, limit: int = 1_000_000, offset: int = 0):
    async with async_session() as session:
        friends = await session.scalars(
            select(Friend)
            .where(Friend.inviter_id == user_id)
            .order_by(Friend.addedAt.desc())
            .offset(offset)
            .limit(limit)
        )
        if friends is None:
            return []
        return [await friend.friend_dict() for friend in friends]


async def create_session(user_id: str, token: str):
    async with async_session() as session:
        new_session = Session(user_id=user_id, token=token,
                              last_online_time=time.time())
        session.add(new_session)
        await session.commit()
        return new_session.to_dict()


async def delete_sessions(user_id: str):
    async with async_session() as session:
        await session.execute(delete(Session).where(Session.user_id == user_id))
        await session.commit()


async def get_session(token: str):
    async with async_session() as session:
        session = await session.scalar(select(Session).where(Session.token == token))
        return session.to_dict()


async def update_online_time_session(token: str):
    async with async_session() as session:
        await session.execute(update(Session).where(Session.token == token).values(last_online_time=time.time()))
        await session.commit()


async def new_post(user_id: int, data: NewPostRequest):
    async with async_session() as session:
        new_post = Post(user_id=user_id, content=data.content, tags=data.tags)
        session.add(new_post)
        await session.commit()
        return new_post.to_dict()


async def get_post_by_id(post_id: str, seeker_id: str):
    async with async_session() as session:
        post = await session.scalar(select(Post).where(Post.id == post_id))
        if not post:
            return 1, {}

        author = await get_user_by_id(post.user_id)
        if not author:
            return 2, {}

        if author["isPublic"] == False:
            if seeker_id == author["id"]:
                pass
            else:
                is_friend = await session.scalar(select(Friend).where(Friend.inviter_id == author["id"] and Friend.invitee_id == seeker_id))
                if not is_friend:
                    return 3, {}

        return 0, post.to_dict()


async def get_posts_my(user_id: int, limit: int = 1_000_000, offset: int = 0):
    async with async_session() as session:
        posts = await session.scalars(select(Post).where(Post.user_id == user_id).order_by(Post.createdAt.desc()).offset(offset).limit(limit))
        if posts is None:
            return []
        return [post.to_dict() for post in posts]


async def get_feed_by_login(login: str, seeker_id: str, limit: int = 1_000_000, offset: int = 0):
    async with async_session() as session:
        author = await session.scalar(select(User).where(User.login == login))
        if not author:
            return 2, []

        if author.isPublic == False:
            if seeker_id == author.id:
                pass
            else:
                is_friend = await session.scalar(select(Friend).where(Friend.inviter_id == author.id and Friend.invitee_id == seeker_id))
                if not is_friend:
                    return 3, []

        posts = await session.scalars(select(Post).where(Post.user_id == author.id).order_by(Post.createdAt.desc()).offset(offset).limit(limit))
        if posts is None:
            return 0, []
        return 0, [post.to_dict() for post in posts]
