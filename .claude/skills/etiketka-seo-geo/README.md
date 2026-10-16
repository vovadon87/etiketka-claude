# etiketka-seo-geo

Навык Claude для SEO и GEO сайта etiketka.express. Один навык, девять режимов.

## Установка

**Claude Code** (проектный или личный навык):
```
mkdir -p .claude/skills && cp -r etiketka-seo-geo .claude/skills/      # для проекта
# или
cp -r etiketka-seo-geo ~/.claude/skills/                                # для пользователя
```
Claude Code находит `SKILL.md` сам и включает навык, когда запрос совпадает с описанием (документация Anthropic: Agent Skills, раздел «Use Skills in Claude Code»).

**claude.ai**: по документации Anthropic пользовательские навыки можно загрузить в настройках (Настройки → Возможности → Навыки), zip-архивом с папкой `etiketka-seo-geo/SKILL.md` в корне. Скрипты из `scripts/` работают в claude.ai только при включённом выполнении кода; доступ к сайту зависит от разрешений сети в вашем аккаунте. Без них навык работает в режиме «инструкции + шаблоны».

**API**: передать навык через `container.skills` (Code Execution Tool), см. документацию «Using Agent Skills with the API».

## Примеры запуска

```
etiketka-seo-geo audit https://etiketka.express/            # аудит главной
etiketka-seo-geo audit site                                 # весь сайт по sitemap
etiketka-seo-geo page https://etiketka.express/etiketki-dlya-kosmetiki-parfyumerii
etiketka-seo-geo semantics косметика                        # семантика направления
etiketka-seo-geo content "этикетки для шампуней"            # бриф + тексты
etiketka-seo-geo geo https://etiketka.express/              # GEO-аудит
etiketka-seo-geo local СПб Москва                           # региональное SEO
etiketka-seo-geo implement publish/kosmetika --dry-run      # пакет правок без записи
etiketka-seo-geo verify https://etiketka.express/            # повторная проверка
etiketka-seo-geo report 2026-09 2026-10                     # сравнение периодов
```
Естественные фразы тоже работают: «проверь главную на SEO», «подготовь title и описание для страницы косметики», «что поправить на сайте для ответов ИИ».

Опции: `--dry-run` (только пакет правок), `--no-network` (без запросов к сайту, по файлам проекта), `--scope <url|папка>`.

## Скрипты

```
python scripts/crawl.py https://etiketka.express/ [--out crawl.json]   # сайт: домены, robots, sitemap, страницы
python scripts/check_page.py <url>                                     # одна страница, подробно
```
Только стандартная библиотека Python 3.9+. Скрипты читают сайт, ничего не изменяют.

## Что навык делает сам, а что требует разрешения

Сам: аудиты, тексты, файлы, черновики, пакеты правок, правки в локальных блоках T123 (с копией в `archive/`).
С разрешения: изменения на опубликованном сайте и в Tilda. Доступа к Tilda у навыка нет — он отдаёт точные инструкции.
