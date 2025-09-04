# Movie recommender

Телеграм-бот для интеллектуальной рекомендации фильмов на основе ввденного фильма. Реализована микросервисная архиктура с Krakend API-Gateway, Nginx и ml kernel(content-based sentence-transformer).

---

## Архитектура

```mermaid
    flowchart TD
        subgraph Client
            TG[movie_rec_bot]
        end

        subgraph Backend
            API[Nginx]
            RS[Recommender System ML Core]
            DB[PostgreSQL Database]
        end

        TG -->|TG-BOT's queries| API
        API -->|Sending data of films, history| DB
        API -->|Model query| RS
        RS -->|Rec films| API
        API -->|Backend's answer| TG
        DB --> |Request status| API
```
---

## Дорожная карта

```mermaid
    gantt
    title Roadmap проекта "movie_rec_bot"
    dateFormat  YYYY-DD
    axisFormat  %d

    section Подготовка
    Определение функционала             :done,    des1, 2025-19, 1h
    Проектирование архитектуры          :done,  des2, after des1, 1h

    section Бекенд и бд
    Настройка PostgreSQL сервиса                :done, b1, after des2, 4h
    Реализация Backend(KrakenD, Nginx,FastAPI)          :done, b2, after b1, 12h

    section ML часть
    Создание M(ядро)-сервиса       :done, c1, after b2, 10h

    section Telegram Bot
    Создание бота и UI            :done, d1, after c1, 14h
    Интеграция с API              :done, d2, after d1, 1d

    section Завершение
    Тестирование                  :done, e1, after d2, 8h
    Деплой                        :done, e2, after d2, 8h

```
---

## Технологический стек

### Микросервисная архиктерктура(FastAPI)

#### Database сервис
-  PostgreSQL(история запросов для каждой сессии)
-  SQLModel(для коннекта с постгресом и инициализации моделей данных)
  
#### Ml-ядро сервис
- Sentence-transformer
- Nltk

#### KrakenD сервиса
- KrakenD(API-Gateway) 

#### Nginx сервис
- Nginx(load balancer & reverse proxy)) 

#### Telegram Bot service
- Aiogram

#### Инфраструктура
- Docker, Docker Compose(в каждом сервисе для независимой масштабирования оркестрации сервиса)
- GitLab CI(непрерывная интеграция в гитлаб(только деплой))


## Старт
1. Клонируем репу:
   >git clone https://github.com/Sosylka19/rec_sys.git`
   
2. Переходим в папку проекта
   >cd rec_sys

3. Для удобного поднятия всех сервисов написан Makefile:
    >make start

#### Описание команд Makefile:

-- __make start__ - запускает все контейнеры

-- __make <название сервиса>__ - собирает отдельный сервис с флагом --build

-- __make down_all__ - удаляет все  контейнеры

-- __make down___**<название сервиса>** - удаляет определенный контейнер


