from __future__ import annotations

import argparse
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mtc_filename_helper import (  # noqa: E402
    DEFAULT_DATE,
    build_resource_filename,
    build_student_filename,
)


class FilenameHelperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MTC Filename Helper")
        self.root.geometry("760x460")
        self.root.minsize(700, 420)

        self.mode_var = tk.StringVar(value="student")
        self.date_var = tk.StringVar(value=DEFAULT_DATE)
        self.document_type_var = tk.StringVar(value="Worksheet")
        self.unit_or_task_var = tk.StringVar(value="")
        self.extension_var = tk.StringVar(value="docx")
        self.surname_var = tk.StringVar(value="")
        self.first_name_var = tk.StringVar(value="")
        self.resource_title_var = tk.StringVar(value="Digital Literacy Activity")
        self.result_var = tk.StringVar(value="")

        self._build_ui()
        self._update_mode_fields()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        heading = ttk.Label(
            frame,
            text="MTC Filename Helper",
            font=("Arial", 18, "bold"),
        )
        heading.grid(row=0, column=0, columnspan=4, sticky="w")

        intro = ttk.Label(
            frame,
            text="Create audit-safe filenames for student records and teaching resources.",
            font=("Arial", 11),
        )
        intro.grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 16))

        mode_box = ttk.LabelFrame(frame, text="File Type", padding=12)
        mode_box.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(0, 14))

        ttk.Radiobutton(
            mode_box,
            text="Student file",
            value="student",
            variable=self.mode_var,
            command=self._update_mode_fields,
        ).grid(row=0, column=0, sticky="w", padx=(0, 20))
        ttk.Radiobutton(
            mode_box,
            text="Teaching resource or general file",
            value="resource",
            variable=self.mode_var,
            command=self._update_mode_fields,
        ).grid(row=0, column=1, sticky="w")

        labels = [
            ("Date", self.date_var),
            ("Document type", self.document_type_var),
            ("Unit or task", self.unit_or_task_var),
            ("Extension", self.extension_var),
            ("Student surname", self.surname_var),
            ("Student first name", self.first_name_var),
            ("Resource title", self.resource_title_var),
        ]

        self.entries: dict[str, ttk.Entry] = {}
        start_row = 3
        for index, (label_text, variable) in enumerate(labels):
            row = start_row + index
            label = ttk.Label(frame, text=label_text)
            label.grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(frame, textvariable=variable, width=48)
            entry.grid(row=row, column=1, columnspan=3, sticky="ew", pady=5)
            self.entries[label_text] = entry

        button_row = start_row + len(labels)
        buttons = ttk.Frame(frame)
        buttons.grid(row=button_row, column=0, columnspan=4, sticky="w", pady=(12, 12))

        ttk.Button(buttons, text="Generate Filename", command=self.generate).grid(
            row=0, column=0, padx=(0, 10)
        )
        ttk.Button(buttons, text="Copy Filename", command=self.copy_result).grid(
            row=0, column=1, padx=(0, 10)
        )
        ttk.Button(buttons, text="Reset Form", command=self.reset_form).grid(
            row=0, column=2
        )

        result_box = ttk.LabelFrame(frame, text="Generated Filename", padding=12)
        result_box.grid(row=button_row + 1, column=0, columnspan=4, sticky="nsew")

        result_entry = ttk.Entry(
            result_box,
            textvariable=self.result_var,
            font=("Menlo", 12),
        )
        result_entry.pack(fill="x", expand=True)

        help_text = (
            "Tip: Use student mode for assessment or evidence files. "
            "Use resource mode for worksheets, trainer notes, slides, and templates."
        )
        ttk.Label(frame, text=help_text, wraplength=700).grid(
            row=button_row + 2, column=0, columnspan=4, sticky="w", pady=(10, 0)
        )

        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(button_row + 1, weight=1)

    def _update_mode_fields(self) -> None:
        student_mode = self.mode_var.get() == "student"
        self.entries["Student surname"].configure(state="normal" if student_mode else "disabled")
        self.entries["Student first name"].configure(state="normal" if student_mode else "disabled")
        self.entries["Resource title"].configure(state="disabled" if student_mode else "normal")

    def reset_form(self) -> None:
        self.mode_var.set("student")
        self.date_var.set(DEFAULT_DATE)
        self.document_type_var.set("Worksheet")
        self.unit_or_task_var.set("")
        self.extension_var.set("docx")
        self.surname_var.set("")
        self.first_name_var.set("")
        self.resource_title_var.set("Digital Literacy Activity")
        self.result_var.set("")
        self._update_mode_fields()

    def generate(self) -> None:
        try:
            if self.mode_var.get() == "student":
                if not self.surname_var.get().strip() or not self.first_name_var.get().strip():
                    raise ValueError("Enter the student surname and first name.")
                filename = build_student_filename(
                    date_part=self.date_var.get().strip(),
                    surname=self.surname_var.get().strip(),
                    first_name=self.first_name_var.get().strip(),
                    document_type=self.document_type_var.get().strip() or "Worksheet",
                    unit_or_task=self.unit_or_task_var.get().strip(),
                    extension=self.extension_var.get().strip() or "docx",
                )
            else:
                if not self.resource_title_var.get().strip():
                    raise ValueError("Enter a resource title.")
                filename = build_resource_filename(
                    date_part=self.date_var.get().strip(),
                    resource_title=self.resource_title_var.get().strip(),
                    document_type=self.document_type_var.get().strip() or "Worksheet",
                    unit_or_task=self.unit_or_task_var.get().strip(),
                    extension=self.extension_var.get().strip() or "docx",
                )

            self.result_var.set(filename)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Filename Helper", str(exc))

    def copy_result(self) -> None:
        if not self.result_var.get().strip():
            self.generate()
        if not self.result_var.get().strip():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_var.get())
        self.root.update()
        messagebox.showinfo("Filename Helper", "Filename copied to clipboard.")


def run_self_test() -> None:
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
    parser = argparse.ArgumentParser(description="MTC Filename Helper desktop app.")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run a simple filename generation test without opening the app.",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return

    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    FilenameHelperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
