# Book Review App: Search for Books and Share Your Opinion

Created as a Project 1 for CS50 Web Programming with Python and JavaScript course (2018 edition)

## <https://book-reviews-wapp.herokuapp.com/>
> #### To explore the website without having to complete registration use the following credentials:
>
>	- Username: **Explorer**
>	- Password: **password**

This is a book review web application built with Flask and PostgreSQL database hosted by Heroku.

## __Usage__:
	- Register for an account
	- Search by title (part of the title), ISBN or author
	- Leave reviews
	- See history of reviews
	- Change password as needed
	- Route /api/<isbn> returns a JSON response containing the book’s title, author, publication date, 
	ISBN number, review count and average score.
	

Project includes:

	-Pipfile
	-Pipfile.lock (created with pipenv)
	-Procfile (deploy to Heroku)
	-import.py
		Uploads to the database from books.csv.
	-books.csv
		Contains list of books with its title, author and ISBN.
	-application.py
		Flask application.
	/templates
	/static

HTML Templates (in /templates)

	-layout.html
		Layout template created with Jinja 2 that is extended to other pages. Includes navigation 
		bar and content block. 
	-register.html
		Registration page. In case user enters username that is already in use, or password and 
		confirmation don't match, there is a relevant warning message flashed.
	-login.html
		Login page. In case user enters wrong username or password, a warning message is flashed.
	-index.html
		Homepage with option to search books by ISBN, title or author.
	-query.html
		Page to display all possible matching results to the submitted query, including partial 
		match. Each result contains a button "See more" for additional information on the book. 
	-bookpage.html
		Page containing detailed information about the book, including Goodreads ratings data 
		(average rating and number of ratings it is based on) and reviews submitted on the web app. 
		On this page there is also a form for submitting a review. If the user has previously 
		submitted a review for this book, there is an "Overwrite" option near such review that 
		takes user to the top of the page to change the review.
	-userpage.html
		This page contains a list of reviews submitted by the user and contains field for changing 
		user password.

Static Files (in /static)

	Subdirectory for CSS (/static/css) contains stylesheet.css.
	Subdirectory for Images (/static/css/img).
	-scripts.js
		Includes script for filling star ratings based on received score (used in bookpage.html and 
		userpage.html) and function for return to top of the html page (used in bookpage.html) 

API Access

	Route /api/<isbn> returns a JSON response containing the book’s title, author, publication date, 
	ISBN number, review count and average score.
	

To Create Your Own App Locally

	# Clone repository
	$ git clone https://github.com/Jam-Iko/project-1
     
	# Install necessary Python packages are installed.
	$ pip3 install -r requirements.txt 
     
	# Set the environment variables:
	# On a Mac or on Linux:
	$ export FLASK_APP=application.py
	$ export DATABASE_URL= #URI of your database, check your DB credentials page on Heroku.
	$ export GOODREADS_KEY= #Goodreads API key. For more info: https://www.goodreads.com/api.
		
	# On Windows:
	$ set FLASK_APP=application.py
	$ set DATABASE_URL= #URI of your database, check your DB credentials page on Heroku.
	$ set GOODREADS_KEY= #Goodreads API key. For more info: https://www.goodreads.com/api.
		
	# Optionally set the environment variable FLASK_DEBUG to 1.
