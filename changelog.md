# Changelog

## v0.2.0 
### Добавлено (31.05.2025)
- Была создана база данных, где будут храниться загруженные файлы.
- После была создана модель для бд и добавлен функционал добавления в бд при обработке данных
- Создан [docker-compose](text_analyzer/docker-compose.yml). В нём теперь собираются отдельные 2 контейнера, это: web и db.
- Развёрнут docker-compose на виртуалке.

### Добавлено (30.05.2025)
- Докер файл был разбит на build и deploy для уменьшения веса контейнера.
- Был перекинут docker контейнер на виртуалку и запущен сервер

### Добавлено (26.05.2025)
- Частично были внесены конфигурируемые параметры в файл `.env`:
  - Порт приложения (PORT)
  - Переменные Django: `SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`
  - Параметры подключения к базе данных: `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`


- Был добавлен Docker [файл](text_analyzer/Dockerfile).
- Был добавлен функционал [метрик](text_analyzer/system/metrics.py), в нём прописаны функции для их расчёта.
- Были добавлены эндпоинты в [endpoints.py](text_analyzer/system/endpoints.py) и добавлены пути к ним в [urls.py](text_analyzer/text_analyzer/urls.py)
- Был добавлен файл [requirements](text_analyzer/requirements.txt), в который были записаны необходимые параметры окружения.



