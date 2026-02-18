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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
