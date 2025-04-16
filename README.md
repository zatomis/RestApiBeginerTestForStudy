# 🍽️ Тестовое задание: API-сервис бронирования столиков в ресторане

## 📌 Цель
Разработать REST API для бронирования столиков в ресторане. Сервис должен позволять создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

## Как начать
### Начальные настройки
* Клонируем репозиторий
```commandline
git clone git@github.com:zatomis/RestApiBeginerTestForStudy.git
```

### Проект может быть развернут на вашем сервере. Используйте dockerfile.
1. Создайте сеть докер
```commandline
docker network create myNetwork
```

2. Создайте образ ! Внимание файл .env должен содержать поля 
![img.png](img.png)
```commandline
docker build -t reservation_image .
```

3. Запустите pg sql в докере. Тут указаны пароли в тестовых целях
```commandline
docker run --name reservations_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=restaurant \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16
```

4. Запустите образ
```commandline
docker run --name reservation_back \
    -p 7777:8000 \
    --network=myNetwork \
    reservation_image
```

5. Запустите в браузере 
![img_1.png](img_1.png)
```commandline
    http://хх.хх.хх.хх:7777/docs
    где вместо хх - ваш ip адрес сервера
```

## Предварительная подготовка для запуска в Dockercompose

## Цель проекта
Код написан в тестовых целях 


x#команда ниже работает через композ
docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image

[//]: # ( это локально)
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx 

[//]: # ( это на сервере + прокинуть папку с сертификатом)
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/letsencrypt:/var/letsencrypt \
    --network=myNetwork \
    -d -p 80:80 -p 443:443 nginx 

------------------------------------------------------------


docker build -t reservation_image .
------------------------------------------------------------

git remote add gitlab git@gitlab.com:zatomis/booking.git 
git push --all gitlab
------------------------------------------------------------
Gitlab Runner  Запуск раннера
https://habr.com/ru/articles/764568

docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine

Регистрация раннера

docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register

Изменение конфига
Шаг 1
Заходим в режим редактирования конфига через
micro /srv/gitlab-runner/config/config.toml

Шаг 2
Меняем
volumes = ["/cache"] на
volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]


Это для создания и выполнения миграций
alembic revision --autogenerate -m "initial db"
alembic upgrade head