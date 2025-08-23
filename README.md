
## architectire


```mermaid
    flowchart TD
        subgraph Client
            TG[movie_rec_bot]
        end

        subgraph Backend
            API[userver Backend]
            RS[Recommender System ML Core]
            DB[(PostgreSQL Database)]
        end

        TG -->|User's queries| API
        API -->|Deriving data of films, hostory| DB
        API -->|Model query| RS
        RS -->|Rec films| API
        API -->|Backend's answer| TG
```

## roadmap

```mermaid
    gantt
    title Roadmap проекта "movie_rec_bot"
    dateFormat  YYYY-DD
    axisFormat  %d

    section Подготовка
    Определение функционала             :done,    des1, 2025-19, 1h
    Проектирование архитектуры          :done,  des2, after des1, 1h

    section Бекенд и бд
    Настройка PostgreSQL сервиса                :active, b1, after des2, 4h
    Реализация Backend(KrakenD, Nginx, ,FastAPI)          :b2, after b1, 12h

    section ML часть
    Интеграция модели в API       :c1, after b2, 10h

    section Telegram Bot
    Создание бота и UI            :d1, after c1, 14h
    Интеграция с API              :d2, after d1, 1d

    section Завершение
    Тестирование                  :e1, after d2, 8h
    Деплой                        :e2, after d2, 8h

```

### request-response cycle

1. user authorizing: tg-bot(client) send request on API Gateway;
2. server process the query and send query to the DB for auth/reg;
3. user input film: tg -> krakend -> ml_core -> server -> tg
4. user getting 5 similar films with photo, description, aability to resend requery and watch trailer;

### instruments

- tg libs: aiogram
- backend: FastAPI, Nginx, KrakenD, RabbitMQ
- db: PostgreSQL
- ml: model(sentence-transformer)
