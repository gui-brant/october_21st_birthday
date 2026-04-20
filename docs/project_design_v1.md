Start of the project:

Since October is struggling with "starting" her prosthetics projects, then that's what we're going to be creating for her: an application that can allow her to start her prosthetics projects. Here are the features that must be included in the demo design:

The program should be very simple as of right now. It should have three main tabs: the log in tab, the main tab, and the calendar tab.

Log in and Sign up tab - Asks for your email and password by default (Log in window). If you click sign up at the bottom of the window, it will prompt you for Name, Age, email, password, and retype password. Once you put all of the information, and you can only proceed if all of the information is there and the retype password succeeds, then you will be sent an OTP to your email. If you manage to put in an OTP, then may proceed into your version of the web app.
Whenever you log into the website, you have to put an OTP after you've managed to put your email and password.

Main Tab - It says "Hello, {name}, what are we working on today?" as a large title much like a ChatBot would. Below this you can find three boxes: a Search for Project box, a "+ New Project" box, and a list of every project below that (from latest to oldest). At the top left of the dashboard, it will showcase "{name} {lastName}" and an EXP bar beside it (more on that soon). On the top right of the dashboard, there will be a "Log out" button that sends the user back to the Sign in page and gets rid of the cookie for that machine/user. To the right of the name and EXP bar, there should be a Calendar button that will transfer the user into the page with his/her current calendar.

Clicking "Search for a Project Box" allows you to type in the name of the title of the project that you're looking for and it will show only the projects whose name match the input strings. A trie can be used for this functionality. Then, as per the result of the trie, it will eliminate the Projects whose names do not match the input dynamically as the user types. So, typing to the box is the prompt for the system to run the trie logic. Every change on the input also changes the matches shown below "+ New Project". So, if there is a project Called "Arm 2" and another project called "Arm 1," then typing "A" should show both, typing "Ar" should show both, typing "Arm " should show both, but typing "Arm 1" should show only "Arm 1." Moreover, it should not be whitespace sensitive. It should erase whitespace from both the input and matching project name, and try to match those two without whitespace.

Clicking "+ New Project" erases the "Hello, {name}, what are we working on today?" title, along with the other projects and "Search" boxes. The background image and tab options at the top remain the same, however. The general layout of the web app will also remain the same, as if nothing had changed. This will lead the user to the main logical loop of the program: insert project name -> insert general topic (what is it that you're doing/making?) -> Knowledge/Research needed! - What is it that you need to do/make it? (this would allow for brainstorming-style list creation, it would create a list of numbered items where each item can be dragged up or down as it is enter-keyed into creation; the user can then organize the list by dragging the produced boxes up or down. There should also be an option to change the numbers in the list into bullets or dashes) -> Plan subtasks by clicking on each box, you prompt a dropdown menu with subtasks. This similar in dynamics to the Project menu for a specific project.

Clicking on a specific project will open the page for that project as described below.

Calendar - A slick, minimalistic, and simple calendar that allows the user assign tasks to be done during a certain window of time. Ideally, this can be imported from an Open More about that soon. This calendar must have a two-way Google API integration and will be built upon Angular's FullCalendar model. Google Identity Services/Auth 2.0 will be used for connecting the app to your Google Account.

The structure of a project creation will follow a prompt and answer format:

- Title and Project creation: First, there will be just a pop up for the name of the project/task. You type in its name on a big box that will pop up on the middle of the screen after you pressed "+ New Project." Above that box, it will ask "What is the name of the project?". Pressing enter will make that input the title of the page (so it will fade away the question and the input box and will fade in the input Title at the top of the page). Adding the title, creates a new project. If the user taps out of the window without typing anything into the Title, that does not create a new project. If the user taps out of the window with anything written (even if a typo or incomplete), that becomes a project on the main menu page. Once a project is created, the project tab has the project name at the top of the page, which can be edited by clicking on it and typing as normal. Pressing "Enter" during the editing will change the name permanently. Making changes to the title and pressing out or refreshing the window should auto save those changes, even though "Enter" was not pressed.

- Creating Tasks in the Project: once the project is created, at all times, there will be a line directly below the title page. On the left side of that line, there will be a "New Task" button. On the right side of that lide, there will be three buttons that allow for the selection of the three different types of listing that can be done (numbered, bullet, dashes). The numbered button will be a 1, the bullet button will be a white dot, and the dash will be a -. At this point, the list would be empty since the project is new, so nothing shows up on the screen other than that line and the title. By clicking "New Task," the "New Task" button will fade away and the line "Knowledge/Research needed - What is it that you need to do/make it?" will fade into its place, the tasks that were already there should stay in place along with the overall layout. Directly below that line, there will be a button on the right most side that says "Done Adding Tasks". Clicking it, will fade that phrase out and fade in "Are you sure?" with two options directly below "Yes", which closes the "Add Task" layout and goes back to the regular display of the Project, and "No", which fades away the "Are you sure?" back into "Done Adding Tasks". Below the line with "Knowledge/Research needed - What is it that you need to do/make it?" and the "Are you sure?" button, you can see a box where you can type in to add a new Task to the project. This task will pop up at the top of the list on "Enter", if items are already there, then the new one will be numbered "1", increasing the number of every other task below it (unless the dash or dot is selected, in which case nothing would happen other than put a dash or a dot beside the starting line of the input task). You can still drag items to any desired order in that mode, as well out of that mode. To the left of the number, bullet, or dash, there should be a tickeable box. If every subtask is ticked off, the task is ticked off automatically, or you can do it manually.

- Creating subtasks in the project: Clicking on a task shows a dropdown menu. On top of the dropdown menu, there should be a "Edit or Add Subtask" button that works exactly like the "New Task" button, but it works only on the domain for tasks that are assigned below that specific Task. It has the "Done Adding Subtasks" and "Are you sure?" messages with the same dynamics as the "New Tasks" button. For now, the listing type (number, dash, or dot) will be chosen according to the option for the Tasks, but make sure to mark these listing types differently than the ones for Tasks, because this logic will change on future updates. Subtasks can be ticked off, just like tasks. Subtasks' tick box is also on the left of their number, dot, or dash. Subtasks can also be dragged up or down in and out of the task addition mode. Subtasks also have a time commitment estimation, and a date and time to submit. You can only change the estimated time or date and time to submit after you have clicked the "Edit or Add Subtask" button. Clicking the "Edit or Add Subtask" button will allow you to see the Subtask as follows:
[] 1. Take garbage downstairs.
Estimated time: <input>
Due Date: <None by default; clicking None or the current Due Date will pop up a small basic input calendar (it should have the basic functionalities to scroll past years and months, and navigate through them). The default date of the calendar is the current month with an option to go back to the Years tab>
Due time: <Does not allow you to click if Due Date is None. Write in Hour and Minute as input with a selection of PM or AM on the right side>
Every subtask can be clicked to expand a dropdown menu that shows the estimated time, due date, and due time, while off of edit mode. Clicking that subtask again would retract the dropdown menu, of course (as every dropdown menu should be in this project or otherwise). Selecting a time and date would generate an input to the app's calendar for this user. This input should now appear on the Calendar tab, as well as be sent to that person's connected Google Calendar.

NOTE: If I drag a task or subtask above or below another task or subtask, the assigned number to the left should change dynamically as I drag up and down. Holding the left side of the box for a task or subtask allows you to drag it in the context of its box space (the whole project tab for tasks, but only the specific task dropdown menu for the subtasks). Holding the left side of the box and dragging it above or below another box should prompt the system to make the numbering change of all other boxes.
Levelling system:
Starting at Level 1: Week 1 - 1 hour of work per day - 7 hours for 7 rewards in the week - up to level 7. Week 2 - 2 hours of work per day - 14 hours for 7 rewards in the week - up to level 14. Week 3 - 3 hours of work per day - 21 hours for in the week - up to level 21. Week 4 - 4 hours of work per day - 28 hours in the week - up to level 28. This is a rapid pace. Starting at level 28, the scaling will begin to plateau at a much steadier pace. It will work at that steady pace between 4 hours of work per day (for a reward), all the way to 16 hours of work per day for a reward. It should take somebody two years, with 7 rewards achieved per week, to go from 4 hours to 8 hours. Tell me the level milestone that this represents. Then, it should take that person another 3 years, with 7 rewards achieved per week, to go from 8 hours to 16 hours. Tell me the level milestone that this represents. At the end of a 5-year cycle, that person should reach 112 hours of work to get 7 rewards in the week. The scaling should seize there, meaning that, to get one reward per day, at that point on, one would have to be productive 16 hours per day.
Milestones:
From level 1 to level 28:
You defined the first month like this:
- Week 1: 1 hour/reward
- Week 2: 2 hours/reward
- Week 3: 3 hours/reward
- Week 4: 4 hours/reward
With 7 rewards per week, that gives these milestone levels:
- Level 7 → 1 hour/reward phase completed
- Level 14 → 2 hours/reward phase completed
- Level 21 → 3 hours/reward phase completed
- Level 28 → 4 hours/reward phase completed
From level 28 to level 756:
from 4 h/reward to 8 h/reward
- over 2 years
- while maintaining 7 rewards/week
From level 756 to level 1848:
from 8 h/reward to 16 h/reward
- over 3 more years
- at 7 rewards/week
Cap scaling at level 1848
Note: the mathematical formula that outlines this exists and has been created. It is taken into account for coding purposes. The basic formula is E(x) = 100 * H(x), where H(x) is defined by a very large piecewise function.
Note 2: about the formula; E(x) = 100 * H(x), H(x) is the amount of hours required to level up (outlined by the screenshotted piecewise function), E(x) is the amount of EXP required to level up, and x is the current level. 
Review additions:
OTP Flow — No Expiry or Failure State Defined

Solution:  Define a timeout (e.g. 5 min) after which the OTP expires and the user must request a new one, with a "Resend OTP" button Set a max attempt count (5 tries) before locking the session and redirecting to login.

2. New Project — Tap-Out Behavior is Contradictory

Solution:  Trim and sanitize input on tap-out: if the result after trimming is empty, no project is created. Also, projects should be deleteable (trash can on the right side of each project bar, click it creates an "Are you sure?" pop up)

3. New Task Entry — New Items Always Jump to Position #1

Solution:  Append new tasks to the bottom of the list instead as behavior default. Letting the user choose insertion behavior in Settings (top vs. bottom) will be a later feature. Append at the top for now and create a note on the design diagrams (along with the other notes that I already have) that a later update should have an option to append to the bottom or top. 

4. Subtask Listing Type Inherits From Task — But Feels Unresolved

Solution: Subtasks only appear if you click on the Task to which they belong. They will be comprised by the dropdown menu that is the Task that engulfs them. To edit the name of a task or subtask, as a result, double clicking is necessary. Single clicks allow for name edits in place (same as Title of Project). The visual differentiation is the fact that subtasks are indented, by nature of design, inside of tasks. 

5. Due Time Has No Timezone Handling

Solution: Detect and store the user's timezone on signup/login and apply it globally
Google Calendar Sync — One-Way Conflict Risk

Solution: Define a sync policy: Google Calendar is the source of truth for time, the app is the source of truth for task structure

8. Search Trie — No Empty State or Zero-Result Behavior

Solution:  Show the empty state with a neutral message only. The neutral message should be "No projects found."

9. Log Out Clears Cookie — But Session Security Isn't Defined

Solution:  Add a "Remember me" checkbox on login that controls cookie persistence duration. In later patches, the persistence length can be edited in settings from the options - 5 minutes, 15 minutes, 30 minutes, 1 hour, 3 hours, 1 day, 5 days, Never (time out; this implies cookie timeout only if log off.). Default is 30 minutes.  


Planned updates:
- There should be an option to change the Task AND Subtask listing style -> Make sure that they are marked separately during initial development, even though the same logic will change both task and subtask numbering, dotting, or dashing.
- Add settings that allow you to see and modify your user name and age. Also, it shows you your email address and has an option to change the layout of the app.
Let the user choose insertion behavior in Settings (top vs. bottom)
In later patches, the persistence length can be edited in settings from the options - 5 minutes, 15 minutes, 30 minutes, 1 hour, 3 hours, 1 day, 5 days, Never (time out; this implies cookie timeout only if log off.). Default is 30 minutes.