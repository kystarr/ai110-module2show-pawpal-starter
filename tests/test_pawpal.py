"""
Test suite for PawPal+ system.

Tests the core functionality of the pet care scheduling system.
"""

import sys
import os

# Add parent directory to path so we can import pawpal_system
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


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


def test_filter_by_completion_status():
    """Test filtering tasks by completed/incomplete status."""
    print("=== Testing Filter by Completion Status ===")

    owner = Owner("Test", 60)
    pet = Pet("Buddy", "dog", 5)

    task1 = Task("Task 1", 10, "daily")
    task2 = Task("Task 2", 10, "daily")
    task2.mark_complete()

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    incomplete = scheduler.filter_by_completion_status(all_tasks, completed=False)
    completed = scheduler.filter_by_completion_status(all_tasks, completed=True)

    assert len(incomplete) == 1, f"Should have 1 incomplete task, got {len(incomplete)}"
    assert len(completed) == 1, f"Should have 1 completed task, got {len(completed)}"
    assert task1 in incomplete, "task1 should be in incomplete list"
    assert task2 in completed, "task2 should be in completed list"

    print("PASS: Filter by completion status works correctly!\n")


def test_filter_by_pet():
    """Test filtering tasks by pet name."""
    print("=== Testing Filter by Pet ===")

    owner = Owner("Test", 60)
    pet1 = Pet("Max", "dog", 5)
    pet2 = Pet("Luna", "cat", 3)

    task1 = Task("Walk Max", 20, "daily")
    task2 = Task("Feed Luna", 5, "daily")

    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()

    max_tasks = scheduler.filter_by_pet(all_tasks, "Max")
    luna_tasks = scheduler.filter_by_pet(all_tasks, "Luna")

    assert len(max_tasks) == 1, f"Should have 1 task for Max, got {len(max_tasks)}"
    assert len(luna_tasks) == 1, f"Should have 1 task for Luna, got {len(luna_tasks)}"
    assert task1 in max_tasks, "task1 should be in Max's tasks"
    assert task2 in luna_tasks, "task2 should be in Luna's tasks"

    print("PASS: Filter by pet works correctly!\n")


def test_sort_by_duration():
    """Test sorting tasks by duration."""
    print("=== Testing Sort by Duration ===")

    owner = Owner("Test", 60)
    scheduler = Scheduler(owner)

    tasks = [
        Task("Long task", 30, "daily"),
        Task("Short task", 5, "daily"),
        Task("Medium task", 15, "daily")
    ]

    sorted_asc = scheduler.sort_by_duration(tasks, ascending=True)
    sorted_desc = scheduler.sort_by_duration(tasks, ascending=False)

    assert sorted_asc[0].duration_minutes == 5, "First task should be 5 minutes"
    assert sorted_asc[1].duration_minutes == 15, "Second task should be 15 minutes"
    assert sorted_asc[2].duration_minutes == 30, "Third task should be 30 minutes"

    assert sorted_desc[0].duration_minutes == 30, "First task (desc) should be 30 minutes"
    assert sorted_desc[2].duration_minutes == 5, "Last task (desc) should be 5 minutes"

    print("PASS: Sort by duration works correctly!\n")


def test_task_is_due_daily():
    """Test daily task due logic."""
    print("=== Testing Daily Task Due Logic ===")

    task = Task("Daily task", 10, "daily")

    # Never completed - should be due
    assert task.is_due() == True, "Never completed daily task should be due"

    # Completed today - not due yet
    task.last_completed = datetime.now()
    assert task.is_due() == False, "Task completed today should not be due"

    # Completed yesterday - due again
    task.last_completed = datetime.now() - timedelta(days=1)
    assert task.is_due() == True, "Task completed yesterday should be due"

    print("PASS: Daily task due logic works correctly!\n")


def test_task_is_due_weekly():
    """Test weekly task due logic."""
    print("=== Testing Weekly Task Due Logic ===")

    task = Task("Weekly task", 10, "weekly")

    # Never completed - should be due
    assert task.is_due() == True, "Never completed weekly task should be due"

    # Completed 3 days ago - not due yet
    task.last_completed = datetime.now() - timedelta(days=3)
    assert task.is_due() == False, "Task completed 3 days ago should not be due"

    # Completed 7 days ago - due again
    task.last_completed = datetime.now() - timedelta(days=7)
    assert task.is_due() == True, "Task completed 7 days ago should be due"

    print("PASS: Weekly task due logic works correctly!\n")


def test_detect_time_conflicts():
    """Test conflict detection when tasks exceed available time."""
    print("=== Testing Conflict Detection ===")

    owner = Owner("Test", 30)  # Only 30 minutes available
    pet = Pet("Buddy", "dog", 5)

    # Add tasks totaling 50 minutes (exceeds 30)
    pet.add_task(Task("Task 1", 20, "daily"))
    pet.add_task(Task("Task 2", 30, "daily"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    tasks = owner.get_all_incomplete_tasks()

    conflict = scheduler.detect_time_conflicts(tasks)

    assert conflict['has_conflict'] == True, "Should detect a conflict"
    assert conflict['total_required_minutes'] == 50, "Should require 50 minutes"
    assert conflict['available_minutes'] == 30, "Should have 30 minutes available"
    assert conflict['overflow_minutes'] == 20, "Should have 20 minutes overflow"

    print("PASS: Conflict detection works correctly!\n")


def test_recurring_task_daily():
    """Test that daily tasks automatically create new instance for next day."""
    print("=== Testing Daily Task Recurrence ===")

    pet = Pet("Buddy", "dog", 5)
    daily_task = Task("Feed Buddy", 10, "daily", priority="high", task_type="feeding")
    pet.add_task(daily_task)

    # Should have 1 incomplete task initially
    assert len(pet.get_incomplete_tasks()) == 1, "Should have 1 incomplete task initially"

    # Complete the task with recurrence
    new_task = pet.complete_recurring_task(daily_task)

    # Original task should be complete
    assert daily_task.completed == True, "Original task should be complete"

    # Should have created a new task
    assert new_task is not None, "Should create new task for daily frequency"
    assert new_task.description == daily_task.description, "New task should have same description"
    assert new_task.completed == False, "New task should be incomplete"

    # New task should have due date of tomorrow (within 1 day from now)
    assert new_task.due_date is not None, "New task should have a due date"
    time_until_due = (new_task.due_date - datetime.now()).total_seconds()
    assert 86000 < time_until_due < 87000, "Due date should be approximately 1 day from now"

    # Should now have 1 completed and 1 incomplete task
    assert len(pet.get_completed_tasks()) == 1, "Should have 1 completed task"
    assert len(pet.get_incomplete_tasks()) == 1, "Should have 1 incomplete task"
    assert len(pet.get_all_tasks()) == 2, "Should have 2 total tasks"

    print("PASS: Daily task recurrence works correctly!\n")


def test_recurring_task_weekly():
    """Test that weekly tasks automatically create new instance for next week."""
    print("=== Testing Weekly Task Recurrence ===")

    pet = Pet("Buddy", "dog", 5)
    weekly_task = Task("Groom Buddy", 20, "weekly", priority="low", task_type="grooming")
    pet.add_task(weekly_task)

    # Complete the task with recurrence
    new_task = pet.complete_recurring_task(weekly_task)

    # Should have created a new task
    assert new_task is not None, "Should create new task for weekly frequency"

    # New task should have due date 7 days from now
    assert new_task.due_date is not None, "New task should have a due date"
    time_until_due = (new_task.due_date - datetime.now()).total_seconds()
    # 7 days = 604800 seconds, allow some variance
    assert 604000 < time_until_due < 605000, "Due date should be approximately 7 days from now"

    # Should have 1 completed and 1 incomplete task
    assert len(pet.get_completed_tasks()) == 1, "Should have 1 completed task"
    assert len(pet.get_incomplete_tasks()) == 1, "Should have 1 incomplete task"

    print("PASS: Weekly task recurrence works correctly!\n")


def test_recurring_task_as_needed():
    """Test that as-needed tasks do NOT create new instances."""
    print("=== Testing As-Needed Task (No Recurrence) ===")

    pet = Pet("Luna", "cat", 3)
    as_needed_task = Task("Trim nails", 10, "as-needed", priority="low", task_type="grooming")
    pet.add_task(as_needed_task)

    # Complete the task with recurrence
    new_task = pet.complete_recurring_task(as_needed_task)

    # Should NOT create a new task for as-needed
    assert new_task is None, "Should NOT create new task for as-needed frequency"

    # Original task should be complete
    assert as_needed_task.completed == True, "Original task should be complete"

    # Should have only 1 task total (the completed one)
    assert len(pet.get_all_tasks()) == 1, "Should have only 1 task (no new instance created)"
    assert len(pet.get_completed_tasks()) == 1, "Should have 1 completed task"
    assert len(pet.get_incomplete_tasks()) == 0, "Should have 0 incomplete tasks"

    print("PASS: As-needed task correctly does NOT recur!\n")


def test_scheduler_complete_with_recurrence():
    """Test scheduler's complete_task_with_recurrence method."""
    print("=== Testing Scheduler Recurrence Method ===")

    owner = Owner("Test", 60)
    pet = Pet("Max", "dog", 5)
    task = Task("Walk Max", 30, "daily", priority="high", task_type="walk")
    pet.add_task(task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)

    # Complete task through scheduler
    new_task = scheduler.complete_task_with_recurrence(task)

    # Should create new task
    assert new_task is not None, "Scheduler should create new task for daily frequency"
    assert task.completed == True, "Original task should be complete"
    assert new_task.completed == False, "New task should be incomplete"

    # Check task counts through owner
    all_tasks = owner.get_all_tasks()
    incomplete_tasks = owner.get_all_incomplete_tasks()
    assert len(all_tasks) == 2, "Should have 2 total tasks"
    assert len(incomplete_tasks) == 1, "Should have 1 incomplete task"

    print("PASS: Scheduler recurrence method works correctly!\n")


def test_task_conflicts_detection():
    """Test detecting when two tasks have overlapping scheduled times."""
    print("=== Testing Task Conflict Detection ===")

    # Create tasks with scheduled times
    time1 = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    time2 = datetime.now().replace(hour=8, minute=15, second=0, microsecond=0)
    time3 = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

    # Task 1: 8:00 AM - 8:30 AM (30 minutes)
    task1 = Task("Walk dog", 30, "daily", scheduled_start_time=time1)

    # Task 2: 8:15 AM - 8:25 AM (10 minutes) - OVERLAPS with task1
    task2 = Task("Feed dog", 10, "daily", scheduled_start_time=time2)

    # Task 3: 9:00 AM - 9:15 AM (15 minutes) - NO OVERLAP
    task3 = Task("Play with cat", 15, "daily", scheduled_start_time=time3)

    # Test conflict detection
    assert task1.conflicts_with(task2) == True, "Task 1 should conflict with Task 2"
    assert task2.conflicts_with(task1) == True, "Task 2 should conflict with Task 1 (symmetric)"
    assert task1.conflicts_with(task3) == False, "Task 1 should NOT conflict with Task 3"
    assert task2.conflicts_with(task3) == False, "Task 2 should NOT conflict with Task 3"

    # Test get_end_time
    expected_end = time1 + timedelta(minutes=30)
    assert task1.get_end_time() == expected_end, "End time should be start + duration"

    print("PASS: Task conflict detection works correctly!\n")


def test_scheduler_conflict_detection():
    """Test scheduler's ability to detect all conflicts in a list of tasks."""
    print("=== Testing Scheduler Conflict Detection ===")

    owner = Owner("Test", 120)
    pet1 = Pet("Max", "dog", 5)
    pet2 = Pet("Luna", "cat", 3)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)

    # Create overlapping tasks
    time1 = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    time2 = datetime.now().replace(hour=8, minute=15, second=0, microsecond=0)
    time3 = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

    task1 = Task("Walk Max", 30, "daily", scheduled_start_time=time1)
    task2 = Task("Feed Max", 10, "daily", scheduled_start_time=time2)
    task3 = Task("Play with Luna", 15, "daily", scheduled_start_time=time3)

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    # Detect conflicts
    tasks = [task1, task2, task3]
    conflicts = scheduler.detect_scheduling_conflicts(tasks)

    # Should find 1 conflict (task1 and task2 overlap)
    assert len(conflicts) == 1, f"Should find 1 conflict, found {len(conflicts)}"
    assert conflicts[0]['task1'] == task1, "Conflict should involve task1"
    assert conflicts[0]['task2'] == task2, "Conflict should involve task2"
    assert "SCHEDULING CONFLICT" in conflicts[0]['message'], "Should have conflict message"

    print("PASS: Scheduler conflict detection works correctly!\n")


def test_sort_tasks_chronologically():
    """Test sorting tasks by scheduled start time in chronological order."""
    print("=== Testing Chronological Sorting ===")

    # Create tasks with different scheduled times
    time_morning = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
    time_noon = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    time_evening = datetime.now().replace(hour=18, minute=30, second=0, microsecond=0)
    time_night = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)

    # Create tasks in non-chronological order
    task_noon = Task("Lunch feeding", 10, "daily", scheduled_start_time=time_noon)
    task_night = Task("Evening play", 15, "daily", scheduled_start_time=time_night)
    task_morning = Task("Morning walk", 30, "daily", scheduled_start_time=time_morning)
    task_evening = Task("Dinner time", 10, "daily", scheduled_start_time=time_evening)

    tasks = [task_noon, task_night, task_morning, task_evening]

    # Sort chronologically (earliest first)
    sorted_tasks = sorted(tasks, key=lambda t: t.scheduled_start_time)

    # Verify chronological order
    assert sorted_tasks[0] == task_morning, "First task should be morning (7:00 AM)"
    assert sorted_tasks[1] == task_noon, "Second task should be noon (12:00 PM)"
    assert sorted_tasks[2] == task_evening, "Third task should be evening (6:30 PM)"
    assert sorted_tasks[3] == task_night, "Fourth task should be night (9:00 PM)"

    # Verify times are in ascending order
    for i in range(len(sorted_tasks) - 1):
        assert sorted_tasks[i].scheduled_start_time < sorted_tasks[i+1].scheduled_start_time, \
            f"Task {i} should be before task {i+1}"

    print("PASS: Tasks sorted chronologically in correct order!\n")


def test_sort_by_task_type():
    """Test sorting tasks by task type in logical daily routine order."""
    print("=== Testing Sort by Task Type ===")

    owner = Owner("Test", 120)
    scheduler = Scheduler(owner)

    # Create tasks with different types (in random order)
    tasks = [
        Task("Playtime", 15, "daily", task_type="enrichment"),
        Task("Morning walk", 30, "daily", task_type="walk"),
        Task("Give medication", 5, "daily", task_type="meds"),
        Task("Brush fur", 10, "daily", task_type="grooming"),
        Task("Feed breakfast", 10, "daily", task_type="feeding"),
        Task("Clean litter", 5, "daily", task_type="other")
    ]

    # Sort by task type
    sorted_tasks = scheduler.sort_by_task_type(tasks)

    # Verify order: feeding → meds → walk → grooming → enrichment → other
    assert sorted_tasks[0].task_type == "feeding", "First should be feeding"
    assert sorted_tasks[1].task_type == "meds", "Second should be meds"
    assert sorted_tasks[2].task_type == "walk", "Third should be walk"
    assert sorted_tasks[3].task_type == "grooming", "Fourth should be grooming"
    assert sorted_tasks[4].task_type == "enrichment", "Fifth should be enrichment"
    assert sorted_tasks[5].task_type == "other", "Last should be other"

    print("PASS: Tasks sorted by type in correct routine order!\n")


def test_prioritize_tasks():
    """Test that prioritize_tasks sorts by priority first, then duration as tiebreaker."""
    print("=== Testing Priority-Based Sorting ===")

    owner = Owner("Test", 120)
    scheduler = Scheduler(owner)

    # Create tasks with mixed priorities and durations
    tasks = [
        Task("Low priority long", 30, "daily", priority="low"),
        Task("High priority long", 25, "daily", priority="high"),
        Task("Medium priority short", 10, "daily", priority="medium"),
        Task("High priority short", 5, "daily", priority="high"),
        Task("Low priority short", 8, "daily", priority="low"),
        Task("Medium priority long", 20, "daily", priority="medium")
    ]

    # Use scheduler's prioritize method
    sorted_tasks = scheduler.prioritize_tasks(tasks)

    # Verify: high priority tasks come first
    assert sorted_tasks[0].priority == "high", "First task should be high priority"
    assert sorted_tasks[1].priority == "high", "Second task should be high priority"

    # Verify: among high priority, shorter duration comes first
    assert sorted_tasks[0].duration_minutes == 5, "Shortest high priority task first"
    assert sorted_tasks[1].duration_minutes == 25, "Longer high priority task second"

    # Verify: then medium priority
    assert sorted_tasks[2].priority == "medium", "Third task should be medium priority"
    assert sorted_tasks[3].priority == "medium", "Fourth task should be medium priority"

    # Verify: among medium priority, shorter duration comes first
    assert sorted_tasks[2].duration_minutes == 10, "Shorter medium priority task first"
    assert sorted_tasks[3].duration_minutes == 20, "Longer medium priority task second"

    # Verify: finally low priority
    assert sorted_tasks[4].priority == "low", "Fifth task should be low priority"
    assert sorted_tasks[5].priority == "low", "Sixth task should be low priority"

    # Verify: among low priority, shorter duration comes first
    assert sorted_tasks[4].duration_minutes == 8, "Shorter low priority task first"
    assert sorted_tasks[5].duration_minutes == 30, "Longer low priority task second"

    print("PASS: Tasks prioritized correctly with duration tiebreaker!\n")


def test_exact_duplicate_scheduled_times():
    """Test conflict detection when two tasks have identical start times."""
    print("=== Testing Exact Duplicate Scheduled Times ===")

    # Create two tasks with EXACTLY the same start time
    same_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)

    task1 = Task("Feed Max", 15, "daily", scheduled_start_time=same_time)
    task2 = Task("Feed Luna", 10, "daily", scheduled_start_time=same_time)

    # These should conflict (can't do both at exactly the same time)
    assert task1.conflicts_with(task2) == True, "Tasks with same start time should conflict"
    assert task2.conflicts_with(task1) == True, "Conflict should be symmetric"

    # Calculate expected end times
    end1 = same_time + timedelta(minutes=15)
    end2 = same_time + timedelta(minutes=10)

    assert task1.get_end_time() == end1, "Task 1 end time should be correct"
    assert task2.get_end_time() == end2, "Task 2 end time should be correct"

    print("PASS: Exact duplicate times correctly detected as conflicts!\n")


def test_adjacent_tasks_no_conflict():
    """Test that tasks scheduled back-to-back do NOT conflict."""
    print("=== Testing Adjacent Tasks (No Conflict) ===")

    # Create adjacent tasks: 8:00-8:30, then 8:30-9:00
    time1 = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    time2 = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)

    task1 = Task("Morning walk", 30, "daily", scheduled_start_time=time1)
    task2 = Task("Breakfast", 30, "daily", scheduled_start_time=time2)

    # Task 1 ends at 8:30, Task 2 starts at 8:30 - should NOT conflict
    assert task1.conflicts_with(task2) == False, "Adjacent tasks should NOT conflict"
    assert task2.conflicts_with(task1) == False, "Conflict check should be symmetric"

    # Verify end time of task1 equals start time of task2
    assert task1.get_end_time() == task2.scheduled_start_time, \
        "Task 1 should end exactly when Task 2 starts"

    print("PASS: Adjacent tasks correctly identified as non-conflicting!\n")


def test_recurring_task_not_found_error():
    """Test that completing a task not in pet's list raises ValueError."""
    print("=== Testing Recurring Task Not Found Error ===")

    owner = Owner("Test", 60)
    pet1 = Pet("Max", "dog", 5)
    pet2 = Pet("Luna", "cat", 3)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Create task and add to pet1
    task = Task("Walk Max", 30, "daily")
    pet1.add_task(task)

    scheduler = Scheduler(owner)

    # Try to complete the task through scheduler (should work)
    new_task = scheduler.complete_task_with_recurrence(task)
    assert new_task is not None, "Should successfully complete task in pet's list"

    # Create a task that doesn't belong to ANY pet
    orphan_task = Task("Orphan task", 10, "daily")

    # Try to complete orphan task - should raise ValueError
    try:
        scheduler.complete_task_with_recurrence(orphan_task)
        assert False, "Should have raised ValueError for task not in any pet's list"
    except ValueError as e:
        assert "not found in any pet's task list" in str(e), \
            "Error message should indicate task not found"
        print(f"  Correctly raised ValueError: {e}")

    # Try to complete task through wrong pet - should raise ValueError
    try:
        pet2.complete_recurring_task(task)  # task belongs to pet1, not pet2
        assert False, "Should have raised ValueError for task not in this pet's list"
    except ValueError as e:
        assert "not found" in str(e), "Error message should indicate task not found"
        print(f"  Correctly raised ValueError: {e}")

    print("PASS: Recurring task error handling works correctly!\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("TESTING PAWPAL+ SYSTEM")
    print("=" * 60)

    try:
        # Basic functionality tests
        test_task_completion()
        test_task_addition()
        test_filter_by_completion_status()
        test_filter_by_pet()

        # Sorting tests
        test_sort_by_duration()
        test_sort_tasks_chronologically()
        test_sort_by_task_type()
        test_prioritize_tasks()

        # Due date logic tests
        test_task_is_due_daily()
        test_task_is_due_weekly()

        # Time conflict detection
        test_detect_time_conflicts()

        # Recurrence tests
        test_recurring_task_daily()
        test_recurring_task_weekly()
        test_recurring_task_as_needed()
        test_scheduler_complete_with_recurrence()
        test_recurring_task_not_found_error()

        # Scheduling conflict tests
        test_task_conflicts_detection()
        test_scheduler_conflict_detection()
        test_exact_duplicate_scheduled_times()
        test_adjacent_tasks_no_conflict()

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
