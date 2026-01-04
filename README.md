# Quote50
#### Video Demo:  https://youtu.be/2GdRzVeC9ko
#### Description:
"Quote50" is a social media platform where users can post, like, and "requote" quotes. These quotes can be from books, movies, a specific person, or even ones they've made up themselves. The main features of the website include posting quotes, liking or "requoting" other users' posts, and searching through the website's content.

When accessing Quote50 for the first time, users must register an account to fully interact with the site. After logging in, users are redirected to the homepage where they can see a list of every quote posted by the most recent to the oldest one.

If a user wants to post a quote they simply enter the quote they want to share and the source it came from (e.g., a book or movie title) directly on the home page.

Each quote has two buttons below it: one for liking the quote and another for "requoting" it (similar to a retweet). When interacting with these buttons, the like/requote counters update instantly without refreshing the whole page. That was achieved by using AJAX, which sends requests to the server with the ID of the quote the user interacted with and retrieves the updated counts without refreshing the page. 

Also, AJAX is used on the homepage to fetch all quotes the user has liked or requoted, so the page loads with the proper styling of the quote's buttons (like/requote), reflecting the user's previous interactions.

The header provides access to the user's profile page and a logout option. There's also a search bar where users can search for other users, quotes, or sources. Results can be filtered as needed afterwards.

The profile page shows all the quotes a user has posted, along with any quotes they've requoted. There is also an option to see all the quotes the user has liked.

The search bar in the header allows users to search for anything across the website. Once the search results are displayed, users can apply filters to see only what they want to, being it specific quotes, users, or sources.

The project uses SQLite3 and the database has two tables:
- Users: This table stores user information such as username, email, hashed passwords, liked quotes and requoted quotes.
- Quotes: This table stores quotes information such as the quotes themselves, sources, timestamps and the user who posted it.

User passwords are hashed using Werkzeug to ensure security.

For storing likes and requotes, it was used SQLite's support for JSON fields to store the IDs of quotes the user has interacted with, along with a timestamp. This allows for sorting and rendering quotes based on the latest action (e.g., a liked quote from yesterday can appear above a quote posted today).

I decided to store likes and requotes within a JSON field in the user table instead of creating a separate table to track interactions. This design choice was made to simplify the database for this project's scope. While a third table would have been more normalized and organized, it was not necessary given the project's size.

The decision to use SQLite3 over a more powerful database like MySQL was primarily due to ease of setup, my previous knowledge and the small scale of the project. However, while working on the database interactions I encountered a limitation: SQLite3 does not natively support a TIMESTAMP data type, instead, it stores it as strings (e.g., "2024-01-01 00:00:00"). To display these timestamps in a more user-friendly format (e.g., "Jan 01, 2024"), I wrote a Python function to convert and reformat the timestamp strings when rendering them in the jinja templates.

#### Folder Structure
The `/static` folder contains all the JavaScript files, CSS stylesheets, and images used in the website. For this project, I chose not to use Bootstrap as I wanted to create a personalized style and add custom stylings that Bootstrap doesn't provide. However, for icons, I used Bootstrap Icons to avoid downloading multiple image files. The only image used in the entire website is the logo, which is located in the `/img` folder within `/static`.

Inside the `/static` folder, you'll find the following JavaScript files:

- `Hovering.js`: Changes the class of certain icons to apply different styles when hovering with the cursor.
- `LikesRequotes.js`: Manages the AJAX interactions for liking and requoting quotes as described earlier.
- `Placeholders.js`: Dynamically changes the quote input placeholder text for a better user experience.
- `SearchFilters.js`: Handles the filtering of search results based on user input in the search bar.

The main styling for the website is contained in `/static/style.css`, which holds all the custom CSS used throughout the site.

The `/templates` folder contains all the HTML files for the website. Most of these are Jinja templates that are rendered inside `layout.html`, which serves as the base layout for the site.

One exception is the `_quotes.html` file, which is a Jinja macro specifically designed for rendering quotes across different pages. Using a macro allowed me to avoid copying and pasting the same code for rendering quotes multiple times, making the code more reusable and easier to maintain.

The `app.py` file contains the entire backend logic for the website. It handles all the routes and manages the POST and GET requests across the website. It also manages database interactions with the `quote50.db` SQLite database, where all the necessary data (like users, quotes, likes, and requotes) is stored.