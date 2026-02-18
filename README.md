# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes intelligent algorithmic features that go beyond basic task scheduling. These features make the system practical for real-world pet care scenarios.

### 🔍 Filtering Capabilities

The `Scheduler` class provides powerful filtering methods to segment tasks:

- **`filter_by_completion_status()`** - Separate completed from incomplete tasks
- **`filter_by_pet()`** - Get all tasks for a specific pet (case-insensitive name matching)
- **`filter_by_task_type()`** - Filter by type: walk, feeding, meds, grooming, enrichment, other
- **`filter_by_frequency()`** - Filter by recurrence: daily, weekly, as-needed
- **`filter_due_tasks()`** - Smart filtering based on recurrence logic and last completion date

All filters run in O(n) time and can be combined to create sophisticated task queries.

**Example:**
```python
scheduler = Scheduler(owner)
all_tasks = owner.get_all_incomplete_tasks()

# Get all feeding tasks for Max
max_tasks = scheduler.filter_by_pet(all_tasks, "Max")
feeding_tasks = scheduler.filter_by_task_type(max_tasks, "feeding")

# Get only tasks that are due today
due_today = scheduler.filter_due_tasks(all_tasks)
```

### 📊 Sorting Algorithms

Sort tasks to match different scheduling strategies:

- **`sort_by_duration()`** - Sort by time (ascending/descending)
  - Quick-win strategy: Shortest tasks first
  - Time-filling strategy: Longest tasks first
  - O(n log n) complexity using Python's Timsort

- **`sort_by_task_type()`** - Sort by logical daily routine order
  - Order: feeding → meds → walk → grooming → enrichment → other
  - Reflects typical pet care best practices
  - Creates natural schedule flow

**Example:**
```python
# Quick wins: tackle shortest tasks first
quick_wins = scheduler.sort_by_duration(all_tasks, ascending=True)

# Daily routine order
routine = scheduler.sort_by_task_type(all_tasks)
```

### 🔄 Recurring Task Automation

Tasks automatically recur based on their frequency using Python's `timedelta`:

- **Daily tasks**: When completed, a new instance is created with `due_date = today + 1 day`
- **Weekly tasks**: When completed, a new instance is created with `due_date = today + 7 days`
- **As-needed tasks**: Marked complete, no automatic recurrence

**Key Features:**
- Tasks track `last_completed` timestamp for recurrence calculation
- `Task.is_due()` method determines if a task should be scheduled based on frequency
- `complete_task_with_recurrence()` handles the full lifecycle automatically

**Example:**
```python
# Complete a daily feeding task
feeding_task = Task("Feed Max", 10, "daily", priority="high", task_type="feeding")
new_task = scheduler.complete_task_with_recurrence(feeding_task)

# Original task is marked complete
# new_task is automatically created and due tomorrow
```

### ⚠️ Conflict Detection

PawPal+ includes two types of conflict detection:

1. **Time Budget Conflicts** (`detect_time_conflicts()`)
   - Detects when total task duration exceeds available time
   - Provides overflow calculation and warning messages
   - Integrated into plan generation for upfront warnings

2. **Scheduling Conflicts** (`detect_scheduling_conflicts()`)
   - Detects overlapping time slots using interval overlap algorithm
   - O(n²) pairwise comparison of all scheduled tasks
   - Returns detailed conflict messages with task names, pets, and times

**Example:**
```python
# Create overlapping tasks
walk = Task("Walk Max", 30, "daily", scheduled_start_time=datetime(2025,1,15,8,0))
feed = Task("Feed Max", 10, "daily", scheduled_start_time=datetime(2025,1,15,8,15))

# Detect conflicts
conflicts = scheduler.detect_scheduling_conflicts([walk, feed])
if conflicts:
    print(conflicts[0]['message'])
    # "SCHEDULING CONFLICT: 'Walk Max' (Max) at 08:00 AM overlaps with 'Feed Max' (Max) at 08:15 AM"
```

### 🧠 Algorithm Complexity

All scheduling algorithms are designed for real-world performance:

- **Filtering**: O(n) - Linear scan through tasks
- **Sorting**: O(n log n) - Python's optimized Timsort
- **Conflict Detection**: O(n²) - Pairwise comparison (acceptable for typical pet care scenarios)
- **Plan Generation**: O(n log n) - Dominated by sorting step

The greedy scheduling approach prioritizes speed over perfect optimization, which is appropriate for daily pet care planning where "good enough" schedules are preferable to complex optimization delays.

## Testing PawPal+

### Running Tests

Run the comprehensive test suite using either command:

```bash
# Using pytest (recommended)
python -m pytest tests/test_pawpal.py -v

# Or run directly with Python
python tests/test_pawpal.py
```

### Test Coverage

The test suite includes **20 comprehensive tests** covering:

**Core Functionality:**
- ✅ Task completion and status tracking
- ✅ Pet-task relationship management
- ✅ Owner-pet hierarchy

**Sorting & Filtering:**
- ✅ Duration-based sorting (ascending/descending)
- ✅ Chronological sorting by scheduled time
- ✅ Task type sorting (daily routine order)
- ✅ Priority-based sorting with duration tie-breaker
- ✅ Filtering by completion status, pet, task type, and frequency

**Recurrence Logic:**
- ✅ Daily tasks auto-create next instance (+1 day)
- ✅ Weekly tasks auto-create next instance (+7 days)
- ✅ As-needed tasks do NOT auto-recur
- ✅ Due date calculation (is_due() logic)
- ✅ Error handling for invalid task operations

**Conflict Detection:**
- ✅ Time budget overflow detection
- ✅ Overlapping scheduled time slots
- ✅ Exact duplicate start times
- ✅ Adjacent tasks correctly identified as non-conflicting

**Edge Cases:**
- ✅ Empty owner (no pets)
- ✅ No incomplete tasks
- ✅ Zero time budget scenarios
- ✅ Task not found error handling

### Confidence Level: ⭐⭐⭐⭐ (4/5 Stars)

**Reliability Assessment:**

✅ **Strong Foundation** - All 20 tests pass consistently, covering critical scheduling behaviors

✅ **Algorithm Verification** - Core greedy scheduling, recurrence logic, and conflict detection thoroughly tested

✅ **Edge Case Handling** - Boundary conditions and error scenarios properly validated

⚠️ **Minor Gaps** - UI integration tests not yet implemented (Streamlit app layer untested)

⚠️ **Real-World Usage** - System is new and hasn't undergone extensive real-world usage patterns

**Recommendation:** The backend logic ([pawpal_system.py](pawpal_system.py)) is production-ready for pet care scheduling. The system reliably handles complex scenarios like multi-pet households, recurring tasks, and time conflicts. Consider adding integration tests for the Streamlit UI layer to achieve 5-star confidence.
