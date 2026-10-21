from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import json


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM

    @property
    def status_icon(self) -> str:
        return "✓" if self.completed else "○"


class TodoManager:
    def __init__(self, filename: str = "todos.oop.json"):
        self.file = Path(__file__).parent / filename
        self.todos: list[Todo] = self._load()

    def _load(self) -> list[Todo]:
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        return [Todo(**{**d, "priority": Priority(d["priority"])}) for d in data]

    def save(self) -> None:
        raw = [asdict(t) for t in self.todos]
        self.file.write_text(
            json.dumps(raw, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, title: str, priority: Priority = Priority.MEDIUM) -> Todo:
        if not title.strip():
            raise ValueError("Title cannot be empty")
        new_id = max((t.id for t in self.todos), default=0) + 1
        todo = Todo(id=new_id, title=title.strip(), priority=priority)
        self.todos.append(todo)
        self.save()
        return todo

    def find(self, todo_id: int) -> Todo | None:
        return next((t for t in self.todos if t.id == todo_id), None)

    def complete(self, todo_id: int, completed: bool = True) -> Todo | None:
        todo = self.find(todo_id)
        if todo is None:
            return None
        todo.completed = completed
        self.save()
        return todo

    def delete(self, todo_id: int) -> bool:
        todo = self.find(todo_id)
        if todo is None:
            return False
        self.todos.remove(todo)
        self.save()
        return True

    def search(self, keyword: str) -> list[Todo]:
        keyword = keyword.lower()
        return [t for t in self.todos if keyword in t.title.lower()]

    def __len__(self) -> int:
        return len(self.todos)

    def __iter__(self):
        return iter(self.todos)


if __name__ == "__main__":
    mgr = TodoManager()
    if len(mgr) == 0:
        mgr.add("Belajar decorator", Priority.HIGH)
        mgr.add("Belajar dataclass")
    for todo in mgr:
        print(f"{todo.status_icon} [{todo.id}] {todo.title} [{todo.priority.value}]")
    print(f"Total: {len(mgr)}")
