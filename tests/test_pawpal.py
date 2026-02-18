"""
Test suite for PawPal+ system.

Tests the core functionality of the pet care scheduling system.
"""

import sys
import os

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Pet, Task


def test_task_completion():
    """Test that calling mark_complete() changes the task's status."""
    print("\n=== Testing Task Completion ===")

    # Create a task (should start incomplete)
    task = Task(
        description="Feed the cat",
        duration_minutes=10,
        frequency="daily",
        priority="high",
        task_type="feeding"
    )

    # Verify task starts as incomplete
    assert task.completed == False, "Task should start as incomplete"
    print("PASS: Task starts as incomplete")

    # Mark task as complete
    task.mark_complete()

    # Verify task is now complete
    assert task.completed == True, "Task should be complete after mark_complete()"
    print("PASS: mark_complete() changes task status to complete")

    # Mark task as incomplete again
    task.mark_incomplete()

    # Verify task is now incomplete
    assert task.completed == False, "Task should be incomplete after mark_incomplete()"
    print("PASS: mark_incomplete() changes task status to incomplete")

    print("PASS: All task completion tests passed!\n")


def test_task_addition():
    """Test that adding a task to a Pet increases that pet's task count."""
    print("=== Testing Task Addition ===")

    # Create a pet
    pet = Pet("Mittens", "cat", 5)

    # Verify pet starts with 0 tasks
    initial_count = len(pet.get_all_tasks())
    assert initial_count == 0, f"Pet should start with 0 tasks, but has {initial_count}"
    print(f"PASS: Pet starts with {initial_count} tasks")

    # Add first task
    task1 = Task("Feed Mittens", 10, "daily", priority="high", task_type="feeding")
    pet.add_task(task1)

    # Verify task count increased to 1
    count_after_one = len(pet.get_all_tasks())
    assert count_after_one == 1, f"Pet should have 1 task, but has {count_after_one}"
    print(f"PASS: After adding 1 task, pet has {count_after_one} task")

    # Add second task
    task2 = Task("Play with Mittens", 15, "daily", priority="medium", task_type="enrichment")
    pet.add_task(task2)

    # Verify task count increased to 2
    count_after_two = len(pet.get_all_tasks())
    assert count_after_two == 2, f"Pet should have 2 tasks, but has {count_after_two}"
    print(f"PASS: After adding 2 tasks, pet has {count_after_two} tasks")

    # Add third task
    task3 = Task("Brush Mittens", 10, "weekly", priority="low", task_type="grooming")
    pet.add_task(task3)

    # Verify task count increased to 3
    count_after_three = len(pet.get_all_tasks())
    assert count_after_three == 3, f"Pet should have 3 tasks, but has {count_after_three}"
    print(f"PASS: After adding 3 tasks, pet has {count_after_three} tasks")

    print("PASS: All task addition tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("TESTING PAWPAL+ SYSTEM")
    print("=" * 60)

    try:
        test_task_completion()
        test_task_addition()

        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
