# yamdb_final (CI и CD проекта api_yamdb)
Настройка CI/CD процессов для проекта YaMDb с использованием github action.

![example workflow](https://github.com/mariiabulatova/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## ОПИСАНИЕ ПРОЕКТА
Настройка втоматического разворачивания проекта YaMDb(1), предварительно запакованного в Docker-контейнеры, на удаленный сервер (виртуальная машина на Yandex.Cloud) при поможи github actions. Выполняется при запуске команды "git push" в ветку "master".

(1)Проект YaMDb собирает текстовые отзывы (**Review**) и ретинги (**целое число** в диапазоне от одного до десяти)
от пользователей (**User**)
на произведения (**Title**)
разных категорий (**Category**: книги, фильмы, музыка
(*список предустановлен администратором*))
и разных жанров (**Genre**: сказка, рок, артхаус
(*список предустановлен администратором*)).

___
Запросы к API через api/v1, например:
```
http://<remote server>/api/v1/
http://62.84.121.204/api/v1/
```
Документация по адресу:
```
http://<remote server>/redoc/
http://62.84.121.204/redoc
```
Админка:
```
http://<remote server>/admin
http://62.84.121.204/admin
```
