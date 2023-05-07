# Телеграм бот для сохранения логинов и паролей
## **About**
Данный телеграм бот позволяет сохранять пароли для разных сервисов в одном месте.

Поддерживаются следущие команды:
- /start - выводит приветсвенное сообщение
- /set - добавляет сервис, логин и пароль (сообщения от пользователя удаляются после обработки)
- /cancel - отменяет ввод данных 
- /get выводит список сервисов в ввиде inline кнопок, после выбора сервиса выводятся логин и пароль (сообщение с логином и паролем удаляются через 10 секунд)
- /del выводит список сервисов в ввиде inline кнопок, после выбора сервиса, он удаляется

## **Quick start**
Перед запуском необходимо переименовать файлы env_example и bot/env_example в .env и поменять значения переменных на свои.
Развертывание приложения происходит в Docker с помощью команды 
```
docker-compose up -d --build
```
## **Other**
В качестве базы данных используется postgresql, логин и пароль хранятся в базе данных в зашифрованном виде.
Бот развернут на удаленном сервере https://t.me/vk_password_saver_bot
