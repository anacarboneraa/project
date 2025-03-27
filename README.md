# Health Tracker

#### Video Demo: <(https://youtu.be/R48t1UIkCVo)>

#### Description:

Hello, my name is Ana and I'm from Brazil, currently living in Salvador, Bahia. My CS50 final project is a web application called **Health Tracker**.

I had this idea since I'm currently trying to live a better and healthier life, so my project helps users monitor and improve their health by tracking health indicators such as exercise, healthy meals, and water intake. The health data can be logged daily and accessed via a dashboard that displays all the logged information, with health stats and motivational messages.

This web application was built using Flask as the backend framework, SQLite as the database, Bootstrap for styling, and ChatGPT for some health-related information and code refinements. The frontend consists of some HTML templates enhanced with JavaScript for a better user experience.

### Features:
- User authentication (where users can register and log in securely, using password hashing);
- Health logging (where users can log their health data, stored in SQLite tables);
- Dashboard (where all logged data is displayed and users can filter by dates the information shown);
- Motivational messages (encouraging messages are provided based on the user's data).

### Files:

As for the files I wrote, they are:

- **app.py**: the main application file; it handles routes, user authentication, and database operations. The functions are:

  - `index`: checks if the user is logged in. If true, redirects to /log_health; if false, welcomes the user.

  - `register`: asks the user for 3 inputs: username, password, and password confirmation. If the username is already taken, the passwords do not match, or no input is provided, a flash message appears informing the problem. Once registered successfully, the information is inserted into the database, and the user is redirected to /login.

  - `login`: asks the user for 2 inputs: username and password. If the user does not provide information, or if the username or password does not match those in the database, a flash message appears informing the problem. Once logged in, the user is redirected to /log_health.

  - `logout`: clears the session and logs the user out, redirecting to the index.

  - `log_health`: checks if the user provided the number of meals and water intake. If not, a message appears informing the problem. If the user somehow submits without the date information, the current date is used for the database. Once all the information is provided, the function inserts it into the database and redirects to a new log.

  - `dashboard`: this function checks the date the user chooses to view the logged information and calculates some percentages with it. The meal percentage is calculated by considering the total meals and the healthy meals; the workout percentage is calculated by considering the total number of days and the number of days the user worked out; and the average water intake is considered by the amount of water and total days. Motivational messages are shown based on the calculated numbers, such as:
    - If the user has exercised at least 70% of the days, the message is "Great job staying active!";
    - If at least 40%, "Keep pushing, consistency is key!";
    - If healthy meals exceed 80% of total meals, the message is "Your healthy eating habits are amazing!";
    - If more than 50%, "You're making good choices, keep it up!";
    - If the average water intake is above 8 glasses, the message is "You're staying well hydrated!";
    - If above 5, "Try to drink a little more water daily."

- **health.db**: the SQLite database, which stores users and their health logs. It consists of 2 tables: **users** and **health_logs**:
  - **users**:
    - id INTEGER PRIMARY KEY AUTOINCREMENT
    - username TEXT UNIQUE NOT NULL
    - password TEXT NOT NULL
  - **health_logs**:
    - id INTEGER PRIMARY KEY AUTOINCREMENT
    - user_id INTEGER NOT NULL
    - date DATE DEFAULT CURRENT_DATE
    - workout BOOLEAN DEFAULT 0
    - healthy_meals INTEGER DEFAULT 0
    - total_meals INTEGER DEFAULT 1
    - water_intake INTEGER DEFAULT 0
    - FOREIGN KEY (user_id) REFERENCES users (id)

- **templates/**: this directory contains all the HTML template files, which are:
  - **layout.html**: contains the default layout for all pages, using Bootstrap for design and styling. A navigation bar is shown with the name of the app and a few options depending on whether the user is logged in or not. Options include register and login if the user is not logged in, and log entry, dashboard, and logout if the user is logged in. A footer is also added.

  - **index.html**: welcomes new or returning users and displays the register and login options.

  - **register.html**: allows new users to register, requiring a username, password, and password confirmation. Flash messages appear if the user provides a taken username or mismatched passwords.

  - **login.html**: allows registered users to log in by entering their username and correct password. Flash messages appear if the user does not provide either username or password, or if the password is incorrect.

  - **log_health.html**: allows the user to log their health data, which consists of the log date, whether the user exercised or not, how many healthy meals the user made out of total meals, and their water intake.

  - **dashboard.html**: allows the user to choose the dates they want to view and displays a dashboard with all the logged information and health stats. This includes the percentage of healthy meals out of total meals, the percentage of days the user exercised, and the average amount of water the user drank. Motivational messages are also shown.

### Final Thoughts:

I have enjoyed working on this project. I can really see how much I’ve learned from CS50 since I started with zero knowledge of computer science. Of course, I encountered some difficulties along the way, like creating all the functions and making them work, deciding what I wanted to display on each template, and determining the health information necessary to calculate the stats (which ChatGPT was really helpful for). But revisiting the classes and doing research and study really helped me. I'm very happy and satisfied with my project, and I hope everyone enjoys it. This was CS50.
