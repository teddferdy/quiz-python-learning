import todo
from class_todo import Priority, TodoManager


def test_add_and_complete(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", tmp_path / "todos.json")
    todo.add_todo("Belajar pytest", priority="high")
    todo.set_completed(1)
    saved = todo.load_todos()
    assert saved[0]["completed"] is True
    assert saved[0]["priority"] == "high"


def test_search_is_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", tmp_path / "todos.json")
    todo.add_todo("Belajar Python")
    assert todo.find_todos("python")[0]["title"] == "Belajar Python"


def test_delete_missing_todo(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, "DATA_FILE", tmp_path / "todos.json")
    todo.add_todo("Satu")
    todo.delete_todo(99)
    assert len(todo.load_todos()) == 1


def test_manager_roundtrip_priority(tmp_path):
    path = str(tmp_path / "todos.json")
    manager = TodoManager(path)
    manager.add("Belajar OOP", Priority.HIGH)
    reloaded = TodoManager(path)
    assert reloaded.todos[0].priority is Priority.HIGH


def test_manager_complete_and_delete(tmp_path):
    manager = TodoManager(str(tmp_path / "todos.json"))
    manager.add("Task")
    assert manager.complete(1).completed is True
    assert manager.delete(1) is True
    assert len(manager) == 0
