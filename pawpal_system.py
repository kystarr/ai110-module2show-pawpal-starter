"""
PawPal+ System - Backend Logic Layer

This module contains all the core classes for the pet care scheduling system.

Design Note - Class Relationships:
    - Task: Represents a single activity with description, time, frequency, and completion status
    - Pet: Stores pet details and manages its own list of tasks
    - Owner: Manages multiple pets and provides access to all their tasks
    - Scheduler: The "Brain" that retrieves, organizes, and manages tasks across all pets

    This design uses composition: Pets contain Tasks, Owner contains Pets, and
    Scheduler operates on an Owner to generate optimized daily care plans.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class Pet:
    """Represents a pet with basic information and manages its own tasks."""

    def __init__(self, name: str, species: str, age: int, special_needs: Optional[str] = None):
        """Initialize a Pet with name, species, age, and optional special needs."""
        if not name or not name.strip():
            raise ValueError("Pet name cannot be empty")
        if age < 0:
            raise ValueError(f"Pet age cannot be negative: {age}")

        self.name = name
        self.species = species
        self.age = age
        self.special_needs = special_needs
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet's task list."""
        if task not in self.tasks:
            raise ValueError(f"Task '{task.description}' not found in {self.name}'s task list")
        self.tasks.remove(task)

    def get_all_tasks(self) -> list[Task]:
        """Returns all tasks for this pet (completed and incomplete)."""
        return self.tasks.copy()

    def get_incomplete_tasks(self) -> list[Task]:
        """Returns only incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> list[Task]:
        """Returns only completed tasks for this pet."""
        return [task for task in self.tasks if task.completed]

    def get_info(self) -> str:
        """Returns formatted pet information including task summary."""
        info = f"Pet: {self.name}\n"
        info += f"Species: {self.species}\n"
        info += f"Age: {self.age} years"
        if self.special_needs:
            info += f"\nSpecial needs: {self.special_needs}"

        task_count = len(self.tasks)
        incomplete_count = len(self.get_incomplete_tasks())
        info += f"\nTasks: {task_count} total ({incomplete_count} incomplete)"

        return info

    def __str__(self) -> str:
        """Returns a simple one-line description of the pet."""
        return f"{self.name} ({self.species}, {self.age}y, {len(self.tasks)} tasks)"


@dataclass
class Task:
    """Represents a single pet care activity with completion tracking."""

    description: str
    duration_minutes: int
    frequency: str  # "daily", "weekly", "as-needed"
    completed: bool = False
    priority: str = "medium"  # "low", "medium", or "high"
    task_type: str = "other"  # "walk", "feeding", "meds", "grooming", "enrichment", "other"

    VALID_PRIORITIES = {"low", "medium", "high"}
    VALID_TASK_TYPES = {"walk", "feeding", "meds", "grooming", "enrichment", "other"}
    VALID_FREQUENCIES = {"daily", "weekly", "as-needed"}
    PRIORITY_SCORES = {"high": 3, "medium": 2, "low": 1}

    def __post_init__(self):
        """Validates task attributes after initialization."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if self.duration_minutes <= 0:
            raise ValueError(f"Task duration must be positive: {self.duration_minutes}")
        if self.priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{self.priority}'. Must be one of: {self.VALID_PRIORITIES}")
        if self.task_type not in self.VALID_TASK_TYPES:
            raise ValueError(f"Invalid task_type '{self.task_type}'. Must be one of: {self.VALID_TASK_TYPES}")
        if self.frequency not in self.VALID_FREQUENCIES:
            raise ValueError(f"Invalid frequency '{self.frequency}'. Must be one of: {self.VALID_FREQUENCIES}")

    def mark_complete(self):
        """Marks this task as completed."""
        self.completed = True

    def mark_incomplete(self):
        """Marks this task as incomplete."""
        self.completed = False

    def get_priority_score(self) -> int:
        """Converts priority string to numeric value for sorting (3=high, 2=medium, 1=low)."""
        return self.PRIORITY_SCORES[self.priority]

    def __str__(self) -> str:
        """Returns a formatted task description with completion status."""
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.description} ({self.duration_minutes}min, {self.frequency}, {self.priority} priority)"


class Owner:
    """Represents the pet owner who manages multiple pets.

    The Owner class manages a collection of pets and provides access to all their tasks.
    Time management is handled by the Scheduler class.
    """

    def __init__(self, name: str, available_time_minutes: int):
        """Initialize an Owner with name and daily time budget for pet care."""
        if not name or not name.strip():
            raise ValueError("Owner name cannot be empty")
        if available_time_minutes < 0:
            raise ValueError(f"Available time cannot be negative: {available_time_minutes}")

        self.name = name
        self.available_time_minutes = available_time_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a pet to this owner's care."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet):
        """Removes a pet from this owner's care."""
        if pet not in self.pets:
            raise ValueError(f"Pet '{pet.name}' not found in {self.name}'s pet list")
        self.pets.remove(pet)

    def get_all_pets(self) -> list[Pet]:
        """Returns all pets owned by this owner."""
        return self.pets.copy()

    def get_all_tasks(self) -> list[Task]:
        """Returns all tasks across all pets (combined list)."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks

    def get_all_incomplete_tasks(self) -> list[Task]:
        """Returns all incomplete tasks across all pets."""
        all_incomplete = []
        for pet in self.pets:
            all_incomplete.extend(pet.get_incomplete_tasks())
        return all_incomplete

    def __str__(self) -> str:
        """Returns a simple one-line description of the owner."""
        return f"{self.name} ({len(self.pets)} pet{'s' if len(self.pets) != 1 else ''}, {self.available_time_minutes} min/day)"


# Helper functions for working with plan dictionaries

def display_plan(plan: dict) -> str:
    """Formats a plan dictionary for display with all details."""
    owner = plan['owner']
    pets_count = plan['pets_count']
    pets_str = f"{pets_count} pet{'s' if pets_count != 1 else ''}"

    output = f"=== Daily Plan for {owner.name} ({pets_str}) ===\n\n"

    if not plan['scheduled_tasks']:
        output += "No tasks scheduled.\n"
    else:
        output += "Scheduled Tasks:\n"
        for i, task in enumerate(plan['scheduled_tasks'], 1):
            output += f"  {i}. {task}\n"

    output += f"\nTime Summary:\n"
    output += f"  Total scheduled: {plan['total_time_minutes']} minutes\n"
    output += f"  Remaining time: {plan['remaining_time_minutes']} minutes\n"

    if plan['skipped_tasks']:
        output += f"\nSkipped Tasks ({len(plan['skipped_tasks'])}):\n"
        for task in plan['skipped_tasks']:
            output += f"  - {task}\n"

    output += f"\nReasoning:\n{plan['reasoning']}\n"

    return output


def get_plan_summary(plan: dict) -> str:
    """Returns a brief one-line summary of a plan."""
    task_count = len(plan['scheduled_tasks'])
    pets_count = plan['pets_count']
    return f"{task_count} task{'s' if task_count != 1 else ''} for {pets_count} pet{'s' if pets_count != 1 else ''}, {plan['total_time_minutes']} minutes"


class Scheduler:
    """The 'Brain' - retrieves, organizes, and manages tasks across all pets.

    The Scheduler works with an Owner and all their pets, using a greedy algorithm
    to prioritize and fit tasks into the available time budget. It handles incomplete
    tasks across all pets and generates optimized daily care plans.

    Algorithm Complexity: O(n log n) for sorting + O(n) for fitting = O(n log n) overall.
    Tradeoff: Greedy is fast but not optimal. A true optimal solution (0/1 knapsack) would be
    O(n × budget) but is overkill for this use case.
    """

    def __init__(self, owner: Owner):
        """Initialize a Scheduler for the given owner's pets and tasks."""
        self.owner = owner

    def generate_plan(self) -> dict:
        """Creates the daily schedule across all owner's pets using greedy algorithm."""
        # Edge case: no pets
        if not self.owner.pets:
            return {
                'owner': self.owner,
                'scheduled_tasks': [],
                'total_time_minutes': 0,
                'remaining_time_minutes': self.owner.available_time_minutes,
                'reasoning': "Owner has no pets to care for.",
                'skipped_tasks': [],
                'pets_count': 0
            }

        # Get all incomplete tasks from all pets
        all_tasks = self.owner.get_all_incomplete_tasks()

        # Edge case: no tasks to schedule
        if not all_tasks:
            return {
                'owner': self.owner,
                'scheduled_tasks': [],
                'total_time_minutes': 0,
                'remaining_time_minutes': self.owner.available_time_minutes,
                'reasoning': "No incomplete tasks to schedule.",
                'skipped_tasks': [],
                'pets_count': len(self.owner.pets)
            }

        # Edge case: no time available
        if self.owner.available_time_minutes == 0:
            return {
                'owner': self.owner,
                'scheduled_tasks': [],
                'total_time_minutes': 0,
                'remaining_time_minutes': 0,
                'reasoning': "Owner has no available time for pet care tasks.",
                'skipped_tasks': all_tasks.copy(),
                'pets_count': len(self.owner.pets)
            }

        # Step 1: Prioritize tasks (sort by priority score, highest first)
        sorted_tasks = self.prioritize_tasks(all_tasks)

        # Step 2: Fit tasks into available time
        selected_tasks = self.fit_tasks_to_time(sorted_tasks, self.owner.available_time_minutes)

        # Step 3: Calculate metrics
        total_time = sum(task.duration_minutes for task in selected_tasks)
        remaining_time = self.owner.available_time_minutes - total_time

        # Step 4: Determine which tasks were skipped
        skipped_tasks = [task for task in sorted_tasks if task not in selected_tasks]

        # Step 5: Build reasoning explanation
        reasoning = self.build_reasoning(selected_tasks, skipped_tasks)

        # Step 6: Create and return the plan as a dictionary
        return {
            'owner': self.owner,
            'scheduled_tasks': selected_tasks,
            'total_time_minutes': total_time,
            'remaining_time_minutes': remaining_time,
            'reasoning': reasoning,
            'skipped_tasks': skipped_tasks,
            'pets_count': len(self.owner.pets)
        }

    def prioritize_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sorts tasks by priority (highest first), then by duration (shorter first)."""
        # Sort by priority score (descending), then by duration (ascending) as tiebreaker
        return sorted(
            tasks,
            key=lambda task: (-task.get_priority_score(), task.duration_minutes)
        )

    def fit_tasks_to_time(self, sorted_tasks: list[Task], time_budget: int) -> list[Task]:
        """Selects which tasks fit in available time using greedy algorithm."""
        selected = []
        remaining_time = time_budget

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_time:
                selected.append(task)
                remaining_time -= task.duration_minutes

        return selected

    def build_reasoning(self, selected_tasks: list[Task], rejected_tasks: list[Task]) -> str:
        """Generates human-readable explanation text for scheduling decisions."""
        reasoning_parts = []

        # Overall strategy
        pet_names = [pet.name for pet in self.owner.pets]
        pets_str = ", ".join(pet_names) if len(pet_names) <= 3 else f"{len(pet_names)} pets"
        reasoning_parts.append(
            f"Scheduling strategy: Prioritize tasks by priority (high > medium > low) "
            f"across {pets_str}, then fit as many as possible into the "
            f"{self.owner.available_time_minutes}-minute time budget."
        )

        # What was scheduled
        if selected_tasks:
            reasoning_parts.append(
                f"\nScheduled {len(selected_tasks)} task(s):"
            )
            for task in selected_tasks:
                reasoning_parts.append(
                    f"  • {task.description} ({task.priority} priority, {task.duration_minutes} min)"
                )
        else:
            reasoning_parts.append("\nNo tasks could be scheduled.")

        # What was skipped and why
        if rejected_tasks:
            reasoning_parts.append(f"\nSkipped {len(rejected_tasks)} task(s) due to time constraints:")
            for task in rejected_tasks:
                reasoning_parts.append(
                    f"  • {task.description} ({task.priority} priority, {task.duration_minutes} min)"
                )

        return "\n".join(reasoning_parts)
