# Forms for Sveton

Этот каталог содержит локальные скрипты для создания анкет в Yandex Forms и Nextcloud Forms через API.

## Состав

- `create_yandex_form.py` - создание анкеты по YAML/JSON-спецификации.
- `create_nextcloud_form.py` - создание или синхронизация анкеты в Nextcloud Forms по той же YAML/JSON-спецификации.
- `requirements.txt` - Python-зависимости.
- `input/form.example.yaml` - базовый пример спецификации.
- `input/sveton_form_template.yaml` - стартовый шаблон под Светон.
- `input/electrician_screening_form.yaml` - анкета первичного отбора электриков.
- `input/electrician_express_test_form.yaml` - отдельный экспресс-тест по блоку знаний.
- `assets/sveton-logo.png` - логотип Светона для ручной загрузки в шапку анкеты.

## Установка

В этом проекте настроен запуск без системного `venv`, чтобы скрипт работал в текущем окружении без `sudo`.

```bash
cd /home/sergey/Sveton/07_forms
python3 -m pip install --upgrade pip
python3 -m pip install --target .deps -r requirements.txt
```

## Переменные окружения

Для Yandex Forms скрипт ожидает:

- `YANDEX_FORMS_TOKEN`
- `YANDEX_FORMS_ORG_ID`

Для Nextcloud Forms скрипт ожидает:

- `NEXTCLOUD_BASE_URL`
- `NEXTCLOUD_USER`
- `NEXTCLOUD_APP_PASSWORD`

Если в YAML указан `nextcloudForms.baseUrl`, скрипт использует этот хост вместо `NEXTCLOUD_BASE_URL`. Для анкеты электриков целевой хост зафиксирован как `https://nc.domibp.ru`, чтобы форма не создавалась на стороннем Nextcloud из старых переменных окружения.

Пример для текущей сессии:

```bash
export YANDEX_FORMS_TOKEN="your_oauth_token"
export YANDEX_FORMS_ORG_ID="940878"
export NEXTCLOUD_BASE_URL="https://example.nextcloud.host"
export NEXTCLOUD_USER="user"
export NEXTCLOUD_APP_PASSWORD="app-password"
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

## Nextcloud Forms

Проверка спецификации:

```bash
./create_nextcloud_form.py input/electrician_screening_form.yaml --dry-run
./create_nextcloud_form.py input/electrician_express_test_form.yaml --dry-run
```

Создание новой формы:

```bash
./create_nextcloud_form.py input/electrician_screening_form.yaml
```

Синхронизация уже созданной формы:

```bash
./create_nextcloud_form.py input/electrician_screening_form.yaml --form-id 1
./create_nextcloud_form.py input/electrician_express_test_form.yaml --form-id 2
```

Текущие Nextcloud Forms формы электриков:

- `Анкета электрика-монтажника.`:
  - хост: `https://nc.domibp.ru`;
  - форма ID: `1`;
  - публичная ссылка для кандидатов: `https://nc.domibp.ru/apps/forms/s/FqmceBkMsHLMi5Zx26t4bSWw`;
  - источник: `input/electrician_screening_form.yaml`.
- `Экспресс-тест электрика-монтажника.`:
  - хост: `https://nc.domibp.ru`;
  - форма ID: `2`;
  - публичная ссылка для кандидатов: `https://nc.domibp.ru/apps/forms/s/9WSyCCMFwqkqJZddK2bBrLGB`;
  - источник: `input/electrician_express_test_form.yaml`.

Скрипт создает публичный share для отправки ответов. Внутренняя ссылка вида `/apps/forms/<hash>/submit` может требовать авторизацию; кандидатам нужно отправлять публичную ссылку `/apps/forms/s/<share>`.

## Логотип Светона

Файл для загрузки в анкету:

- `/home/sergey/Sveton/07_forms/assets/sveton-logo.png`

Текущий API-скрипт не загружает логотип автоматически. После создания анкеты откройте `admin_url` из вывода скрипта и добавьте логотип в редакторе Yandex Forms вручную.

## Ручные настройки в Yandex Forms

После создания формы нужно вручную проверить в редакторе:

- логотип и цвета формы;
- обязательность вопросов;
- ограничения количества ответов для вопросов с пометкой `maxSelections`;
- порядок и визуальное разделение блоков;
- публикацию формы.

YAML-спецификация может хранить эти требования как служебные поля, но текущий API-скрипт применяет только создание формы и вопросов.

## Ручные настройки в Nextcloud Forms

После создания формы нужно проверить в редакторе:

- условный показ поля загрузки фото `q12_upload_photos`, если эта настройка доступна в текущей версии UI;
- ограничения количества вариантов для вопросов с `maxSelections`;
- визуальное оформление формы, если нужно отклониться от стандартной темы Nextcloud.
