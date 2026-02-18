"""
PawPal+ Demo - Daily Pet Care Scheduler

This script demonstrates the PawPal+ system by creating an owner with multiple pets,
assigning tasks to each pet, and generating an optimized daily care schedule.
"""

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

    # Add tasks for Max
    max_dog.add_task(Task(
        description="Morning walk",
        duration_minutes=30,
        frequency="daily",
        priority="high",
        task_type="walk"
    ))

    max_dog.add_task(Task(
        description="Feed Max breakfast",
        duration_minutes=10,
        frequency="daily",
        priority="high",
        task_type="feeding"
    ))

    max_dog.add_task(Task(
        description="Give Max arthritis medication",
        duration_minutes=5,
        frequency="daily",
        priority="high",
        task_type="meds"
    ))

    max_dog.add_task(Task(
        description="Play fetch in backyard",
        duration_minutes=20,
        frequency="daily",
        priority="medium",
        task_type="enrichment"
    ))

    max_dog.add_task(Task(
        description="Brush Max's coat",
        duration_minutes=15,
        frequency="weekly",
        priority="low",
        task_type="grooming"
    ))

    print(f"Pet 1: {max_dog}")
    print(f"  Tasks assigned: {len(max_dog.get_all_tasks())}")
    print()

    # Create second pet: Luna (cat)
    luna_cat = Pet("Luna", "cat", 3)

    # Add tasks for Luna
    luna_cat.add_task(Task(
        description="Feed Luna breakfast",
        duration_minutes=5,
        frequency="daily",
        priority="high",
        task_type="feeding"
    ))

    luna_cat.add_task(Task(
        description="Clean Luna's litter box",
        duration_minutes=10,
        frequency="daily",
        priority="medium",
        task_type="other"
    ))

    luna_cat.add_task(Task(
        description="Interactive play session",
        duration_minutes=15,
        frequency="daily",
        priority="medium",
        task_type="enrichment"
    ))

    luna_cat.add_task(Task(
        description="Trim Luna's nails",
        duration_minutes=10,
        frequency="as-needed",
        priority="low",
        task_type="grooming"
    ))

    print(f"Pet 2: {luna_cat}")
    print(f"  Tasks assigned: {len(luna_cat.get_all_tasks())}")
    print()

    # Create third pet: Goldie (goldfish)
    goldie_fish = Pet("Goldie", "goldfish", 1)

    # Add tasks for Goldie
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

    goldie_fish.add_task(Task(
        description="Test water quality",
        duration_minutes=8,
        frequency="weekly",
        priority="medium",
        task_type="other"
    ))

    goldie_fish.add_task(Task(
        description="Clean algae from tank",
        duration_minutes=12,
        frequency="weekly",
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

    # Demonstrate task completion
    print("=" * 60)
    print("TASK COMPLETION DEMO")
    print("=" * 60)
    print()

    # Mark some tasks as complete
    if plan['scheduled_tasks']:
        completed_task = plan['scheduled_tasks'][0]
        completed_task.mark_complete()
        print(f"Marked as complete: {completed_task}")
        print()

        # Show updated task counts
        print(f"Updated incomplete tasks: {len(owner.get_all_incomplete_tasks())}")
        print()


if __name__ == "__main__":
    main()
