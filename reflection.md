# PawPal+ Project Reflection

## 1. System Design

1. Add/Manage Pet and Owner Information
Enter basic information about the pet owner (e.g., name, available time per day)
Enter basic information about their pet (e.g., name, type, age, special needs)

2. Add/Edit Pet Care Tasks
Create new tasks with details like:
Task type (walks, feeding, meds, enrichment, grooming, etc.)
Duration (how long each task takes)
Priority level (which tasks are most important)
Edit or modify existing tasks as needs change

3. Generate and View Daily Schedule
Generate a daily care plan based on:
Available time
Task priorities
Owner preferences and constraints
View the schedule clearly with reasoning/explanations for why tasks were scheduled in that order

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

There are five classes all stemming from the Scheduler Parent class. From there, the Scheduler class uses the Pet class, Owner class, creates the DailyPlan class, and manages the Task class. The Owner class has a Pet class, and the DailyPlan class contains the task class. Some responsibilites for each class include generate_plan() within the Scheduler class, has_time_for(task) within the Owner class, get_info() within the Pet class, add_task() within the DailyPlan class, and get_prioirity_score() responsibiliity within the Task class. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.


An extra class named DailyPlan was added in the UML diagram initially. It was removed to keep to the four classes instrudted to create in the project instructions. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Some constraints that Scheduler cosiders are task priority, budgeted time, task duration, completion status, and conflict awareness. These matter most bescause the amount of time owners have is limited, prioirity markings will help owners decide how to best take care of their pet, and duration will be used to imporve efficiency and ensure the schedule fits within the alloted time. 


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff that Scheduler makes is using a greedy algorithm instead of computing the mathematically optimal schedule. So, it'ss select tasks in prioirty order and adds them if they fit instead of ecploriing all possible combinations of tasks. One reason this tradeoff is reasonable because speed and effiecincy matter more than perfect optimality. Pet owners need quick and easy to understand schedules. Also, the schedules that are produced with this algorithm are still high quality. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools to help with each step in the project instructions, so designing the UML diagram, brainstorming, etc. I found that telling AI what the app is supposed to be doing, as well as which phase I was on and how it should be completed were helpful when prompt engineering.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

Once, when creating the final UML diagram, Claude wanted to make a markdown file instead of giving the code to paste into mermaid.live. I evaluated the file, then rejected it once deciding it was too complex and outside of the rules of the assignment. 

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Behaviors that were tested are core scheduling logic suck as task prioritization and greedy algorithm selection, sorting algorithms, filtering operations, recurrence automation, conflict detection, edge cases, and data validation. These tests were critical because they verify the core scheduling algorithm works correctly across different scenarios. The sorting and filtering tests ensure users can organize tasks in meaningful ways. Recurrence testing validates that daily/weekly tasks automatically regenerate, which is essential for a practical pet care system. Conflict detection tests prevent impossible schedules from being created. Edge case tests ensure the system handles unusual situations gracefully without crashing, making it robust for real-world use.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am pretty confidentthat the scheduler works correctly. It runs smoothly in the app, and all 20 tests passed. Some edge cases that can be be tested if I had more time are UI integration tests, large-scale performance tests, timezone edge cases, real-time updates, etc. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm happy with the code that Claude created. When testing, all of the tests passed on the first runthrough. It tested often as well. After each change, Claude offered tests, even when not completely necessary.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add a visual caledar view to allow owners to see each task as it occurs throughout the day. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that it is super important to design systems that compltely cover everything an app needs without being overly complex. A good app also needs to have good relationships that make sense.




## Prompt Comparison


Claude produced a practical, application-focused implementation that is easy to integrate. OpenAI produced a more modular and Pythonic architecture that prioritizes reusability, testability, and clean abstraction boundaries. For long-term maintainability and extensibility, the OpenAI design is stronger, even though both algorithms achieve the same scheduling goals.