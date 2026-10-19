# etiketka-claude

Агент и навыки Claude Code для SEO/GEO-работы с сайтом типографии этикеток [etiketka.express](https://etiketka.express) («Ваша Этикетка»).

## Состав

```text
.claude/
├── agents/
│   └── etiketka-seo-geo-writer.md      # агент: пишет SEO/GEO-статьи по полному конвейеру
└── skills/
    ├── audit-seo-geo/                  # базовый навык: аудит, семантика, техSEO, GEO, Tilda;
    │   └── sites/etiketka/             #   профиль сайта и факты компании (site-context.md)
    └── etiketka-seo-geo-articles/      # навык статей: Wordstat → интент → ТЗ → статья → ЭПОС → 12 ворот QA
semantics/                              # выгрузки Wordstat владельца (только чтение)
```

Агент предзагружает оба навыка (поле `skills` во frontmatter). Факты компании — только из `audit-seo-geo/sites/etiketka/site-context.md` со статусами «подтверждено владельцем / опубликовано на сайте». Общеотраслевые сведения не подтверждают возможности компании (правило в `templates/fact-check.md`).

## Запуск

В сессии Claude Code (локальной из этого каталога или облачной на этом репозитории):

```text
@agent-etiketka-seo-geo-writer https://etiketka.express/<страница> [on-page|blog|rewrite|cluster|refresh|audit|auto]
```

или фразой: «используй агента etiketka-seo-geo-writer для <URL>». Навык отдельно: `/etiketka-seo-geo-articles on-page <URL>`.

## Скрипты навыка статей (`.claude/skills/etiketka-seo-geo-articles/scripts/`)

| Скрипт | Назначение |
|---|---|
| `wordstat_io.py` | чтение, валидация и дедупликация выгрузок Wordstat (CSV/XLSX); исходники не изменяет |
| `quality_checks.py` | механический анти-спам: повторы, шаблонные обороты, переупотребление слов |
| `md_to_html.py` | статья Markdown → семантический HTML (для вставки в Tilda T123) |
| `build_pdf.py` | статья → PDF через headless Chrome/Edge (для согласования) |
| `run_tests.py` | тесты (31): `python .claude/skills/etiketka-seo-geo-articles/scripts/run_tests.py` |

## Ограничения облачных сессий

- Живых MCP-инструментов Wordstat в облаке нет — используйте выгрузки из `semantics/` (параметр `wordstat_source`); без них агент выдаёт черновик с пометкой «семантика предварительная».
- Для `build_pdf.py` нужен Chrome или Edge (в облаке может отсутствовать — тогда сохраняйте HTML).
- Частотность никогда не выдумывается; публикация на сайт — только вручную владельцем.

## Канон

Рабочие копии навыков живут в `~/.claude/` на основной машине; при изменениях синхронизировать сюда коммитом. Результаты запусков (`outputs/…`) в репозиторий не коммитятся (см. `.gitignore`).
