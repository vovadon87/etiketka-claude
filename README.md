# etiketka-claude

Агент и навыки Claude Code для SEO/GEO-работы с сайтом типографии этикеток [etiketka.express](https://etiketka.express) («Ваша Этикетка»).

## Состав

```text
.claude/
├── agents/
│   └── etiketka-seo-geo-writer.md      # агент: пишет SEO/GEO-статьи по полному конвейеру
└── skills/
    ├── etiketka-seo-geo/               # базовый навык: аудит, семантика, техSEO, GEO, Tilda
    └── etiketka-seo-geo-articles/      # навык статей: Wordstat → интент → ТЗ → статья → ЭПОС → 12 ворот QA
```

Агент предзагружает оба навыка (поле `skills` во frontmatter). Факты компании — только из `etiketka-seo-geo/references/site-context.md` со статусами «подтверждено владельцем / опубликовано на сайте».

## Запуск

В сессии Claude Code (локальной из этого каталога или облачной на этом репозитории):

```text
@agent-etiketka-seo-geo-writer https://etiketka.express/<страница> [on-page|blog|rewrite|cluster|refresh|audit|auto]
```

или фразой: «используй агента etiketka-seo-geo-writer для <URL>».

Тесты скриптов: `python .claude/skills/etiketka-seo-geo-articles/scripts/run_tests.py`.

## Ограничения облачных сессий

- Живых MCP-инструментов Wordstat в облаке нет — выгрузки частотности нужно класть в репозиторий (например, в `semantics/`) и указывать путь при запуске; без них агент выдаёт черновик с пометкой «семантика предварительная».
- Частотность никогда не выдумывается; публикация на сайт — только вручную владельцем.

## Канон

Рабочие копии навыков живут в `~/.claude/` на основной машине; при изменениях синхронизировать их сюда коммитом. Результаты запусков (`outputs/…`) в репозиторий не коммитятся, если не нужны облаку.
