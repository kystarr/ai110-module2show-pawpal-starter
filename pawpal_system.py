"""
PawPal+ System - Backend Logic Layer

This module contains all the core classes for the pet care scheduling system.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    """Represents a pet with basic information."""

    name: str
    species: str
    age: int
    special_needs: Optional[str] = None

    def get_info(self) -> str:
        """Returns formatted pet information."""
        pass

    def __str__(self) -> str:
        """String representation of the pet."""
        pass


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"
    task_type: str  # "walk", "feeding", "meds", "grooming", "enrichment", "other"
    preferred_time: Optional[str] = None  # "morning", "afternoon", "evening"

    def get_priority_score(self) -> int:
        """Converts priority string to numeric value for sorting.

        Returns:
            int: 3 for high, 2 for medium, 1 for low
        """
        pass

    def __str__(self) -> str:
        """Readable description of the task."""
        pass


class Owner:
    """Represents the pet owner and their constraints."""

    def __init__(self, name: str, available_time_minutes: int, preferences: Optional[dict] = None):
        """Initialize an Owner.

        Args:
            name: Owner's name
            available_time_minutes: Daily time budget for pet care
            preferences: Optional dictionary of owner preferences
        """
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or {}

    def has_time_for(self, task: Task) -> bool:
        """Checks if a task fits in remaining time budget.

        Args:
            task: The task to check

        Returns:
            bool: True if task duration fits in available time
        """
        pass

    def __str__(self) -> str:
        """String representation of the owner."""
        pass


class DailyPlan:
    """Represents the output schedule for a day."""

    def __init__(
        self,
        scheduled_tasks: list[Task],
        total_time_minutes: int,
        remaining_time_minutes: int,
        reasoning: str,
        skipped_tasks: Optional[list[Task]] = None
    ):
        """Initialize a DailyPlan.

        Args:
            scheduled_tasks: Tasks included in the plan, in order
            total_time_minutes: Sum of all task durations
            remaining_time_minutes: Unused time from owner's budget
            reasoning: Explanation of scheduling decisions
            skipped_tasks: Tasks that couldn't fit in the schedule
        """
        self.scheduled_tasks = scheduled_tasks
        self.total_time_minutes = total_time_minutes
        self.remaining_time_minutes = remaining_time_minutes
        self.reasoning = reasoning
        self.skipped_tasks = skipped_tasks or []

    def display(self) -> str:
        """Formats the plan for display.

        Returns:
            str: Formatted schedule as a string
        """
        pass

    def get_summary(self) -> str:
        """Returns a brief summary of the plan.

        Returns:
            str: Summary like "5 tasks, 120 minutes"
        """
        pass

    def add_task(self, task: Task) -> None:
        """Adds a task to the plan (if building incrementally).

        Args:
            task: The task to add
        """
        pass


class Scheduler:
    """Core logic for generating daily pet care plans."""

    def __init__(self, owner: Owner, pet: Pet, tasks: list[Task]):
        """Initialize a Scheduler.

        Args:
            owner: The pet owner with time constraints
            pet: The pet being cared for
            tasks: All available tasks to schedule
        """
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def generate_plan(self) -> DailyPlan:
        """Main method - creates the schedule.

        Returns:
            DailyPlan: The generated daily plan with scheduled tasks
        """
        pass

    def prioritize_tasks(self) -> list[Task]:
        """Sorts tasks by priority.

        Returns:
            list[Task]: Tasks sorted by priority (highest first)
        """
        pass

    def fit_tasks_to_time(self, sorted_tasks: list[Task], time_budget: int) -> list[Task]:
        """Selects which tasks fit in available time.

        Args:
            sorted_tasks: Tasks already sorted by priority
            time_budget: Available time in minutes

        Returns:
            list[Task]: Tasks that fit within the time budget
        """
        pass

    def build_reasoning(self, selected_tasks: list[Task], rejected_tasks: list[Task]) -> str:
        """Generates explanation text for scheduling decisions.

        Args:
            selected_tasks: Tasks included in the plan
            rejected_tasks: Tasks that couldn't be scheduled

        Returns:
            str: Human-readable explanation of the schedule
        """
        pass
