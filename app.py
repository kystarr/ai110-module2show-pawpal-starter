import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time per day (minutes)", min_value=0, max_value=1440, value=180)

# Initialize Owner in session state if it doesn't exist
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time_minutes=available_time)

st.markdown("### Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add Pet"):
    # Create a new Pet object and add it to the Owner
    new_pet = Pet(name=pet_name, species=species, age=pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added {pet_name} to {st.session_state.owner.name}'s pets!")

# Display current pets
if st.session_state.owner.pets:
    st.write(f"**{st.session_state.owner.name}'s Pets:**")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet}")
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add tasks to your pets. These will feed into your scheduler.")

# Only show task inputs if there are pets
if st.session_state.owner.pets:
    # Select which pet to add task to
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Add task for:", pet_names)
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task description", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        task_type = st.selectbox("Task type", ["walk", "feeding", "meds", "grooming", "enrichment", "other"])
    with col5:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed"])

    if st.button("Add Task"):
        # Create a Task object and add it to the selected pet
        new_task = Task(
            description=task_title,
            duration_minutes=int(duration),
            frequency=frequency,
            priority=priority,
            task_type=task_type
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' to {selected_pet.name}!")

    # Display all tasks for all pets
    st.write("**All Tasks:**")
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        for pet in st.session_state.owner.pets:
            if pet.tasks:
                st.write(f"**{pet.name}:**")
                for task in pet.tasks:
                    st.write(f"  - {task}")
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate an optimized daily schedule based on your pets' tasks and available time.")

if st.button("Generate Schedule", type="primary"):
    if not st.session_state.owner.pets:
        st.warning("⚠️ Please add at least one pet before generating a schedule.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("⚠️ Please add at least one task before generating a schedule.")
    else:
        # Create a Scheduler and generate the plan
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()

        # Store plan in session state for viewing/filtering
        st.session_state.plan = plan
        st.session_state.scheduler = scheduler

        # Display conflict warnings prominently
        conflict_info = plan['conflict_info']
        if conflict_info['has_conflict']:
            st.error(f"⚠️ {conflict_info['message']}")
            st.warning(
                f"**Time Budget Issue:** You have {conflict_info['overflow_minutes']} minutes "
                f"of overflow. Consider increasing available time or reducing task load."
            )
        else:
            st.success(f"✅ {conflict_info['message']}")

        # Display the plan header
        st.markdown(f"### 📋 Daily Plan for {plan['owner'].name}")

        # Time summary with visual progress bar
        time_used_pct = (plan['total_time_minutes'] / max(plan['owner'].available_time_minutes, 1)) * 100
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Scheduled", f"{plan['total_time_minutes']} min")
        with col2:
            st.metric("Remaining Time", f"{plan['remaining_time_minutes']} min")
        with col3:
            st.metric("Pets", plan['pets_count'])

        st.progress(min(time_used_pct / 100, 1.0), text=f"Time Utilization: {time_used_pct:.1f}%")

        # Display scheduled tasks in a professional table
        if plan['scheduled_tasks']:
            st.markdown("#### ✅ Scheduled Tasks")

            # Create a data table for better visualization
            import pandas as pd
            task_data = []
            for i, task in enumerate(plan['scheduled_tasks'], 1):
                # Find which pet owns this task
                pet_name = "Unknown"
                for pet in st.session_state.owner.pets:
                    if task in pet.tasks:
                        pet_name = pet.name
                        break

                task_data.append({
                    "#": i,
                    "Task": task.description,
                    "Pet": pet_name,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority.upper(),
                    "Type": task.task_type.capitalize(),
                    "Frequency": task.frequency.capitalize()
                })

            df = pd.DataFrame(task_data)

            # Color-code priority
            def highlight_priority(row):
                if row['Priority'] == 'HIGH':
                    return ['background-color: #ffcccc'] * len(row)
                elif row['Priority'] == 'MEDIUM':
                    return ['background-color: #fff4cc'] * len(row)
                else:
                    return ['background-color: #ccffcc'] * len(row)

            styled_df = df.style.apply(highlight_priority, axis=1)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No tasks could be scheduled.")

        # Display skipped tasks with warning
        if plan['skipped_tasks']:
            st.markdown(f"#### ⏭️ Skipped Tasks ({len(plan['skipped_tasks'])})")
            st.warning(
                f"The following tasks could not fit in the available time budget. "
                f"Consider rescheduling or increasing available time."
            )

            # Create skipped tasks table
            import pandas as pd
            skipped_data = []
            for task in plan['skipped_tasks']:
                # Find which pet owns this task
                pet_name = "Unknown"
                for pet in st.session_state.owner.pets:
                    if task in pet.tasks:
                        pet_name = pet.name
                        break

                skipped_data.append({
                    "Task": task.description,
                    "Pet": pet_name,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority.upper(),
                    "Type": task.task_type.capitalize()
                })

            skipped_df = pd.DataFrame(skipped_data)
            st.dataframe(skipped_df, use_container_width=True, hide_index=True)

        # Scheduling reasoning in expander
        with st.expander("📊 Scheduling Reasoning & Algorithm Details"):
            st.write(plan['reasoning'])
            st.markdown("---")
            st.caption(
                "**Algorithm:** Greedy scheduling with priority-based sorting. "
                "Time complexity: O(n log n) for sorting + O(n) for fitting = O(n log n) overall."
            )

# Advanced Task Analysis Section (only show if plan exists)
if 'plan' in st.session_state and 'scheduler' in st.session_state:
    st.divider()
    st.subheader("📊 Advanced Task Analysis")
    st.caption("Explore your tasks with different sorting and filtering options")

    scheduler = st.session_state.scheduler
    all_tasks = st.session_state.owner.get_all_tasks()

    if all_tasks:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Sort Tasks By:**")
            sort_option = st.radio(
                "Choose sorting method:",
                ["Priority (Default)", "Duration (Shortest First)", "Duration (Longest First)", "Task Type Order"],
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**Filter Tasks By:**")
            filter_option = st.selectbox(
                "Choose filter:",
                ["All Tasks", "Completed Only", "Incomplete Only", "By Pet", "By Task Type", "By Frequency"]
            )

        # Apply filtering
        filtered_tasks = all_tasks.copy()

        if filter_option == "Completed Only":
            filtered_tasks = scheduler.filter_by_completion_status(all_tasks, completed=True)
        elif filter_option == "Incomplete Only":
            filtered_tasks = scheduler.filter_by_completion_status(all_tasks, completed=False)
        elif filter_option == "By Pet":
            if st.session_state.owner.pets:
                selected_pet = st.selectbox("Select pet:", [pet.name for pet in st.session_state.owner.pets])
                filtered_tasks = scheduler.filter_by_pet(all_tasks, selected_pet)
        elif filter_option == "By Task Type":
            selected_type = st.selectbox("Select type:", ["walk", "feeding", "meds", "grooming", "enrichment", "other"])
            filtered_tasks = scheduler.filter_by_task_type(all_tasks, selected_type)
        elif filter_option == "By Frequency":
            selected_freq = st.selectbox("Select frequency:", ["daily", "weekly", "as-needed"])
            filtered_tasks = scheduler.filter_by_frequency(all_tasks, selected_freq)

        # Apply sorting
        if sort_option == "Priority (Default)":
            sorted_tasks = scheduler.prioritize_tasks(filtered_tasks)
        elif sort_option == "Duration (Shortest First)":
            sorted_tasks = scheduler.sort_by_duration(filtered_tasks, ascending=True)
        elif sort_option == "Duration (Longest First)":
            sorted_tasks = scheduler.sort_by_duration(filtered_tasks, ascending=False)
        elif sort_option == "Task Type Order":
            sorted_tasks = scheduler.sort_by_task_type(filtered_tasks)

        # Display results
        if sorted_tasks:
            st.success(f"Found {len(sorted_tasks)} task(s)")

            import pandas as pd
            analysis_data = []
            for task in sorted_tasks:
                # Find which pet owns this task
                pet_name = "Unknown"
                for pet in st.session_state.owner.pets:
                    if task in pet.tasks:
                        pet_name = pet.name
                        break

                analysis_data.append({
                    "Status": "✅" if task.completed else "⬜",
                    "Task": task.description,
                    "Pet": pet_name,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority.upper(),
                    "Type": task.task_type.capitalize(),
                    "Frequency": task.frequency.capitalize()
                })

            analysis_df = pd.DataFrame(analysis_data)
            st.dataframe(analysis_df, use_container_width=True, hide_index=True)
        else:
            st.info("No tasks match the selected filter.")
    else:
        st.info("Add tasks to see analysis options.")
