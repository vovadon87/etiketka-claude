# audit-seo-geo

Навык Claude для SEO и GEO любого сайта. Ядро общее, факты каждой компании лежат в профиле `sites/<имя>/`. Один навык, десять режимов.

Профили: `etiketka` (etiketka.express). Новый сайт добавляется режимом `onboard` (образец — `sites/_template/`).

## Установка (Claude Code)
```
cp -r audit-seo-geo ~/.claude/skills/
```
Claude Code находит `SKILL.md` сам и включает навык, когда запрос совпадает с описанием.

## Примеры запуска
```
audit-seo-geo audit https://etiketka.express/
audit-seo-geo audit site --site=etiketka
audit-seo-geo page https://etiketka.express/etiketki-dlya-kosmetiki-parfyumerii
audit-seo-geo semantics косметика
audit-seo-geo geo https://etiketka.express/
audit-seo-geo onboard https://новый-сайт.ru/
audit-seo-geo verify https://etiketka.express/
audit-seo-geo report 2026-09 2026-10
```
Естественные фразы тоже работают: «проверь главную на SEO», «подготовь title и описание для страницы», «что поправить для ответов ИИ».

Опции: `--site=<профиль>`, `--dry-run` (только пакет правок), `--no-network`, `--scope <url|папка>`.

## Скрипты
```
python -I scripts/crawl.py https://example.ru/ [--out crawl.json] [--pages /a,/b]
python -I scripts/check_page.py <url>
```
Только стандартная библиотека Python 3.9+. Только чтение. Выводят UTF-8.

## Что навык делает сам, а что требует разрешения
Сам: аудиты, тексты, файлы, черновики, пакеты правок.
С разрешения: изменения опубликованного сайта, отправка заявок. Правки в Tilda возможны через Tilda MCP только по команде владельца.

## История
2026-10-19: переработан из `etiketka-seo-geo` в общее ядро + профиль сайта. Прежний навык в `~/.claude/_archive/skills-retired-2026-10-19/`.
