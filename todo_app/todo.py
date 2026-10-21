import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todos.json"
PRIORITIES = ("high", "medium", "low")


def load_todos():
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE.name} is corrupted. Starting empty.")
        return []


def save_todos(todos):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)


def print_todos(todos, heading="Your Todos"):
    if not todos:
        print("No todos found.")
        return

    print(f"\n--- {heading} ---")
    for todo in todos:
        icon = "✓" if todo["completed"] else "○"
        priority = todo.get("priority", "medium").upper()
        due = f" | Due: {todo['due_date']}" if todo.get("due_date") else ""
        category = f" | Category: {todo['category']}" if todo.get("category") else ""
        print(f"{icon} [{todo['id']}] {todo['title']} | {priority}{due}{category}")
    print()


def find_todos(keyword):
    return [
        t for t in load_todos()
        if keyword.lower() in t["title"].lower()
    ]


def filter_by_priority(priority):
    return [
        t for t in load_todos()
        if t.get("priority", "medium") == priority
    ]


def filter_by_category(category):
    return [
        t for t in load_todos()
        if t.get("category", "").lower() == category.lower()
    ]


def add_todo(title, priority="medium", due_date=None, category=None):
    todos = load_todos()
    new_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({
        "id": new_id,
        "title": title,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "category": category,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_todos(todos)
    print(f"✓ Todo added: {title}")


def update_todo(todo_id, title=None, priority=None, due_date=None, category=None):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            if title:
                todo["title"] = title
            if priority:
                todo["priority"] = priority
            if due_date:
                todo["due_date"] = due_date
            if category:
                todo["category"] = category
            save_todos(todos)
            print(f"✓ Todo updated: {todo['title']}")
            return
    print(f"Todo with id {todo_id} not found.")


def set_completed(todo_id, completed=True):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = completed
            save_todos(todos)
            state = "completed" if completed else "incomplete"
            print(f"✓ Marked as {state}: {todo['title']}")
            return
    print(f"Todo with id {todo_id} not found.")


def delete_todo(todo_id):
    todos = load_todos()
    remaining = [t for t in todos if t["id"] != todo_id]
    if len(remaining) == len(todos):
        print(f"Todo with id {todo_id} not found.")
        return
    save_todos(remaining)
    print("✓ Todo deleted.")


def show_stats():
    todos = load_todos()
    total = len(todos)
    completed = sum(1 for t in todos if t["completed"])
    print("\n--- Todo Stats ---")
    print(f"Total: {total}")
    print(f"Completed: {completed}")
    print(f"Incomplete: {total - completed}")
    if total:
        print(f"Progress: {completed / total * 100:.1f}%")
    print()


def ask_priority(allow_skip=False):
    while True:
        hint = "Enter to skip" if allow_skip else "Enter = medium"
        value = input(f"Priority (high/medium/low, {hint}): ").strip().lower()
        if not value:
            return None if allow_skip else "medium"
        if value in PRIORITIES:
            return value
        print("Invalid priority.")


def ask_due_date():
    while True:
        value = input("Due date (YYYY-MM-DD, Enter to skip): ").strip()
        if not value:
            return None
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date format.")


def ask_id(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid id.")
        return None


def show_menu():
    print("\n=== Todo App ===")
    print("1. Add todo")
    print("2. View todos")
    print("3. Mark as completed")
    print("4. Mark as incomplete")
    print("5. Delete todo")
    print("6. Search todo")
    print("7. Filter by priority")
    print("8. Filter by category")
    print("9. Edit todo")
    print("10. Stats")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        match choice:
            case "1":
                title = input("Title: ").strip()
                if not title:
                    print("Title cannot be empty.")
                    continue
                add_todo(
                    title,
                    priority=ask_priority(),
                    due_date=ask_due_date(),
                    category=input("Category (optional): ").strip() or None,
                )

            case "2":
                print_todos(load_todos())

            case "3" | "4":
                print_todos(load_todos())
                todo_id = ask_id("Todo id: ")
                if todo_id is not None:
                    set_completed(todo_id, completed=(choice == "3"))

            case "5":
                print_todos(load_todos())
                todo_id = ask_id("Todo id to delete: ")
                if todo_id is not None:
                    delete_todo(todo_id)

            case "6":
                keyword = input("Search keyword: ").strip()
                if keyword:
                    print_todos(find_todos(keyword), f"Search: {keyword}")

            case "7":
                priority = input("Priority to filter: ").strip().lower()
                if priority in PRIORITIES:
                    print_todos(filter_by_priority(priority), f"Priority: {priority.upper()}")
                else:
                    print("Invalid priority.")

            case "8":
                category = input("Category to filter: ").strip()
                if category:
                    print_todos(filter_by_category(category), f"Category: {category}")

            case "9":
                print_todos(load_todos())
                todo_id = ask_id("Todo id to edit: ")
                if todo_id is None:
                    continue
                print("Press Enter to keep the current value.")
                update_todo(
                    todo_id,
                    title=input("New title: ").strip() or None,
                    priority=ask_priority(allow_skip=True),
                    due_date=ask_due_date(),
                    category=input("New category: ").strip() or None,
                )

            case "10":
                show_stats()

            case "0":
                print("Goodbye!")
                break

            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()
