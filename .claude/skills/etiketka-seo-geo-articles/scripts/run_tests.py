#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Тесты критических функций навыка. Запуск: python run_tests.py (код 0 = все прошли)."""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import wordstat_io as w
import quality_checks as q

PASSED = []
FAILED = []


def check(name, cond, detail=""):
    (PASSED if cond else FAILED).append(name)
    print(("ok   " if cond else "FAIL ") + name + (f" — {detail}" if detail and not cond else ""))


# --- wordstat_io: parse_frequency ---
check("частотность: целое", w.parse_frequency(115) == (True, 115))
check("частотность: строка с пробелом '13 795'", w.parse_frequency("13 795") == (True, 13795))
check("частотность: 'нет данных' -> None", w.parse_frequency("нет данных") == (True, None))
check("частотность: пустая -> None", w.parse_frequency("") == (True, None))
check("частотность: мусор отклоняется", w.parse_frequency("примерно 100")[0] is False)
check("частотность: отрицательная отклоняется", w.parse_frequency(-5)[0] is False)
check("частотность: дробная отклоняется", w.parse_frequency(3.7)[0] is False)

# --- wordstat_io: normalize_phrase ---
check("нормализация: регистр/ё/операторы",
      w.normalize_phrase('  "Этикетки  для КОСМЕТИКИ!" ') == "этикетки для косметики")
check("нормализация: !слово", w.normalize_phrase("!наклейки !на !косметику") == "наклейки на косметику")

# --- wordstat_io: CSV цикл validate/dedupe/export ---
tmp = tempfile.mkdtemp()
src = os.path.join(tmp, "core.csv")
with io.open(src, "w", encoding="utf-8-sig", newline="") as f:
    f.write("Запрос;Частотность без операторов;Частотность в кавычках\n")
    f.write("этикетки для косметики;205;10\n")
    f.write("Этикетки для косметики;205;нет данных\n")   # дубль по норме
    f.write("наклейки на флаконы духов;76;\n")
errors, data, idx = w.validate(src, verbose=False)
check("validate: ошибок нет на корректном файле", errors == [] and len(data) == 3)
dups = w.find_duplicates(src, verbose=False)
check("dedupe: находит дубль по нормализованной форме", len(dups) == 1)

bad = os.path.join(tmp, "bad.csv")
with io.open(bad, "w", encoding="utf-8-sig", newline="") as f:
    f.write("Запрос;Частотность без операторов\n")
    f.write("этикетки;около 200\n")
errors_bad, _, _ = w.validate(bad, verbose=False)
check("validate: ловит выдуманную/нечисловую частотность", len(errors_bad) == 1)

dst = os.path.join(tmp, "out.csv")
n = w.export(src, dst, force=False)
check("export: канонический CSV создан", n == 3 and os.path.exists(dst))
with io.open(dst, encoding="utf-8-sig") as f:
    content = f.read()
check("export: заголовок канонический", content.splitlines()[0].startswith("Исходная фраза;Частотность без операторов"))
check("export: 'нет данных' сохранён, не превращён в число", "нет данных" in content)
try:
    w.export(src, dst, force=False)
    check("export: защита от перезаписи", False)
except SystemExit:
    check("export: защита от перезаписи", True)
try:
    w.export(src, src, force=True)
    check("export: запись в исходник запрещена", False)
except SystemExit:
    check("export: запись в исходник запрещена", True)

# --- quality_checks ---
spam = ("## Печать этикеток\n\nВ современном мире печать этикеток для косметики это печать этикеток "
        "недорого. Наша компания предлагает печать этикеток для косметики. "
        "Печать этикеток для косметики в Москве, Санкт-Петербурге, Казани, Новосибирске.\n\n"
        "## Печать этикеток для косметики цена\n\n## Печать этикеток для косметики срочно\n")
rep = q.analyze(spam)
check("anti-spam: находит шаблонные обороты", "в современном мире" in rep["template_phrases"])
check("anti-spam: находит повтор n-грамм", any(x["count"] >= 4 for x in rep["repeated_ngrams"]))
check("anti-spam: слово в 3+ заголовках", any(x["headings"] >= 3 for x in rep["heading_repeats"]))
check("anti-spam: гео-перечисление", len(rep["geo_enumerations"]) >= 1)

clean = ("## Какой материал выбрать для флакона в ванной\n\n"
         "Если упаковка контактирует с водой, бумага без защиты размокает. "
         "Для душевой продукции подходит полимерная плёнка: она не теряет вид от влаги.\n\n"
         "## Как подготовить макет\n\nДобавьте вылеты 2–3 мм и переведите шрифты в кривые. "
         "Растровые изображения — 300 dpi в масштабе один к одному.\n")
rep2 = q.analyze(clean)
check("anti-spam: чистый текст без ложных срабатываний",
      not rep2["template_phrases"] and not rep2["flag_lemma_overuse"] and not rep2["geo_enumerations"])

dup_text = "## А\n\n" + ("Прозрачная плёнка сохраняет видимость флакона и подходит для гладкой тары без рельефа. " * 2) + "\n\n" + \
           "Прозрачная плёнка сохраняет видимость флакона и подходит для гладкой тары без рельефа и пузырей на поверхности после нанесения этикетки вручную.\n"
rep3 = q.analyze(dup_text)
check("anti-spam: похожие абзацы", len(rep3["similar_paragraphs"]) >= 1)

# --- md_to_html ---
import md_to_html as h

sample = ("<!-- служебный комментарий -->\n# Заголовок\n\nАбзац с **жирным** и [ссылкой](https://etiketka.express/naklejki) & знаком <.\n\n"
          "## Раздел\n\n- пункт один\n- пункт два\n\n1. первый\n2. второй\n\n"
          "| А | Б |\n|---|---|\n| 1 | **2** |\n")
out = h.convert(sample)
check("md_to_html: комментарии отброшены", "служебный" not in out)
check("md_to_html: h1/h2", "<h1>Заголовок</h1>" in out and "<h2>Раздел</h2>" in out)
check("md_to_html: жирный и ссылка", "<strong>жирным</strong>" in out and '<a href="https://etiketka.express/naklejki">ссылкой</a>' in out)
check("md_to_html: экранирование &, <", "&amp;" in out and "&lt;" in out)
check("md_to_html: списки", "<ul>" in out and "<li>пункт два</li>" in out and "<ol>" in out and "<li>второй</li>" in out)
check("md_to_html: таблица", "<table>" in out and "<th>А</th>" in out and "<td><strong>2</strong></td>" in out)
check("md_to_html: нет инлайн-стилей в теле", "style=" not in out)
check("md_to_html: javascript-ссылка не превращается в ссылку", "<a href=\"javascript" not in h.convert("[x](javascript:alert(1))"))

print(f"\nИтого: {len(PASSED)} прошло, {len(FAILED)} провалено")
sys.exit(1 if FAILED else 0)
