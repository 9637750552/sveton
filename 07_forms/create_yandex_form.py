#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEPS_DIR = SCRIPT_DIR / ".deps"
if DEPS_DIR.exists():
    sys.path.insert(0, str(DEPS_DIR))

import requests
import yaml


FORMS_PUBLIC_API = "https://api.forms.yandex.net/v1"
DEFAULT_ORG_ID = "940878"

SUPPORTED_QUESTION_TYPES = {
    "multiple",
    "multiple_unique",
    "dropdown",
    "short",
    "long",
    "date",
    "file",
    "linearscale",
}

OPTION_BASED_TYPES = {"multiple", "multiple_unique", "dropdown"}
SPEC_FILE_SUFFIXES = (".yaml", ".yml", ".json")


class ConfigError(Exception):
    pass


class YandexFormsClient:
    def __init__(
        self,
        token: str,
        org_id: str,
        *,
        cloud_org: bool = False,
        timeout: int = 30,
        api_base: str = FORMS_PUBLIC_API,
    ) -> None:
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        org_header = "X-Cloud-Org-Id" if cloud_org else "X-Org-Id"
        self.session.headers.update(
            {
                "Authorization": f"OAuth {token}",
                org_header: org_id,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _request(self, method: str, path: str, *, payload: dict[str, Any] | None = None) -> Any:
        response = self.session.request(
            method=method,
            url=f"{self.api_base}{path}",
            json=payload,
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            raise RuntimeError(f"Yandex Forms API error: {response.status_code} {response.text}")
        if not response.content:
            return None
        return response.json()

    def check_access(self) -> dict[str, Any]:
        return self._request("GET", "/users/me/")

    def create_survey(self, spec: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "name": spec["title"],
            "texts": {
                "submit": spec.get("submitText", "Отправить"),
                "title": spec.get("thanksTitle", "Спасибо за ответы!"),
                "subtitle": spec.get("submissionMessage", "Ваши ответы приняты."),
            },
        }
        return self._request("POST", "/surveys/", payload=payload)

    def add_question(self, survey_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", f"/surveys/{survey_id}/questions/", payload=payload)

    def publish_survey(self, survey_id: str) -> None:
        self._request("POST", f"/surveys/{survey_id}/publish/")


def load_spec(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(content)
    elif suffix == ".json":
        data = json.loads(content)
    else:
        raise ConfigError(f"Unsupported file type: {path.suffix}. Use .yaml, .yml, or .json.")
    if not isinstance(data, dict):
        raise ConfigError("Form specification must be an object at the top level.")
    return data


def discover_spec_files() -> list[Path]:
    input_dir = SCRIPT_DIR / "input"
    if not input_dir.exists():
        return []
    return sorted(
        path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() in SPEC_FILE_SUFFIXES
    )


def choose_spec_interactively() -> Path:
    candidates = discover_spec_files()
    if not candidates:
        raise ConfigError(
            f"No form specification files found in {SCRIPT_DIR / 'input'}. Add a .yaml, .yml, or .json file first."
        )

    if not sys.stdin.isatty():
        options = "\n".join(f"- {path.relative_to(SCRIPT_DIR)}" for path in candidates)
        raise ConfigError(
            "Specification file is required in non-interactive mode. "
            "Pass a file path explicitly, for example:\n"
            "python3 create_yandex_form.py input/sveton_form_template.yaml\n"
            f"Available files:\n{options}"
        )

    print("Select a form specification:")
    for index, path in enumerate(candidates, start=1):
        print(f"{index}. {path.relative_to(SCRIPT_DIR)}")

    while True:
        raw_value = input("Enter number: ").strip()
        if not raw_value:
            print("Please enter a number.")
            continue
        if not raw_value.isdigit():
            print("Please enter a valid number.")
            continue

        selected_index = int(raw_value)
        if 1 <= selected_index <= len(candidates):
            return candidates[selected_index - 1]
        print(f"Please enter a number from 1 to {len(candidates)}.")


def validate_spec(spec: dict[str, Any]) -> None:
    title = spec.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ConfigError("Field 'title' is required and must be a non-empty string.")

    questions = spec.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ConfigError("Field 'questions' is required and must be a non-empty list.")

    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ConfigError(f"Question #{index} must be an object.")
        qtype = question.get("type")
        if qtype not in SUPPORTED_QUESTION_TYPES:
            raise ConfigError(f"Question #{index} has unsupported type '{qtype}' for Yandex Forms.")
        text = question.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ConfigError(f"Question #{index} must have non-empty 'text'.")
        if qtype in OPTION_BASED_TYPES:
            options = question.get("options")
            if not isinstance(options, list) or not options or not all(isinstance(item, str) and item.strip() for item in options):
                raise ConfigError(f"Question #{index} of type '{qtype}' must have a non-empty 'options' list of strings.")
        if qtype == "linearscale":
            settings = question.get("extraSettings", {})
            if not isinstance(settings, dict):
                raise ConfigError(f"Question #{index} field 'extraSettings' must be an object.")
        if "visibleIf" in question:
            visible_if = question["visibleIf"]
            if not isinstance(visible_if, dict):
                raise ConfigError(f"Question #{index} field 'visibleIf' must be an object.")
            condition_question = visible_if.get("question")
            condition_answer = visible_if.get("answer")
            if not isinstance(condition_question, str) or not condition_question.strip():
                raise ConfigError(f"Question #{index} field 'visibleIf.question' must be a non-empty string.")
            if not isinstance(condition_answer, str) or not condition_answer.strip():
                raise ConfigError(f"Question #{index} field 'visibleIf.answer' must be a non-empty string.")


def build_description_question(spec: dict[str, Any]) -> dict[str, Any] | None:
    description = spec.get("description")
    if not isinstance(description, str) or not description.strip():
        return None
    return {
        "type": "comment",
        "label": description.strip(),
        "header": False,
    }


def build_linear_scale_items(question: dict[str, Any]) -> list[dict[str, str]]:
    settings = question.get("extraSettings", {})
    lowest = int(settings.get("optionsLowest", 1))
    highest = int(settings.get("optionsHighest", 5))
    low_label = settings.get("optionsLabelLowest")
    high_label = settings.get("optionsLabelHighest")

    items: list[dict[str, str]] = []
    for value in range(lowest, highest + 1):
        label = str(value)
        if value == lowest and low_label:
            label = f"{value} - {low_label}"
        elif value == highest and high_label:
            label = f"{value} - {high_label}"
        items.append({"label": label})
    return items


def build_question_payload(question: dict[str, Any]) -> dict[str, Any]:
    qtype = question["type"]
    label = question["text"]

    if qtype == "short":
        payload: dict[str, Any] = {"type": "string", "label": label, "multiline": False}
    elif qtype == "long":
        payload = {"type": "string", "label": label, "multiline": True}
    elif qtype == "multiple_unique":
        payload = {
            "type": "enum",
            "label": label,
            "widget": "radio",
            "items": [{"label": option} for option in question["options"]],
        }
    elif qtype == "multiple":
        payload = {
            "type": "enum",
            "label": label,
            "widget": "checkbox",
            "items": [{"label": option} for option in question["options"]],
        }
    elif qtype == "dropdown":
        payload = {
            "type": "enum",
            "label": label,
            "widget": "select",
            "items": [{"label": option} for option in question["options"]],
        }
    elif qtype == "date":
        payload = {"type": "date", "label": label}
    elif qtype == "file":
        payload = {"type": "file", "label": label}
    elif qtype == "linearscale":
        payload = {
            "type": "enum",
            "label": label,
            "widget": "radio",
            "items": build_linear_scale_items(question),
        }
    else:
        raise ConfigError(f"Unsupported question type for Yandex Forms: {qtype}")

    return payload


def normalize_summary(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": spec["title"],
        "description": spec.get("description", ""),
        "question_count": len(spec["questions"]),
        "questions": [
            {
                "type": question["type"],
                "text": question["text"],
                "required": question.get("isRequired", False),
                "options_count": len(question.get("options", [])),
                "visible_if": question.get("visibleIf"),
            }
            for question in spec["questions"]
        ],
    }


def get_user_env_from_registry(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
            return str(value) if value else None
    except OSError:
        return None


def get_windows_env_from_wsl(name: str) -> str | None:
    if os.name == "nt":
        return None

    powershell = shutil.which("powershell.exe")
    if not powershell:
        return None

    try:
        result = subprocess.run(
            [
                powershell,
                "-NoProfile",
                "-Command",
                f'[Environment]::GetEnvironmentVariable("{name}","User")',
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    value = result.stdout.strip()
    return value or None


def get_env(name: str) -> str | None:
    return os.getenv(name) or get_user_env_from_registry(name) or get_windows_env_from_wsl(name)


def require_env(name: str) -> str:
    value = get_env(name)
    if value:
        return value
    raise ConfigError(f"Environment variable '{name}' is required.")


def create_form_from_spec(client: YandexFormsClient, spec: dict[str, Any], *, publish: bool = False) -> dict[str, Any]:
    survey = client.create_survey(spec)
    survey_id = survey["id"]

    created_questions: list[dict[str, Any]] = []
    description_question = build_description_question(spec)
    if description_question:
        created = client.add_question(survey_id, description_question)
        created_questions.append(
            {
                "id": created["id"],
                "type": "comment",
                "text": description_question["label"],
                "options_count": 0,
            }
        )

    for question in spec["questions"]:
        payload = build_question_payload(question)
        created = client.add_question(survey_id, payload)
        created_questions.append(
            {
                "id": created["id"],
                "type": created.get("type", payload["type"]),
                "text": question["text"],
                "options_count": len(question.get("options", [])),
            }
        )

    if publish:
        client.publish_survey(survey_id)

    required_count = sum(1 for question in spec["questions"] if question.get("isRequired"))
    warnings = []
    if required_count:
        warnings.append(
            "Yandex public API did not apply Nextcloud isRequired flags in verification; "
            f"check {required_count} required questions in the Yandex Forms editor before publishing."
        )
    conditional_count = sum(1 for question in spec["questions"] if question.get("visibleIf"))
    if conditional_count:
        warnings.append(
            "This source contains visibleIf conditions. The current script keeps them in the source "
            f"but does not apply {conditional_count} display condition(s) through the Yandex Forms API; "
            "set them in the Yandex Forms editor before publishing."
        )

    return {
        "id": survey_id,
        "name": survey["name"],
        "is_public": publish,
        "admin_url": f"https://forms.yandex.ru/cloud/admin/{survey_id}/edit",
        "questions": created_questions,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Yandex Form from a Nextcloud-style YAML or JSON specification.")
    parser.add_argument("spec", nargs="?", type=Path, help="Path to the form specification file.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print a summary without creating the form.")
    parser.add_argument("--publish", action="store_true", help="Publish the form after creating it.")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    parser.add_argument("--token", default=get_env("YANDEX_FORMS_TOKEN"), help="Yandex OAuth token. Defaults to YANDEX_FORMS_TOKEN.")
    parser.add_argument("--org-id", default=get_env("YANDEX_FORMS_ORG_ID") or DEFAULT_ORG_ID, help="Yandex organization ID.")
    parser.add_argument("--cloud-org", action="store_true", help="Use X-Cloud-Org-Id instead of X-Org-Id.")
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        spec_path = args.spec or choose_spec_interactively()
    except ConfigError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        spec = load_spec(spec_path)
        validate_spec(spec)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, ConfigError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "spec": str(spec_path.relative_to(SCRIPT_DIR) if spec_path.is_relative_to(SCRIPT_DIR) else spec_path),
                    "summary": normalize_summary(spec),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        token = args.token or require_env("YANDEX_FORMS_TOKEN")
        client = YandexFormsClient(
            token=token,
            org_id=args.org_id,
            cloud_org=args.cloud_org,
            timeout=args.timeout,
        )
        client.check_access()
        result = create_form_from_spec(client, spec, publish=args.publish)
    except (ConfigError, requests.RequestException, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"mode": "create", "spec": str(spec_path), "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
