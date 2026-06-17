# Batch 003: ЭЛК 1 / базовые понятия

Дата: 2026-06-16

Модельный режим: `5.5`, высокий уровень.

## Источник

```text
ЭЛК_1_Базовые_знания_Основные_понятия_ред1_1.docx
```

## Результат

- обработано `6` чанков;
- содержательных чанков: `4`;
- служебных/заголовочных чанков: `2`;
- добавлено `14` atomic statements;
- canonical расширен до `165` валидных утверждений;
- создан кластер `C006 / basic_knowledge`;
- создан редакционный раздел `01_basic_knowledge.md`;
- схема `img_0003` привязана к утверждениям по последовательному и параллельному подключению АКБ.

## Особые решения

Строка `DC - переменное напряжение` не включена в canonical как валидное знание, потому что она противоречит строке `DC - это постоянный ток`.

Проблема источника зафиксирована отдельно:

```text
00_input/documents/electricians_knowledge_base/statements/source_quality_issues.md
```

Утверждения по подключению АКБ помечены как `safety_critical` и `review_required`.

## Проверки

- `validate_atomic_statements.py` для batch 003: passed, `14` statements.
- `validate_atomic_statements.py` для canonical: passed, `165` statements.
- `check_source_coverage.py` для 6 редакционных источников: passed, `0` uncovered content chunks.
