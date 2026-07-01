#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEPS_DIR = SCRIPT_DIR / ".deps"
if DEPS_DIR.exists():
    sys.path.insert(0, str(DEPS_DIR))

import requests
import yaml


SUPPORTED_QUESTION_TYPES = {
    "multiple",
    "multiple_unique",
    "dropdown",
    "short",
    "long",
    "date",
    "time",
    "file",
    "linearscale",
    "color",
    "ranking",
}

OPTION_BASED_TYPES = {"multiple", "multiple_unique", "dropdown", "ranking"}
SPEC_FILE_SUFFIXES = (".yaml", ".yml", ".json")

FORM_PATCH_FIELDS = {
    "title",
    "description",
    "submissionMessage",
    "expires",
    "isAnonymous",
    "submitMultiple",
    "allowEditSubmissions",
    "showExpiration",
    "access",
    "confirmationEmailEnabled",
    "confirmationEmailSubject",
    "confirmationEmailBody",
    "confirmationEmailQuestionId",
    "state",
}

QUESTION_PATCH_FIELDS = {
    "type",
    "text",
    "name",
    "description",
    "isRequired",
    "extraSettings",
    "accept",
}


class ConfigError(Exception):
    pass


class NextcloudFormsClient:
    def __init__(self, base_url: str, user: str, password: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.headers.update(
            {
                "OCS-APIRequest": "true",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.api_style = "v3"

    def _request(self, method: str, path: str, *, params: dict[str, Any] | None = None, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/ocs/v2.php/apps/forms{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        body = response.json()
        meta = body.get("ocs", {}).get("meta", {})
        if meta.get("status") != "ok":
            raise RuntimeError(f"Nextcloud API error: {meta.get('statuscode')} {meta.get('message')}")
        return body["ocs"]["data"]

    def check_access(self) -> None:
        try:
            self._request("GET", "/api/v3/forms")
            self.api_style = "v3"
        except requests.HTTPError as exc:
            if exc.response is None or exc.response.status_code not in {400, 404}:
                raise
            self._request("GET", "/api/v2.4/forms")
            self.api_style = "v2.4"

    def create_form(self, from_id: int | None = None) -> dict[str, Any]:
        if self.api_style == "v2.4":
            if from_id is not None:
                return self._request("POST", f"/api/v2.4/form/clone/{from_id}")
            return self._request("POST", "/api/v2.4/form")

        params = {"fromId": from_id} if from_id is not None else None
        return self._request("POST", "/api/v3/forms", params=params)

    def get_form(self, form_id: int) -> dict[str, Any]:
        if self.api_style == "v2.4":
            return self._request("GET", f"/api/v2.4/form/{form_id}")
        return self._request("GET", f"/api/v3/forms/{form_id}")

    def patch_form(self, form_id: int, key_value_pairs: dict[str, Any]) -> Any:
        if self.api_style == "v2.4":
            return self._request("PATCH", "/api/v2.4/form/update", payload={"id": form_id, "keyValuePairs": key_value_pairs})
        return self._request("PATCH", f"/api/v3/forms/{form_id}", payload={"keyValuePairs": key_value_pairs})

    def create_question(self, form_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        if self.api_style == "v2.4":
            legacy_payload = {
                "formId": form_id,
                "type": payload["type"],
            }
            if "text" in payload:
                legacy_payload["text"] = payload["text"]
            return self._request("POST", "/api/v2.4/question", payload=legacy_payload)
        return self._request("POST", f"/api/v3/forms/{form_id}/questions", payload=payload)

    def patch_question(self, form_id: int, question_id: int, key_value_pairs: dict[str, Any]) -> Any:
        if self.api_style == "v2.4":
            return self._request("PATCH", "/api/v2.4/question/update", payload={"id": question_id, "keyValuePairs": key_value_pairs})
        return self._request(
            "PATCH",
            f"/api/v3/forms/{form_id}/questions/{question_id}",
            payload={"keyValuePairs": key_value_pairs},
        )

    def delete_question(self, form_id: int, question_id: int) -> Any:
        if self.api_style == "v2.4":
            return self._request("DELETE", f"/api/v2.4/question/{question_id}")
        return self._request("DELETE", f"/api/v3/forms/{form_id}/questions/{question_id}")

    def create_options(self, form_id: int, question_id: int, option_texts: list[str]) -> list[dict[str, Any]]:
        if self.api_style == "v2.4":
            created_options: list[dict[str, Any]] = []
            for option_text in option_texts:
                created = self._request(
                    "POST",
                    "/api/v2.4/option",
                    payload={"questionId": question_id, "text": option_text, "optionType": "choice"},
                )
                created_options.append(created)
            return created_options
        return self._request(
            "POST",
            f"/api/v3/forms/{form_id}/questions/{question_id}/options",
            payload={"optionTexts": option_texts, "optionType": "choice"},
        )

    def patch_option(self, form_id: int, question_id: int, option_id: int, key_value_pairs: dict[str, Any]) -> Any:
        if self.api_style == "v2.4":
            return self._request(
                "PATCH",
                "/api/v2.4/option/update",
                payload={"id": option_id, "keyValuePairs": key_value_pairs},
            )
        return self._request(
            "PATCH",
            f"/api/v3/forms/{form_id}/questions/{question_id}/options/{option_id}",
            payload={"keyValuePairs": key_value_pairs},
        )

    def delete_option(self, form_id: int, question_id: int, option_id: int) -> Any:
        if self.api_style == "v2.4":
            return self._request("DELETE", f"/api/v2.4/option/{option_id}")
        return self._request("DELETE", f"/api/v3/forms/{form_id}/questions/{question_id}/options/{option_id}")

    def create_public_share(self, form_id: int) -> dict[str, Any] | None:
        if self.api_style == "v2.4":
            return None
        return self._request(
            "POST",
            f"/api/v3/forms/{form_id}/shares",
            payload={"shareType": "3", "shareWith": "", "permissions": ["submit"]},
        )


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
            f"No form specification files found in {Path(__file__).resolve().parent / 'input'}. "
            "Add a .yaml, .yml, or .json file first."
        )

    if not sys.stdin.isatty():
        options = "\n".join(f"- {path}" for path in candidates)
        raise ConfigError(
            "Specification file is required in non-interactive mode. "
            "Pass a file path explicitly, for example:\n"
            "python3 create_nextcloud_form.py input/electrician_screening_form.yaml\n"
            f"Available files:\n{options}"
        )

    print("Select a form specification:")
    for index, path in enumerate(candidates, start=1):
        print(f"{index}. {path.relative_to(SCRIPT_DIR)}")

    while True:
        raw_value = input("Enter number: ").strip()
        if raw_value.isdigit():
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
            raise ConfigError(f"Question #{index} has unsupported type '{qtype}'.")
        text = question.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ConfigError(f"Question #{index} must have non-empty 'text'.")
        if qtype in OPTION_BASED_TYPES:
            options = question.get("options")
            if not isinstance(options, list) or not options or not all(isinstance(item, str) and item.strip() for item in options):
                raise ConfigError(f"Question #{index} of type '{qtype}' must have a non-empty 'options' list of strings.")
        if "options" in question and qtype not in OPTION_BASED_TYPES:
            options = question["options"]
            if options and qtype not in OPTION_BASED_TYPES:
                raise ConfigError(f"Question #{index} of type '{qtype}' does not use 'options'.")
        if "extraSettings" in question and not isinstance(question["extraSettings"], dict):
            raise ConfigError(f"Question #{index} field 'extraSettings' must be an object.")
        if "accept" in question:
            accept = question["accept"]
            if not isinstance(accept, list) or not all(isinstance(item, str) for item in accept):
                raise ConfigError(f"Question #{index} field 'accept' must be a list of strings.")
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
        if "maxSelections" in question:
            max_selections = question["maxSelections"]
            if not isinstance(max_selections, int) or max_selections < 1:
                raise ConfigError(f"Question #{index} field 'maxSelections' must be a positive integer.")


def build_form_patch(spec: dict[str, Any]) -> dict[str, Any]:
    patch: dict[str, Any] = {}
    for key in FORM_PATCH_FIELDS:
        if key in spec:
            patch[key] = spec[key]
    return patch


def build_question_patch(question: dict[str, Any]) -> dict[str, Any]:
    patch: dict[str, Any] = {}
    for key in QUESTION_PATCH_FIELDS:
        if key in question:
            patch[key] = question[key]
    raw_extra_settings = patch.get("extraSettings") or {}
    extra_settings = raw_extra_settings if isinstance(raw_extra_settings, dict) else {}
    extra_settings = dict(extra_settings)
    if "maxSelections" in question:
        extra_settings["optionsLimitMax"] = question["maxSelections"]
    else:
        extra_settings.pop("optionsLimitMax", None)
    patch["extraSettings"] = extra_settings
    return patch


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
                "max_selections": question.get("maxSelections"),
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


def build_warnings(spec: dict[str, Any], *, public_share: dict[str, Any] | None) -> list[str]:
    warnings: list[str] = []

    conditional_count = sum(1 for question in spec["questions"] if question.get("visibleIf"))
    if conditional_count:
        warnings.append(
            "This source contains visibleIf conditions. The current script validates them but does not apply "
            f"{conditional_count} display condition(s) through the Nextcloud Forms API; check conditional display in the editor."
        )

    limited_questions = sum(1 for question in spec["questions"] if question.get("maxSelections"))
    if limited_questions:
        warnings.append(
            f"Applied maxSelections as extraSettings.optionsLimitMax for {limited_questions} multiple-choice question(s); "
            "check the limits in the Nextcloud Forms editor before sending the link."
        )

    if public_share is None:
        warnings.append("Public share was not created automatically for this API style; check access in the editor.")

    return warnings


def get_spec_nextcloud_base_url(spec: dict[str, Any]) -> str | None:
    settings = spec.get("nextcloudForms")
    if not isinstance(settings, dict):
        return None
    base_url = settings.get("baseUrl")
    if isinstance(base_url, str) and base_url.strip():
        return base_url.strip()
    return None


def create_question_with_retry(
    client: NextcloudFormsClient,
    form_id: int,
    question: dict[str, Any],
    *,
    attempts: int = 6,
) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            return client.create_question(
                form_id,
                {
                    "type": question["type"],
                    "text": question["text"],
                },
            )
        except requests.HTTPError as exc:
            last_error = exc
            if exc.response is None or exc.response.status_code != 404:
                raise
            time.sleep(2 + attempt)

    assert last_error is not None
    raise last_error


def sync_questions_from_spec(client: NextcloudFormsClient, form_id: int, spec: dict[str, Any]) -> list[dict[str, Any]]:
    form = client.get_form(form_id)
    existing_questions = sorted(form.get("questions", []), key=lambda item: int(item.get("order", 0)))
    synced_questions: list[dict[str, Any]] = []

    for index, question in enumerate(spec["questions"]):
        existing_question = existing_questions[index] if index < len(existing_questions) else None
        if existing_question is None:
            existing_question = create_question_with_retry(client, form_id, question)

        question_id = int(existing_question["id"])
        question_patch = build_question_patch(question)
        if question_patch:
            client.patch_question(form_id, question_id, question_patch)

        option_texts = question.get("options", [])
        existing_option_texts = [
            str(option.get("text", "")).strip()
            for option in existing_question.get("options", [])
            if str(option.get("text", "")).strip()
        ]
        existing_options = existing_question.get("options", [])
        if existing_option_texts != option_texts:
            for option in existing_options:
                option_id = option.get("id")
                if isinstance(option_id, int):
                    client.delete_option(form_id, question_id, option_id)
            if option_texts:
                client.create_options(form_id, question_id, option_texts)
        elif option_texts:
            for option in existing_question.get("options", []):
                option_id = option.get("id")
                if isinstance(option_id, int) and option.get("optionType") != "choice":
                    client.patch_option(form_id, question_id, option_id, {"optionType": "choice"})

        synced_questions.append(
            {
                "id": question_id,
                "type": question["type"],
                "text": question["text"],
                "options_count": len(option_texts),
            }
        )

    for existing_question in reversed(existing_questions[len(spec["questions"]):]):
        client.delete_question(form_id, int(existing_question["id"]))

    return synced_questions


def create_form_from_spec(
    client: NextcloudFormsClient,
    spec: dict[str, Any],
    *,
    public: bool = True,
    form_id: int | None = None,
) -> dict[str, Any]:
    if form_id is None:
        form = client.create_form()
        form_id = int(form["id"])

        # Some deployments expose the form immediately for reads, but question
        # endpoints can briefly lag behind the form-create endpoint.
        time.sleep(2)
    else:
        form = client.get_form(form_id)

    form_hash = form["hash"]
    form_patch = build_form_patch(spec)
    if form_patch:
        client.patch_form(form_id, form_patch)

    created_questions = sync_questions_from_spec(client, form_id, spec)

    refreshed_form = client.get_form(form_id)
    existing_shares = refreshed_form.get("shares") or []
    public_share = None
    share_error = None
    if public:
        if existing_shares:
            public_share = existing_shares[0]
        else:
            try:
                public_share = client.create_public_share(form_id)
            except requests.RequestException as exc:
                share_error = str(exc)

    warnings = build_warnings(spec, public_share=public_share)
    if share_error:
        warnings.append(f"Public share API call failed: {share_error}. Create/check public access in the editor.")

    public_submit_url = None
    if public_share and public_share.get("shareWith"):
        public_submit_url = f"{client.base_url}/apps/forms/s/{public_share['shareWith']}"

    return {
        "id": form_id,
        "hash": form_hash,
        "submit_url": public_submit_url or f"{client.base_url}/apps/forms/{form_hash}/submit",
        "internal_submit_url": f"{client.base_url}/apps/forms/{form_hash}/submit",
        "questions": created_questions,
        "public_share": public_share,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a Nextcloud Form from a YAML or JSON file.")
    parser.add_argument("spec", nargs="?", type=Path, help="Path to the form specification file.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print a summary without creating the form.")
    parser.add_argument("--private", action="store_true", help="Do not create a public submit share.")
    parser.add_argument("--form-id", type=int, help="Update/sync an existing form instead of creating a new one.")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds.")
    parser.add_argument("--base-url", help="Nextcloud base URL. Defaults to nextcloudForms.baseUrl in the spec, then NEXTCLOUD_BASE_URL.")
    parser.add_argument("--user", help="Nextcloud username. Defaults to NEXTCLOUD_USER.")
    parser.add_argument("--app-password", help="Nextcloud app password. Defaults to NEXTCLOUD_APP_PASSWORD.")
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
        print(json.dumps({"mode": "dry-run", "spec": str(spec_path), "summary": normalize_summary(spec)}, ensure_ascii=False, indent=2))
        return 0

    try:
        base_url = args.base_url or get_spec_nextcloud_base_url(spec) or require_env("NEXTCLOUD_BASE_URL")
        user = args.user or require_env("NEXTCLOUD_USER")
        app_password = args.app_password or require_env("NEXTCLOUD_APP_PASSWORD")
        client = NextcloudFormsClient(base_url=base_url, user=user, password=app_password, timeout=args.timeout)
        client.check_access()
        result = create_form_from_spec(client, spec, public=not args.private, form_id=args.form_id)
    except (ConfigError, requests.RequestException, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"mode": "create", "spec": str(spec_path), "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
