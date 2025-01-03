# Базовая архитектура проекта на fastapi на примере задания прошлых лет олимпиады PROD

### Запуск проекта

```bash
docker-compose up -d
```

##
### Задания олимпиады PROD
- [x] `01/ping` -> Успешный ответ на /api/ping.
- [x] `02/countries` -> Получение и фильтрация стран.
- [x] `03/auth/register` -> Регистрация пользователей.
- [x] `04/auth/sign-in` -> Аутентификация и получение токена.
- [x] `05/me` -> Получение и редактирование собственного профиля.
- [x] `06/profiles` -> Получение профиля по логину.
- [x] `07/password` -> Изменение пароля.
- [x] `08/friends` -> Друзья!
- [x] `09/posts/publish` -> Публикация поста и получение по ID.
- [x] `10/posts/feed` -> Получение новостной ленты.
- [x] `11/posts/likes` -> Лайки и дизлайки.

##
#### Полное описание кейса можно найти [тут](https://github.com/Central-University-IT/test-python/blob/main/README.md)
#### Требуемую cхему api можно найти в [tests/openapi.yml](./tests/openapi.yml)

## 
#### - python:3.12
#### - postgres:latest