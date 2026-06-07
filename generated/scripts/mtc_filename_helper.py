from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass
from datetime import date


DEFAULT_DATE = date.today().isoformat()
DEFAULT_PREFIX = ["MTC", "Redfern", "RED-01", "Pathway"]


def slugify(value: str, *, allow_underscores: bool = False) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.replace("&", " and ")
    value = value.strip()

    if allow_underscores:
        value = re.sub(r"[^A-Za-z0-9_-]+", "-", value)
    else:
        value = re.sub(r"[^A-Za-z0-9-]+", "-", value)

    value = re.sub(r"-{2,}", "-", value)
    value = value.strip("-_")
    return value


def clean_extension(value: str) -> str:
    value = value.strip().lower()
    if not value:
        return "docx"
    return value[1:] if value.startswith(".") else value


def prompt(label: str, default: str = "") -> str:
    shown = f" [{default}]" if default else ""
    value = input(f"{label}{shown}: ").strip()
    return value or default


@dataclass
class FilenameParts:
    date_part: str
    student_part: str | None
    document_type: str
    unit_or_task: str | None
    resource_title: str | None
    extension: str

    def build(self) -> str:
        parts = [self.date_part, *DEFAULT_PREFIX]

        if self.student_part:
            parts.append(self.student_part)

        if self.resource_title:
            parts.append(self.resource_title)

        parts.append(self.document_type)

        if self.unit_or_task:
            parts.append(self.unit_or_task)

        return "_".join(parts) + f".{self.extension}"


def build_student_filename(
    *,
    date_part: str,
    surname: str,
    first_name: str,
    document_type: str,
    unit_or_task: str,
    extension: str,
) -> str:
    student_part = f"{slugify(surname)}-{slugify(first_name)}"
    parts = FilenameParts(
        date_part=date_part,
        student_part=student_part,
        document_type=slugify(document_type, allow_underscores=True),
        unit_or_task=slugify(unit_or_task, allow_underscores=True) or None,
        resource_title=None,
        extension=clean_extension(extension),
    )
    return parts.build()


def build_resource_filename(
    *,
    date_part: str,
    resource_title: str,
    document_type: str,
    unit_or_task: str,
    extension: str,
) -> str:
    parts = FilenameParts(
        date_part=date_part,
        student_part=None,
        document_type=slugify(document_type, allow_underscores=True),
        unit_or_task=slugify(unit_or_task, allow_underscores=True) or None,
        resource_title=slugify(resource_title, allow_underscores=True) or None,
        extension=clean_extension(extension),
    )
    return parts.build()


def interactive_mode() -> str:
    print("MTC Filename Helper")
    print("1. Student file")
    print("2. Teaching resource or general file")
    choice = prompt("Choose 1 or 2", "1")

    date_part = slugify(prompt("Date", DEFAULT_DATE))
    document_type = prompt("Document type", "Worksheet")
    unit_or_task = prompt("Unit or task", "")
    extension = prompt("Extension", "docx")

    if choice == "1":
        surname = prompt("Student surname")
        first_name = prompt("Student first name")
        return build_student_filename(
            date_part=date_part,
            surname=surname,
            first_name=first_name,
            document_type=document_type,
            unit_or_task=unit_or_task,
            extension=extension,
        )

    resource_title = prompt("Resource title", "Digital Literacy Activity")
    return build_resource_filename(
        date_part=date_part,
        resource_title=resource_title,
        document_type=document_type,
        unit_or_task=unit_or_task,
        extension=extension,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create audit-compliant MTC filenames for student files and teaching resources."
    )
    parser.add_argument("--mode", choices=["student", "resource"], help="Filename type.")
    parser.add_argument("--date", default=DEFAULT_DATE, help="Date in YYYY-MM-DD format.")
    parser.add_argument("--document-type", help="Document type, for example PA-Comments or Worksheet.")
    parser.add_argument("--unit-or-task", default="", help="Unit code or task label.")
    parser.add_argument("--ext", default="docx", help="File extension, for example pdf or docx.")
    parser.add_argument("--surname", help="Student surname.")
    parser.add_argument("--first-name", help="Student first name.")
    parser.add_argument("--resource-title", help="Resource title for non-student files.")
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show example filenames and exit.",
    )
    return parser


def print_examples() -> None:
    print(
        build_student_filename(
            date_part="2026-06-07",
            surname="Williams",
            first_name="Mark",
            document_type="PA-Comments",
            unit_or_task="BSBTEC203",
            extension="docx",
        )
    )
    print(
        build_resource_filename(
            date_part="2026-06-07",
            resource_title="Canvas Phone Access",
            document_type="Student_Worksheet",
            unit_or_task="",
            extension="docx",
        )
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.examples:
        print_examples()
        return

    if not args.mode:
        print(interactive_mode())
        return

    date_part = slugify(args.date)
    document_type = args.document_type or "Worksheet"

    if args.mode == "student":
        if not args.surname or not args.first_name:
            parser.error("--surname and --first-name are required in student mode.")
        print(
            build_student_filename(
                date_part=date_part,
                surname=args.surname,
                first_name=args.first_name,
                document_type=document_type,
                unit_or_task=args.unit_or_task,
                extension=args.ext,
            )
        )
        return

    if not args.resource_title:
        parser.error("--resource-title is required in resource mode.")

    print(
        build_resource_filename(
            date_part=date_part,
            resource_title=args.resource_title,
            document_type=document_type,
            unit_or_task=args.unit_or_task,
            extension=args.ext,
        )
    )


if __name__ == "__main__":
    main()
