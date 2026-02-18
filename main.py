"""
PawPal+ Demo - Daily Pet Care Scheduler

This script demonstrates the PawPal+ system by creating an owner with multiple pets,
assigning tasks to each pet, and generating an optimized daily care schedule.
"""

from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler, display_plan, get_plan_summary


def main():
    print("=" * 60)
    print("PAWPAL+ DAILY PET CARE SCHEDULER")
    print("=" * 60)
    print()

    # Create the owner
    owner = Owner("Sarah", available_time_minutes=90)
    print(f"Owner: {owner}")
    print()

    # Create first pet: Max (dog)
    print("Creating pets and their tasks...")
    print("-" * 60)

    max_dog = Pet("Max", "dog", 7, special_needs="Needs medication for arthritis")

    # Add tasks for Max - INTENTIONALLY OUT OF ORDER
    # Adding: low priority first, then medium, then high (opposite of ideal)
    max_dog.add_task(Task(
        description="Brush Max's coat",
        duration_minutes=15,
        frequency="weekly",
        priority="low",
        task_type="grooming"
    ))

    max_dog.add_task(Task(
        description="Play fetch in backyard",
        duration_minutes=20,
        frequency="daily",
        priority="medium",
        task_type="enrichment"
    ))

    max_dog.add_task(Task(
        description="Morning walk",
        duration_minutes=30,
        frequency="daily",
        priority="high",
        task_type="walk"
    ))

    max_dog.add_task(Task(
        description="Give Max arthritis medication",
        duration_minutes=5,
        frequency="daily",
        priority="high",
        task_type="meds"
    ))

    max_dog.add_task(Task(
        description="Feed Max breakfast",
        duration_minutes=10,
        frequency="daily",
        priority="high",
        task_type="feeding"
    ))

    print(f"Pet 1: {max_dog}")
    print(f"  Tasks assigned: {len(max_dog.get_all_tasks())}")
    print()

    # Create second pet: Luna (cat)
    luna_cat = Pet("Luna", "cat", 3)

    # Add tasks for Luna - RANDOM ORDER (by duration)
    luna_cat.add_task(Task(
        description="Interactive play session",
        duration_minutes=15,
        frequency="daily",
        priority="medium",
        task_type="enrichment"
    ))

    luna_cat.add_task(Task(
        description="Feed Luna breakfast",
        duration_minutes=5,
        frequency="daily",
        priority="high",
        task_type="feeding"
    ))

    luna_cat.add_task(Task(
        description="Trim Luna's nails",
        duration_minutes=10,
        frequency="as-needed",
        priority="low",
        task_type="grooming"
    ))

    luna_cat.add_task(Task(
        description="Clean Luna's litter box",
        duration_minutes=10,
        frequency="daily",
        priority="medium",
        task_type="other"
    ))

    print(f"Pet 2: {luna_cat}")
    print(f"  Tasks assigned: {len(luna_cat.get_all_tasks())}")
    print()

    # Create third pet: Goldie (goldfish)
    goldie_fish = Pet("Goldie", "goldfish", 1)

    # Add tasks for Goldie - MIXED ORDER
    goldie_fish.add_task(Task(
        description="Clean algae from tank",
        duration_minutes=12,
        frequency="weekly",
        priority="low",
        task_type="other"
    ))

    goldie_fish.add_task(Task(
        description="Test water quality",
        duration_minutes=8,
        frequency="weekly",
        priority="medium",
        task_type="other"
    ))

    goldie_fish.add_task(Task(
        description="Feed Goldie",
        duration_minutes=2,
        frequency="daily",
        priority="high",
        task_type="feeding"
    ))

    goldie_fish.add_task(Task(
        description="Check water filter",
        duration_minutes=5,
        frequency="daily",
        priority="low",
        task_type="other"
    ))

    print(f"Pet 3: {goldie_fish}")
    print(f"  Tasks assigned: {len(goldie_fish.get_all_tasks())}")
    print()

    # Add all pets to the owner
    owner.add_pet(max_dog)
    owner.add_pet(luna_cat)
    owner.add_pet(goldie_fish)

    print(f"Total pets under {owner.name}'s care: {len(owner.get_all_pets())}")
    print(f"Total tasks across all pets: {len(owner.get_all_tasks())}")
    print(f"Incomplete tasks to schedule: {len(owner.get_all_incomplete_tasks())}")
    print()

    # Create scheduler and generate the daily plan
    print("=" * 60)
    print("GENERATING TODAY'S SCHEDULE...")
    print("=" * 60)
    print()

    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    # Display the complete plan
    print(display_plan(plan))

    # Show summary
    print("=" * 60)
    print(f"SCHEDULE SUMMARY: {get_plan_summary(plan)}")
    print("=" * 60)
    print()

    # Demonstrate filtering and sorting capabilities
    print("=" * 60)
    print("SORTING & FILTERING DEMO")
    print("=" * 60)
    print()

    # Get all tasks (unsorted, as added)
    all_tasks = owner.get_all_incomplete_tasks()
    print(f"Total incomplete tasks (unsorted, as added): {len(all_tasks)}")
    print()

    # 1. Sort by duration (shortest first)
    print("1. SORT BY DURATION (shortest to longest):")
    sorted_by_time = scheduler.sort_by_duration(all_tasks, ascending=True)
    for i, task in enumerate(sorted_by_time, 1):
        print(f"  {i}. {task.description} - {task.duration_minutes} min ({task.priority} priority)")
    print()

    # 2. Sort by duration (longest first)
    print("2. SORT BY DURATION (longest to shortest):")
    sorted_by_time_desc = scheduler.sort_by_duration(all_tasks, ascending=False)
    for i, task in enumerate(sorted_by_time_desc[:5], 1):  # Show top 5
        print(f"  {i}. {task.description} - {task.duration_minutes} min")
    print()

    # 3. Sort by task type (time-of-day logic)
    print("3. SORT BY TASK TYPE (feeding -> meds -> walk -> grooming -> enrichment -> other):")
    sorted_by_type = scheduler.sort_by_task_type(all_tasks)
    for i, task in enumerate(sorted_by_type, 1):
        print(f"  {i}. [{task.task_type.upper()}] {task.description}")
    print()

    # 4. Filter by pet
    print("4. FILTER BY PET:")
    for pet_name in ["Max", "Luna", "Goldie"]:
        pet_tasks = scheduler.filter_by_pet(all_tasks, pet_name)
        print(f"  {pet_name}: {len(pet_tasks)} tasks")
        for task in pet_tasks:
            print(f"    - {task.description} ({task.duration_minutes} min, {task.priority})")
    print()

    # 5. Filter by task type
    print("5. FILTER BY TASK TYPE:")
    for task_type in ["feeding", "meds", "walk", "grooming", "enrichment", "other"]:
        typed_tasks = scheduler.filter_by_task_type(all_tasks, task_type)
        if typed_tasks:
            print(f"  {task_type.upper()}: {len(typed_tasks)} tasks")
            for task in typed_tasks:
                print(f"    - {task.description}")
    print()

    # 6. Filter by frequency
    print("6. FILTER BY FREQUENCY:")
    for frequency in ["daily", "weekly", "as-needed"]:
        freq_tasks = scheduler.filter_by_frequency(all_tasks, frequency)
        print(f"  {frequency.upper()}: {len(freq_tasks)} tasks")
    print()

    # 7. Filter by completion status
    print("7. FILTER BY COMPLETION STATUS:")
    incomplete = scheduler.filter_by_completion_status(all_tasks, completed=False)
    completed_tasks = scheduler.filter_by_completion_status(all_tasks, completed=True)
    print(f"  Incomplete: {len(incomplete)} tasks")
    print(f"  Completed: {len(completed_tasks)} tasks")
    print()

    # Demonstrate task completion with automatic recurrence
    print("=" * 60)
    print("TASK COMPLETION & RECURRENCE DEMO")
    print("=" * 60)
    print()

    # Complete a task using the new recurrence feature
    if plan['scheduled_tasks']:
        # Get the first scheduled task (Feed Goldie - daily task)
        first_task = plan['scheduled_tasks'][0]
        print(f"Completing task: {first_task.description}")
        print(f"  Frequency: {first_task.frequency}")
        print(f"  Original due date: {first_task.due_date}")
        print()

        # Use the scheduler's recurrence method
        new_task = scheduler.complete_task_with_recurrence(first_task)

        if new_task:
            print(f"[OK] Task marked complete!")
            print(f"[OK] New instance automatically created for next occurrence:")
            print(f"  Description: {new_task.description}")
            print(f"  Due date: {new_task.due_date}")
            print(f"  Status: {new_task}")
            print()
        else:
            print(f"[OK] Task marked complete (no recurrence for as-needed tasks)")
            print()

        # Show updated task counts
        incomplete_now = len(owner.get_all_incomplete_tasks())
        print(f"Total incomplete tasks now: {incomplete_now}")
        print()

        # Complete a weekly task to show different recurrence
        print("Now completing a WEEKLY task...")
        weekly_tasks = scheduler.filter_by_frequency(all_tasks, "weekly")
        if weekly_tasks:
            weekly_task = weekly_tasks[0]
            print(f"Completing task: {weekly_task.description}")
            print(f"  Frequency: {weekly_task.frequency}")
            print()

            new_weekly = scheduler.complete_task_with_recurrence(weekly_task)
            if new_weekly:
                print(f"[OK] Weekly task marked complete!")
                print(f"[OK] New instance created with due date: {new_weekly.due_date}")
                print(f"  (7 days from now)")
                print()

        print(f"Final incomplete task count: {len(owner.get_all_incomplete_tasks())}")
        print()

    # Demonstrate scheduling conflict detection
    print("=" * 60)
    print("SCHEDULING CONFLICT DETECTION DEMO")
    print("=" * 60)
    print()

    # Create tasks with overlapping scheduled times
    print("Creating tasks with overlapping time slots...")
    print()

    # Task 1: Walk Max at 8:00 AM (30 minutes)
    morning_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    walk_task = Task(
        description="Walk Max",
        duration_minutes=30,
        frequency="daily",
        priority="high",
        task_type="walk",
        scheduled_start_time=morning_time
    )
    max_dog.add_task(walk_task)
    print(f"Task 1: {walk_task.description}")
    print(f"  Start time: {walk_task.scheduled_start_time.strftime('%I:%M %p')}")
    print(f"  End time: {walk_task.get_end_time().strftime('%I:%M %p')}")
    print()

    # Task 2: Feed Max at 8:15 AM (10 minutes) - OVERLAPS with walk!
    feed_time = datetime.now().replace(hour=8, minute=15, second=0, microsecond=0)
    feed_task = Task(
        description="Feed Max breakfast (scheduled)",
        duration_minutes=10,
        frequency="daily",
        priority="high",
        task_type="feeding",
        scheduled_start_time=feed_time
    )
    max_dog.add_task(feed_task)
    print(f"Task 2: {feed_task.description}")
    print(f"  Start time: {feed_task.scheduled_start_time.strftime('%I:%M %p')}")
    print(f"  End time: {feed_task.get_end_time().strftime('%I:%M %p')}")
    print()

    # Task 3: Play with Luna at 8:20 AM (15 minutes) - OVERLAPS with both!
    play_time = datetime.now().replace(hour=8, minute=20, second=0, microsecond=0)
    play_task = Task(
        description="Play with Luna",
        duration_minutes=15,
        frequency="daily",
        priority="medium",
        task_type="enrichment",
        scheduled_start_time=play_time
    )
    luna_cat.add_task(play_task)
    print(f"Task 3: {play_task.description}")
    print(f"  Start time: {play_task.scheduled_start_time.strftime('%I:%M %p')}")
    print(f"  End time: {play_task.get_end_time().strftime('%I:%M %p')}")
    print()

    # Task 4: Clean litter box at 9:00 AM (10 minutes) - NO OVERLAP
    clean_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    clean_task = Task(
        description="Clean litter box",
        duration_minutes=10,
        frequency="daily",
        priority="medium",
        task_type="other",
        scheduled_start_time=clean_time
    )
    luna_cat.add_task(clean_task)
    print(f"Task 4: {clean_task.description}")
    print(f"  Start time: {clean_task.scheduled_start_time.strftime('%I:%M %p')}")
    print(f"  End time: {clean_task.get_end_time().strftime('%I:%M %p')}")
    print()

    # Detect conflicts
    scheduled_tasks = [walk_task, feed_task, play_task, clean_task]
    conflicts = scheduler.detect_scheduling_conflicts(scheduled_tasks)

    print("=" * 60)
    print("CONFLICT DETECTION RESULTS")
    print("=" * 60)
    print()

    if conflicts:
        print(f"Found {len(conflicts)} scheduling conflict(s):\n")
        for i, conflict in enumerate(conflicts, 1):
            print(f"{i}. {conflict['message']}")
        print()
        print("WARNING: These tasks cannot be done at the same time!")
        print("Recommendation: Adjust scheduled times to avoid overlaps.")
    else:
        print("No scheduling conflicts detected!")
        print("All tasks can be completed without time slot overlaps.")
    print()


if __name__ == "__main__":
    main()
