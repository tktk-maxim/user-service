from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" ADD "chat_id" INT;
        ALTER TABLE "employee" ADD "telegram_name" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "employee" DROP COLUMN "chat_id";
        ALTER TABLE "employee" DROP COLUMN "telegram_name";"""
