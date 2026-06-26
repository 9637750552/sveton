# Yandex Forms for Sveton

Этот каталог содержит локальный скрипт для создания анкет в Yandex Forms через API.

## Состав

- `create_yandex_form.py` - создание анкеты по YAML/JSON-спецификации.
- `requirements.txt` - Python-зависимости.
- `input/form.example.yaml` - базовый пример спецификации.
- `input/sveton_form_template.yaml` - стартовый шаблон под Светон.
- `assets/sveton-logo.png` - логотип Светона для ручной загрузки в шапку анкеты.

## Установка

В этом проекте настроен запуск без системного `venv`, чтобы скрипт работал в текущем окружении без `sudo`.

```bash
cd /home/sergey/Sveton/07_forms
python3 -m pip install --upgrade pip
python3 -m pip install --target .deps -r requirements.txt
```

## Переменные окружения

Скрипт ожидает:

- `YANDEX_FORMS_TOKEN`
- `YANDEX_FORMS_ORG_ID`

Пример для текущей сессии:

```bash
export YANDEX_FORMS_TOKEN="your_oauth_token"
export YANDEX_FORMS_ORG_ID="940878"
```

Вместо переменных можно передать значения флагами:

```bash
./run_create_yandex_form.sh input/sveton_form_template.yaml --token "your_oauth_token" --org-id "940878"
```

## Проверка спецификации

```bash
./run_create_yandex_form.sh input/sveton_form_template.yaml --dry-run
```

Если файл не передать, скрипт покажет интерактивный список анкет из папки `input/`:

```bash
python3 create_yandex_form.py
```

## Создание анкеты

Черновик:

```bash
./run_create_yandex_form.sh input/sveton_form_template.yaml
```

С публикацией:

```bash
./run_create_yandex_form.sh input/sveton_form_template.yaml --publish
```

## Логотип Светона

Файл для загрузки в анкету:

- `/home/sergey/Sveton/07_forms/assets/sveton-logo.png`

Текущий API-скрипт не загружает логотип автоматически. После создания анкеты откройте `admin_url` из вывода скрипта и добавьте логотип в редакторе Yandex Forms вручную.
