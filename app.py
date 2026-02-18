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

if st.button("Generate Schedule"):
    if not st.session_state.owner.pets:
        st.warning("Please add at least one pet before generating a schedule.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Please add at least one task before generating a schedule.")
    else:
        # Create a Scheduler and generate the plan
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()

        # Display the plan
        st.success("Schedule generated!")

        st.markdown(f"### Daily Plan for {plan['owner'].name}")
        st.write(f"**Pets:** {plan['pets_count']}")

        if plan['scheduled_tasks']:
            st.markdown("**Scheduled Tasks:**")
            for i, task in enumerate(plan['scheduled_tasks'], 1):
                st.write(f"{i}. {task}")
        else:
            st.info("No tasks could be scheduled.")

        st.markdown("**Time Summary:**")
        st.write(f"- Total scheduled: {plan['total_time_minutes']} minutes")
        st.write(f"- Remaining time: {plan['remaining_time_minutes']} minutes")

        if plan['skipped_tasks']:
            st.markdown(f"**Skipped Tasks ({len(plan['skipped_tasks'])}):**")
            for task in plan['skipped_tasks']:
                st.write(f"- {task}")

        with st.expander("Scheduling Reasoning"):
            st.write(plan['reasoning'])
