# Messenger Pro

Месенджер на Django: глобальний чат, приватні діалоги, профілі користувачів
і оновлення повідомлень без перезавантаження сторінки (HTMX).

## Можливості

- Реєстрація / вхід, профіль з аватаркою, біографією та датою народження
- Глобальний чат для всіх користувачів
- Приватні діалоги: пошук користувача → створення або відкриття існуючого треду
- Список чатів із останнім повідомленням (відсортований за часом)
- Надсилання повідомлень через **HTMX** — без перезавантаження сторінки
- Адмінка Django, міграції, кастомна модель користувача

## Технології

Python 3.12+ · Django 6 · HTMX · SQLite · django-environ

## Локальний запуск

```powershell
# 1. Віртуальне середовище та залежності
python -m venv venv
venv\Scripts\activate
pip install django django-environ pillow

# 2. Налаштування
copy .env.example .env
#   відкрий .env і впиши свій SECRET_KEY

# 3. База даних
python manage.py migrate
python manage.py createsuperuser   # необов'язково, для адмінки

# 4. Запуск
python manage.py runserver
```

Відкрий <http://127.0.0.1:8000/>.

> Файл `.env` містить секрети і в ігнорі git. У репозиторії лежить лише
> `.env.example` з прикладом значень.

## Структура проєкту

```
config/                  # налаштування, urls, wsgi/asgi
apps/
├── accounts/            # реєстрація, вхід, профіль, кастомний User
│   ├── models.py        # User + Profile (аватар, bio, дата народження)
│   ├── forms.py
│   └── templates/accounts/
└── chat/                # чати
    ├── models.py        # Thread (треди) і Message (повідомлення)
    ├── views.py         # глобальний чат, список чатів, пошук, приватна кімната
    └── templates/chat/
        ├── room.html              # глобальний чат
        ├── private_room.html      # приватний діалог
        ├── chat_list.html         # список чатів
        └── partials/              # шматки розмітки для повторного використання
            ├── message.html
            └── global_message.html
```

## Як влаштована модель даних

```
User (accounts) ──1:1── Profile
      │
      │ M:N через Thread.participants
      ▼
Thread ──1:N── Message ──N:1── sender (User)
```

- **Thread** — діалог між двома учасниками. `Thread.get_or_create_between(u1, u2)`
  повертає існуючий тред або створює новий (і забороняє чат із самим собою).
- **Message** — текст, час і **одне** поле `sender` (автор).
  Поле `user` було видалено як дублікат: воно дублювало `sender` і плутало
  запити. Міграція `0003` спершу переносить дані, потім видаляє поле.

## Як працює оновлення без перезавантаження (HTMX)

Раніше форма робила звичайний `POST → redirect → повне перезавантаження сторінки`.
Тепер:

1. У формі є атрибути HTMX:

   ```html
   <form method="POST"
         hx-post="{% url 'global_chat' %}"   # куди слати POST
         hx-target="#messages"                # куди вставити відповідь
         hx-swap="beforeend"                  # як вставити: в кінець контейнера
         hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
   ```

   Ця ж форма працює і без JavaScript: якщо HTMX не підвантажився,
   відбувається звичайний POST і редирект (у в'юзі є гілка `else`).

2. У в'юзі перевіряємо заголовок `HX-Request`:

   ```python
   if request.headers.get('HX-Request'):
       return render(request, 'chat/partials/message.html', {'msg': message})
   return redirect('global_chat')
   ```

3. Сервер повертає **тільки один** HTML-фрагмент (`partials/`), який HTMX
   вставляє в кінець списку повідомлень. Плюс кілька рядків JS:
   прокрутка вниз і очищення поля введення.

## Запуск тестів

```powershell
python manage.py test
```
