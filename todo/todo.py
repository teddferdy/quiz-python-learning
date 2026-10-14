import json
import os 
from datetime import datetime

DATA_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def search_todo(keyword): 
    todos = load_todos()
    results = [t for t in todos if keyword.lower() in t["title"].lower()]

    if not results:
        print(f"No todos found with '{keyword}'")
        return

    print(f"\n--- Search Results for '{keyword}' ---")
    for todo in results:
        status = "✓" if todo["completed"] else "○"
        print(f"{status} [{todo['id']}] {todo['title']}")
    print()

def filter_by_priority(priority):
    todos = load_todos()
    results = [t for t in todos if t.get("priority", "medium") == priority]
    
    if not results:
        print(f"No todos with priority '{priority}'")
        return
    
    print(f"\n--- Todos with priority: {priority.upper()} ---")
    for todo in results:
        status = "✓" if todo["completed"] else "○"
        print(f"{status} [{todo['id']}] {todo['title']}")
    print()

def view_todos():
    todos = load_todos()

    if not todos:
        print("No Todos Yet")
        return
    print("\n--- Your Todos ---")
    for todo in todos:
        status = "✓"  if todo["completed"] else "○"
        priority = todo.get("priority", "medium")
        due_date = todo.get("due_date", "")
        category = todo.get("category", "")

        due_info = f" | Due: {due_date}" if due_date else ""
        cat_info = f" | Category: {category}" if category else ""
        priority_info = f" | Priority: {priority.upper()}" 
        print(f"{status} [{todo['id']}] {todo['title']}{priority_info}{due_info}{cat_info}")
    print()


def save_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def delete_todo(id_todo):
    todos = load_todos()
    filtered_todos = [t for t in todos if t["id"] != id_todo]
    if len(filtered_todos) < len(todos):
        save_todos(filtered_todos)
        print(f"✓ Todo deleted")
    else:
        print(f"Todo with id {id_todo} not found")

def mark_completed(id_todo):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == id_todo:
            todo["completed"] = True
            save_todos(todos)
            print(f"✓ Marked as completed: {todo['title']}")
            return
    print(f"Todo with id {id_todo} not found")

def add_todo(title): 
    todos = load_todos()
    # Get priority
    print("Priority levels: high, medium, low")
    priority = input("Enter priority (default: medium): ").strip().lower()
    if priority not in ["high", "medium", "low"]:
        priority = "medium"
    
    # Get due date (optional)
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    if due_date:
        # Validate date format
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Setting due date to None.")
            due_date = None
    else:
        due_date = None
    
    # Get category (optional)
    category = input("Enter category (optional): ").strip()
    if not category:
        category = None
    
    todo = {
        "id": len(todos) + 1,
        "title": title,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "category": category,
        "created_at": datetime.now().isoformat()
    }
    todos.append(todo)
    save_todos(todos)
    print(f"✓ Todo added: {title}")

def show_menu():
    print("\n=== Todo App ===")
    print("1. Add todo")
    print("2. View todos")
    print("3. Mark as completed")
    print("4. Delete todo")
    print("5. Search todo")
    print("6. Filter by priority")
    print("7. Exit")
    print()


def main(): 
    while True:
        show_menu()
        choice = input("Choose An Option (1-5): ").lower().strip()

        if choice == "1":
            title = input("Enter A title").strip()
            if title:
                add_todo(title)
            else:
                print("Title cannot be empty")
        elif choice == "2":
            view_todos()
        elif choice == "3":
            view_todos()
            try:
                todo_id = int(input("Enter A id to Complete:"))
                mark_completed(todo_id)
            except ValueError:
                print("Invalid id")

        elif choice == "4":
            view_todos()

            try:
                todo_id = int(input("Enter A id to delete:"))
                delete_todo(todo_id)
            except ValueError:
                print("Invalid id")

        elif choice == "5":
            print("Goodbye!")
            break
        else: 
            print('Invalid option. Please try again.')

if __name__ == "__main__": 
    main()