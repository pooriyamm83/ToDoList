# To Do List Project - Phase 1 (In-Memory)

**دانشگاه صنعتی امیرکبیر - درس مهندسی نرم‌افزار - پاییز ۱۴۰۴**  
**تهیه‌کننده:** پوریا محمدی  
**ریپازیتوری:** https://github.com/pooriyamm83/ToDoList

---

## وضعیت پیاده‌سازی User Stories (تمام موارد فاز ۱ پیاده‌سازی شده‌اند)

| # | User Story | وضعیت | توضیحات |
|---|-----------|-------|--------|
| ۱ | ساخت پروژه | Completed | `project-create` با نام و توضیحات |
| ۲ | ویرایش پروژه | Completed | `project-edit` |
| ۳ | حذف پروژه (Cascade Delete) | Completed | حذف پروژه → تمام تسک‌ها حذف می‌شوند |
| ۴ | افزودن تسک | Completed | `task-add` با عنوان، توضیحات و ددلاین اختیاری |
| ۵ | تغییر وضعیت تسک | Completed | `task-status` → todo / doing / done |
| ۶ | ویرایش تسک | Completed | `task-edit` (عنوان، توضیحات، ددلاین) |
| ۷ | حذف تسک | Completed | `task-delete` |
| ۸ | نمایش لیست پروژه‌ها | Completed | `project-list` |
| ۹ | نمایش تسک‌های یک پروژه | Completed | `task-list <proj-id>` |

**تمام Acceptance Criteria های ذکر شده در مستند پیاده‌سازی شده‌اند.**

---

## ویژگی‌های پیاده‌سازی شده (Non-Functional)

- استفاده از **OOP** کامل (جداسازی Model / Repository / CLI)
- اعتبارسنجی طول عنوان و توضیحات (۳۰ و ۱۵۰ کاراکتر)
- اعتبارسنجی فرمت ددلاین (`YYYY-MM-DD`)
- محدودیت تعداد پروژه و تسک از طریق **.env**
- **Cascade Delete** کامل (حذف پروژه → حذف تمام تسک‌ها)
- استفاده از **Poetry** برای مدیریت وابستگی‌ها
- استفاده از **python-dotenv** برای بارگذاری تنظیمات
- ساختار لایه‌ای و قابل توسعه برای فازهای بعدی (Persistancy, API و ...)

---

## ساختار پروژه
todo_list_app/
├── todo_list_app/              # پکیج اصلی

│   ├── models/                 # Task و Project

│   ├── repository.py          # In-Memory Repository

│   ├── cli.py                  # رابط خط فرمان

│   ├── config.py               # بارگذاری .env

│   └── main.py

├── .env                        # تنظیمات محلی (در .gitignore)

├── .env.example                # نمونه تنظیمات

├── pyproject.toml

└── README.md

---

## نصب و اجرا

```bash
# کلون کردن پروژه
git clone https://github.com/pooriyamm83/ToDoList.git
cd ToDoList

# نصب وابستگی‌ها با Poetry
poetry install

# کپی کردن فایل تنظیمات
cp .env.example .env
# (در صورت نیاز مقادیر MAX_NUMBER_OF_PROJECT و MAX_NUMBER_OF_TASK را تغییر دهید)

# اجرای برنامه
poetry run python -m todo_list_app
project-create <نام> [توضیحات]              → ساخت پروژه جدید
project-list                                 → نمایش همه پروژه‌ها
project-edit <id> <نام جدید> [توضیحات]      → ویرایش پروژه
project-delete <id>                          → حذف پروژه و تمام تسک‌ها

task-add <proj-id> <عنوان> [توضیحات] [ددلاین]   → افزودن تسک (ددلاین: YYYY-MM-DD)
task-list <proj-id>                          → نمایش تسک‌های یک پروژه
task-status <proj-id> <task-id> <todo|doing|done> → تغییر وضعیت
task-edit <proj-id> <task-id> <عنوان جدید> [توضیحات] [ددلاین جدید]
task-delete <proj-id> <task-id>              → حذف تسک

help                                         → نمایش راهنما
exit                                         → خروج
تنظیمات (.env)
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
