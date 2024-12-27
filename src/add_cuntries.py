import asyncio
from db.session import async_session
from models.country import Country


async def add_countries():
    async with async_session() as session:
        datas = [
            ('Åland Islands', 'AX', 'ALA', 'Europe'),
            ('Albania', 'AL', 'ALB', 'Europe'),
        ]
        for data in datas:
            session.add(Country(name=data[0], alpha2=data[1], alpha3=data[2], region=data[3]))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_countries())
