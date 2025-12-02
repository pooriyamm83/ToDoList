# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool, create_engine  # create_engine را اضافه کردیم
from alembic import context

# ----------------------------------------------------------------------
# گام ۱: تنظیم Python Path
# این کار به Alembic اجازه می‌دهد تا پکیج 'app' (و فایل‌های config/models) را پیدا کند.
# ----------------------------------------------------------------------
# os.getcwd() مسیر ریشه پروژه است که اکنون باید شامل 'app' باشد
sys.path.append(os.getcwd())

# ----------------------------------------------------------------------
# گام ۲: ایمپورت تنظیمات و مدل‌ها (محل‌های جدید)
# ----------------------------------------------------------------------
from todo_list_app.db.base import Base
from todo_list_app.config import DATABASE_URL  # ایمپورت URL از فایل کانفیگ

# مدل‌ها باید ایمپورت شوند تا Alembic آن‌ها را برای autogenerate ببیند
from todo_list_app.models.project import Project
from todo_list_app.models.task import Task

# ----------------------------------------------------------------------


# این شیء Alembic Config است
config = context.config

# تنظیم لاگینگ
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# متادیتای ORM شما
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # از DATABASE_URL تعریف شده در todo_list_app/config استفاده می‌کنیم
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    این تابع مستقیماً از DATABASE_URL در todo_list_app/config برای ساختن Engine استفاده می‌کند
    تا از وابستگی به alembic.ini جلوگیری کند.
    """

    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # URL را برای رندر کردن در autogenerate صراحتاً پاس می‌دهیم
            url=DATABASE_URL
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()