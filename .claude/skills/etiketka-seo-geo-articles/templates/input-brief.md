# Входной бриф запуска — {{дата}}

Единственный обязательный параметр — `url`. Остальные поля заполняются пользователем или значением `auto` (агент решает сам и фиксирует решение).

```yaml
url:                 # обязательный. Пример: https://etiketka.express/etiketki-dlya-kosmetiki-parfyumerii
mode: auto           # on-page | blog | rewrite | cluster | refresh | audit | auto
region:              # по умолчанию: Россия; Москва и МО; СПб и ЛО
  - Россия
  - Москва и Московская область
  - Санкт-Петербург и Ленинградская область
wordstat_source: auto    # путь к выгрузке | auto (поиск файлов → MCP-инструменты → пометка «предварительно»)
existing_semantics: auto # путь к существующему ядру | auto
audience: B2B
primary_goal: qualified_leads
content_length: auto     # auto = по интенту (editorial-guidelines §объём)
competitor_analysis: true
yandex_epos: true
geo_optimization: true
cannibalization_check: true
technical_fact_check: true
visual_compatibility: true
publication: manual_approval   # агент никогда не публикует сам
```

## Зафиксированные решения агента (заполняется агентом)

- Выбранный режим и почему:
- Источник Wordstat и его статус (подтверждён / предварительно):
- Регионы замеров:
- Ограничения запуска (нет сети / нет выгрузки / капча и т.п.):
