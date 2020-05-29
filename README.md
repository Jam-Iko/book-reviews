# Project 1

Web Programming with Python and JavaScript

This is a book review web application built with Flask and PostgreSQL database hosted by Heroku.
Project includes:

	-requirements.txt
	-import.py
		Completes upload to the database from books.csv.
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
		Login page. In case user enters wrong username or password, a relevant warning message 
		is flashed.
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
	

To Launch (Instructions from CS50W Project 1)

	-Run pip3 install -r requirements.txt in your terminal window to make sure that all of the necessary 
	Python packages are installed.
	-Set the environment variable FLASK_APP to be application.py.
		On a Mac or on Linux - export FLASK_APP=application.py	
		On Windows - set FLASK_APP=application.py
	-Optionally set the environment variable FLASK_DEBUG to 1.
	-Set the environment variable DATABASE_URL to be the URI of your database, which you should be able to
	see from the credentials page on Heroku.
