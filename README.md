# Дипломная работа: DF1 API для управления библиотекой

## Описание задачи:
Необходимо разработать REST API для управления библиотекой. API должно предоставлять возможности для управления книгами,
авторами и пользователями, а также для отслеживания выдачи книг пользователям. Для реализации API использовать Django Rest Framework (DRF).

### Система включает в себя следующие функции:
- Регистрация и авторизация пользователей
- Каталог книг и авторов с возможностью поиска и фильтрации
- Возможность брать книги в библиотеке
- Возможность просматривать историю взятых книг
- Административная панель для управления книгами и пользователями 

### Корневая директория
- config/: директория с конфигурационными файлами проекта
- authors/: директория с приложением для управления авторами книг
- lendings/: директория с приложением для управления выдачей книг
- books/: директория с приложением для управления книгами
- users/: директория с приложением для управления пользователями
- fixtures/: приложены фикстуры проекта
- manage.py: файл с командами для управления проектом

Авто-документация доступна swagger/ или redoc/

Необходимые настройки произвести в файле .env (.env_sample прилагается)

Создание суперпользователя: python manage.py csu

Создание суперпользователя в докере: docker exec -it drf_homework-app-1 python manage.py csu (пароль и email 
конфигурируются в .env)

### Запуск Celery для реализации отправки писем на почту пользователю
Локально:

celery -A config worker -P eventlet -l info
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

### Docker
Создание и запуск контейнеров - docker-compose up -d --build

Создание суперпользователя - docker exec -it libraryapi_diplom-app-1 python manage.py csu

Celery и celery-beat запускаются автоматически


Автор: Алексей Литвинов