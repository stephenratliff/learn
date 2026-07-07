"""
taskbook.py — A Python Learning Project
========================================
A fully functional command-line Task Manager that demonstrates
nearly every core feature of Python in one cohesive program.

Run it:  python taskbook.py
Quit:    type 'q' at any menu prompt

Concepts covered:
  - Variables, types, f-strings
  - Lists, dicts, sets, tuples
  - Control flow (if/elif/else, for, while, match/case)
  - Functions, *args, **kwargs, defaults
  - Classes, inheritance, @property
  - Dataclasses
  - Decorators
  - Generators & comprehensions
  - Exception handling
  - File I/O with JSON
  - Type hints
  - Context managers
  - The standard library (datetime, pathlib, functools, collections)
"""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — IMPORTS
# Python's standard library is huge. Import only what you need.
# ─────────────────────────────────────────────────────────────────────────────

import json                          # read/write JSON files
import functools                     # higher-order functions (wraps, reduce)
import datetime                      # dates and times
from pathlib import Path             # object-oriented file paths
from dataclasses import dataclass, field  # auto-generate __init__, __repr__
from typing import Optional          # for type hints like Optional[str]
from collections import Counter      # count occurrences in an iterable


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — CONSTANTS & MODULE-LEVEL VARIABLES
#
# UPPER_CASE names signal "don't change this". Python has no true constants;
# this is a naming convention from PEP 8.
# A set {} is unordered and only holds unique values — perfect for valid choices.
# ─────────────────────────────────────────────────────────────────────────────

DATA_FILE   = Path("tasks.json")          # pathlib.Path — smarter than a string
PRIORITIES  = {"low", "medium", "high"}   # set literal
PRIORITY_EMOJI = {                        # dict maps priority → display symbol
    "low":    "○",
    "medium": "◐",
    "high":   "●",
}

# A tuple of (label, colour_code) pairs — tuples are immutable, good for fixed data
COLOURS = (
    ("green",  "\033[92m"),
    ("yellow", "\033[93m"),
    ("red",    "\033[91m"),
    ("cyan",   "\033[96m"),
    ("reset",  "\033[0m"),
    ("bold",   "\033[1m"),
    ("dim",    "\033[2m"),
)
# Build a dict from the tuple using a dict comprehension
C = {name: code for name, code in COLOURS}


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — A DECORATOR
#
# A decorator is a function that wraps another function to extend its behaviour.
# The @syntax is shorthand: @log_errors above def f() is the same as f = log_errors(f)
# functools.wraps copies the original function's name and docstring onto wrapper.
# ─────────────────────────────────────────────────────────────────────────────

def log_errors(func):
    """Decorator: catch ValueError/KeyError and print them cleanly."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # *args  → collects extra positional args into a tuple
        # **kwargs → collects extra keyword args into a dict
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError) as e:
            # 'as e' binds the exception object to the name e
            print(f"  {C['red']}Error: {e}{C['reset']}")
        except Exception as e:
            # bare Exception catches everything — use sparingly
            print(f"  {C['red']}Unexpected error: {e}{C['reset']}")
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — A DATACLASS
#
# @dataclass auto-generates __init__, __repr__, and __eq__ from the field
# annotations. It's the modern Python way to write simple data-holding classes.
# field(default_factory=...) is used when the default is a mutable value
# like a list — you must NOT write tags: list = []  (that shares one list
# across all instances, a classic Python gotcha).
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Task:
    """Represents a single task."""

    title:    str                  # required — no default
    priority: str  = "medium"     # optional — has default
    done:     bool = False
    tags:     list = field(default_factory=list)   # safe mutable default
    created:  str  = field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d")
        # lambda: anonymous single-expression function
        # datetime.now().strftime formats the current date as "2026-03-18"
    )

    # ── Methods ────────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialize to a plain dict for JSON storage."""
        # vars(self) returns the instance's __dict__ — a shortcut to all fields
        return vars(self)

    @classmethod                          # @classmethod receives the class, not an instance
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize from a dict (e.g. loaded from JSON)."""
        return cls(**data)                # ** unpacks dict as keyword arguments

    def __str__(self) -> str:
        """Called by str() and print(). Human-readable representation."""
        # Multiline f-string — backslash continues the expression
        status = f"{C['green']}✓{C['reset']}" if self.done else f"{C['dim']}·{C['reset']}"
        priority_marker = PRIORITY_EMOJI.get(self.priority, "?")
        tag_str = "  " + " ".join(f"#{t}" for t in self.tags) if self.tags else ""
        return f"  {status} {priority_marker} {self.title}{tag_str}"

    def __repr__(self) -> str:
        """Called by repr(). Unambiguous, for debugging."""
        return f"Task(title={self.title!r}, priority={self.priority!r}, done={self.done})"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — A CLASS (with inheritance potential)
#
# This is a traditional class — more control than dataclass when you need
# custom logic in __init__, properties, class methods, etc.
# ─────────────────────────────────────────────────────────────────────────────

class TaskBook:
    """
    Manages a collection of Tasks.

    Demonstrates:
      - __init__, instance variables, class variables
      - @property (computed attribute)
      - @log_errors decorator on a method
      - Generator method (yield)
      - File I/O with context manager
      - Exception handling
    """

    # Class variable — shared by ALL instances of TaskBook
    _instance_count: int = 0

    def __init__(self, filepath: Path):
        # Instance variables — unique to each object
        self.filepath   = filepath
        self.tasks: list[Task] = []      # type hint: list of Task objects
        TaskBook._instance_count += 1
        self._load()                     # _ prefix = "private by convention"

    # ── Properties ─────────────────────────────────────────────────────────
    # @property lets you call book.stats instead of book.stats()
    # It looks like an attribute but runs code.

    @property
    def stats(self) -> dict:
        """Return a dict of summary statistics."""
        total = len(self.tasks)
        done  = sum(1 for t in self.tasks if t.done)   # generator expression
        by_priority = Counter(t.priority for t in self.tasks)
        all_tags = [tag for t in self.tasks for tag in t.tags]  # flatten list
        return {
            "total":       total,
            "done":        done,
            "pending":     total - done,
            "by_priority": dict(by_priority),
            "top_tags":    Counter(all_tags).most_common(5),
        }

    @property
    def count(self) -> int:
        return len(self.tasks)

    # ── Generator method ────────────────────────────────────────────────────
    # A generator uses 'yield' to produce values lazily (one at a time).
    # Callers iterate with: for task in book.pending():
    # Nothing is computed until the caller asks for the next item.

    def pending(self):
        """Yield tasks that are not yet done."""
        for task in self.tasks:
            if not task.done:
                yield task

    def by_priority(self, priority: str):
        """Yield tasks matching a given priority — generator expression form."""
        return (t for t in self.tasks if t.priority == priority)

    # ── CRUD operations ─────────────────────────────────────────────────────

    @log_errors   # decorator applied to this method
    def add(self, title: str, priority: str = "medium", tags: Optional[list] = None) -> Task:
        """Add a new task. Returns the created Task."""
        # Validate — raise ValueError to be caught by the decorator
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of {PRIORITIES}")

        # 'or []' is the idiomatic way to handle a None default for a mutable arg
        task = Task(title=title.strip(), priority=priority, tags=tags or [])
        self.tasks.append(task)
        self._save()
        return task

    @log_errors
    def complete(self, index: int) -> Task:
        """Mark task at index as done (1-based)."""
        task = self._get(index)
        task.done = True
        self._save()
        return task

    @log_errors
    def reopen(self, index: int) -> Task:
        """Mark task at done as pending."""
        task = self._get(index)
        task.done = False
        self._save()
        return task

    @log_errors
    def remove(self, index: int) -> Task:
        """Remove task at index (1-based). Returns the removed Task."""
        task = self._get(index)
        self.tasks.remove(task)   # removes by value (uses __eq__)
        self._save()
        return task

    def clear_done(self) -> int:
        """Remove all completed tasks. Returns count removed."""
        before = len(self.tasks)
        # List comprehension creates a NEW list — no mutation-while-iterating bug
        self.tasks = [t for t in self.tasks if not t.done]
        removed = before - len(self.tasks)
        if removed:
            self._save()
        return removed

    def search(self, query: str) -> list[Task]:
        """Return tasks whose title contains the query (case-insensitive)."""
        q = query.lower()
        return [t for t in self.tasks if q in t.title.lower()]

    def sorted_by(self, key: str = "priority") -> list[Task]:
        """Return tasks sorted by a field name."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        if key == "priority":
            # sorted() returns a new list; lambda extracts the sort key
            return sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 99))
        elif key == "title":
            return sorted(self.tasks, key=lambda t: t.title.lower())
        elif key == "date":
            return sorted(self.tasks, key=lambda t: t.created)
        else:
            raise ValueError(f"Unknown sort key: {key!r}")

    # ── Private helpers ──────────────────────────────────────────────────────

    def _get(self, index: int) -> Task:
        """Convert 1-based user index to 0-based list index, with bounds check."""
        # Walrus operator (:=) assigns and tests in one expression (Python 3.8+)
        if not (1 <= index <= len(self.tasks)):
            raise ValueError(f"Index {index} out of range (1–{len(self.tasks)}).")
        return self.tasks[index - 1]

    def _save(self) -> None:
        """Persist tasks to JSON file."""
        # Context manager: 'with open(...) as f' auto-closes the file
        with open(self.filepath, "w", encoding="utf-8") as f:
            # json.dump serialises a Python object to a JSON string in the file
            # [t.to_dict() for t in self.tasks]  — list comprehension
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def _load(self) -> None:
        """Load tasks from JSON file if it exists."""
        if not self.filepath.exists():
            return   # file hasn't been created yet — that's fine

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)          # parse JSON → Python list of dicts
            # Rebuild Task objects from the raw dicts
            self.tasks = [Task.from_dict(d) for d in raw]
        except json.JSONDecodeError:
            print(f"  {C['yellow']}Warning: {self.filepath} is corrupt — starting fresh.{C['reset']}")
            self.tasks = []


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — STANDALONE FUNCTIONS
#
# Not everything needs to be a method. Pure functions are easier to test.
# ─────────────────────────────────────────────────────────────────────────────

def display_tasks(tasks: list[Task], heading: str = "Tasks") -> None:
    """Print a numbered list of tasks with a heading."""
    print(f"\n  {C['bold']}{C['cyan']}{heading}{C['reset']}  ({len(tasks)} items)")
    print(f"  {'─' * 40}")

    if not tasks:
        print(f"  {C['dim']}(nothing here){C['reset']}")
    else:
        for i, task in enumerate(tasks, start=1):   # enumerate gives (index, value)
            num = f"{C['dim']}{i:2}.{C['reset']}"
            done_style = C['dim'] if task.done else ""
            print(f"{num} {done_style}{task}{C['reset']}")
    print()


def display_stats(stats: dict) -> None:
    """Pretty-print the stats dict."""
    print(f"\n  {C['bold']}Stats{C['reset']}")
    print(f"  {'─' * 40}")
    print(f"  Total:   {stats['total']}")
    print(f"  Done:    {C['green']}{stats['done']}{C['reset']}")
    print(f"  Pending: {C['yellow']}{stats['pending']}{C['reset']}")
    if stats["by_priority"]:
        print(f"  By priority: ", end="")
        # dict.items() yields (key, value) pairs
        pairs = [f"{k}={v}" for k, v in stats["by_priority"].items()]
        print("  |  ".join(pairs))
    if stats["top_tags"]:
        tag_list = ", ".join(f"#{tag}({n})" for tag, n in stats["top_tags"])
        print(f"  Top tags: {tag_list}")
    print()


def prompt(message: str, default: str = "") -> str:
    """
    Print a prompt and return the user's input stripped of whitespace.
    If the user hits Enter with no input, return the default.
    """
    hint = f" [{default}]" if default else ""
    raw = input(f"  {C['cyan']}{message}{hint}:{C['reset']} ").strip()
    return raw or default


def choose_priority() -> str:
    """Ask the user to pick a priority. Returns the chosen string."""
    while True:
        raw = prompt("Priority (low / medium / high)", default="medium").lower()
        if raw in PRIORITIES:
            return raw
        print(f"  {C['yellow']}Please enter low, medium, or high.{C['reset']}")


def parse_tags(raw: str) -> list[str]:
    """
    Parse a comma-separated tag string into a cleaned list.
    '  work, home , urgent ' → ['work', 'home', 'urgent']
    """
    if not raw:
        return []
    # split, strip whitespace, lower-case, filter empty strings
    return [t.strip().lower() for t in raw.split(",") if t.strip()]


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — MAIN LOOP & MENU
#
# The main() function orchestrates the whole program.
# It uses a while loop, a dict-based menu dispatch, and match/case.
# ─────────────────────────────────────────────────────────────────────────────

MENU = """
  {bold}┌─ TaskBook ──────────────────────┐{reset}
  │  {cyan}a{reset}  Add a task                  │
  │  {cyan}l{reset}  List all tasks               │
  │  {cyan}p{reset}  List by priority             │
  │  {cyan}d{reset}  Mark done                    │
  │  {cyan}r{reset}  Reopen a task                │
  │  {cyan}x{reset}  Remove a task                │
  │  {cyan}c{reset}  Clear completed              │
  │  {cyan}s{reset}  Search                       │
  │  {cyan}t{reset}  Stats                        │
  │  {cyan}q{reset}  Quit                         │
  └──────────────────────────────────┘"""


def print_menu() -> None:
    print(MENU.format(**C))   # .format(**C) injects colour codes by name


def run_add(book: TaskBook) -> None:
    """Gather input and add a task."""
    title    = prompt("Task title")
    priority = choose_priority()
    tags_raw = prompt("Tags (comma-separated, optional)", default="")
    tags     = parse_tags(tags_raw)

    task = book.add(title, priority=priority, tags=tags)
    if task:
        print(f"  {C['green']}Added:{C['reset']} {task.title}")


def run_list(book: TaskBook) -> None:
    """List all tasks."""
    display_tasks(book.tasks, heading="All Tasks")


def run_list_by_priority(book: TaskBook) -> None:
    """List tasks sorted by priority."""
    display_tasks(book.sorted_by("priority"), heading="Tasks by Priority")


def run_complete(book: TaskBook) -> None:
    """Mark a task as done."""
    display_tasks(book.tasks)
    try:
        n = int(prompt("Task number to complete"))
    except ValueError:
        print(f"  {C['red']}Please enter a number.{C['reset']}")
        return
    task = book.complete(n)
    if task:
        print(f"  {C['green']}Done:{C['reset']} {task.title}")


def run_reopen(book: TaskBook) -> None:
    """Reopen a completed task."""
    done_tasks = [t for t in book.tasks if t.done]
    if not done_tasks:
        print(f"  {C['dim']}No completed tasks to reopen.{C['reset']}")
        return
    display_tasks(done_tasks, heading="Completed Tasks")
    try:
        n = int(prompt("Task number to reopen"))
    except ValueError:
        print(f"  {C['red']}Please enter a number.{C['reset']}")
        return
    task = book.reopen(n)
    if task:
        print(f"  {C['yellow']}Reopened:{C['reset']} {task.title}")


def run_remove(book: TaskBook) -> None:
    """Remove a task by number."""
    display_tasks(book.tasks)
    if not book.tasks:
        return
    try:
        n = int(prompt("Task number to remove"))
    except ValueError:
        print(f"  {C['red']}Please enter a number.{C['reset']}")
        return
    task = book.remove(n)
    if task:
        print(f"  {C['red']}Removed:{C['reset']} {task.title}")


def run_clear(book: TaskBook) -> None:
    """Clear all completed tasks after confirmation."""
    done_count = sum(1 for t in book.tasks if t.done)
    if done_count == 0:
        print(f"  {C['dim']}No completed tasks to clear.{C['reset']}")
        return
    confirm = prompt(f"Remove {done_count} completed task(s)? (y/n)", default="n")
    if confirm.lower() == "y":
        removed = book.clear_done()
        print(f"  {C['green']}Cleared {removed} task(s).{C['reset']}")


def run_search(book: TaskBook) -> None:
    """Search tasks by title."""
    q = prompt("Search for")
    if not q:
        return
    results = book.search(q)
    display_tasks(results, heading=f'Results for "{q}"')


def run_stats(book: TaskBook) -> None:
    """Show summary statistics."""
    display_stats(book.stats)


def main() -> None:
    """
    Entry point. Sets up the TaskBook and runs the interactive loop.

    The menu is a dict mapping command letters to handler functions.
    This is the 'dispatch table' pattern — cleaner than a long if/elif chain.
    """
    print(f"\n  {C['bold']}{C['cyan']}Welcome to TaskBook{C['reset']}")
    print(f"  Data file: {DATA_FILE.resolve()}\n")

    book = TaskBook(DATA_FILE)

    if book.count > 0:
        print(f"  Loaded {book.count} task(s).")
        display_tasks(book.tasks, heading="Current Tasks")
    else:
        print(f"  {C['dim']}No tasks yet. Type 'a' to add one.{C['reset']}")

    # Dict of  command_letter → handler_function
    # Functions are first-class objects — they can live in a dict.
    dispatch: dict[str, callable] = {
        "a": run_add,
        "l": run_list,
        "p": run_list_by_priority,
        "d": run_complete,
        "r": run_reopen,
        "x": run_remove,
        "c": run_clear,
        "s": run_search,
        "t": run_stats,
    }

    while True:            # infinite loop — we break on 'q'
        print_menu()
        choice = prompt("Command").lower()

        # match/case — Python 3.10+ structural pattern matching
        # (fall back to if/elif if you're on Python 3.9)
        match choice:
            case "q":
                print(f"\n  {C['green']}Goodbye!{C['reset']}\n")
                break
            case "" | "?":
                continue   # just redisplay the menu
            case cmd if cmd in dispatch:
                # Guard clause: only matches if cmd is a key in dispatch
                dispatch[cmd](book)   # call the handler, passing book
            case _:
                # Wildcard — matches anything not matched above
                print(f"  {C['yellow']}Unknown command '{choice}'. Press Enter to see the menu.{C['reset']}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — SCRIPT GUARD
#
# When Python runs a file directly, __name__ is set to "__main__".
# When a file is imported as a module, __name__ is the module name.
# This guard ensures main() only runs when the file is executed directly,
# not when it's imported by another script.
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
