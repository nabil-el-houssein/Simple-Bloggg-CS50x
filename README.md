# Simple Bloggg
#### Video Demo: https://youtu.be/Ik6vzX66jbw

## **Table of contents**
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Directories and Files](#directories-and-files)

## Introduction
  Simple Bloggg is a web based blog that enables the users to create and edit their own blogs. It also allows the users to edit their own profiles and catch up with other bloggers.

## Technologies
  - Flask (Backend)
  - HTML
  - CSS
  - Javascript & jQuery (Client Side)
  - SQLite3 (Database)
  - Bootstrap 4 & Material Design For Bootstrap

## Directories and files
The main directory consists of two directories (**static** and **templates**) and four files (**application.py, blog.db, helpers.py** and **requirements.txt**).
  - ### **static**

    Static is where all the static files are stored and it consists of the following:
    1. images
        1. `sad_cat.jpg` which is rendered whenever there is an error (typo) in the link or the user is trying to access a prohibited link (like post/editblog/ where the user is not the owner of the blog).
        2. `default.jpg` which is the default profile picture of any user.
        3. `profile_pics` which contains the custom profile pictures of the users if uploaded.

    2. `styles.css` which contains all the styling used over the web app.
    3. `script.js` which contains the following jQueries running on the client side:
        1. Used `top.location.pathname` to run specific jQueries on specific pages.
        2. Two jQueries to navigate between the tabs(register & login) of `login.html`.
        3. jQuery to check if the login inputs are not empty before enabling the "log in" button.
        4. `onFormUpdate()` which ensures all the input fields are not empty and the checkbox is checked before enabling the "register" button.
        5. jQueries to check if the two password fields are of specific length(8-25 characters) and are identical otherwise disabling the 'register' button and presenting a small error text below the input field.
        6. jQuery to disallow special characters in username except `underscore(_)` and `dash(-)` in `register.html`.
        7. jQuery to make all the buttons (except `changePassword` button) to open the modal in `profile.html`.
        8. jQuery for the datepicker to operate.
        9. jQuery to disallow characters in phone except `0-9`, `()` & `+` in editing `profile.html`.
        10. `getValidUrl()` which ensures the user entered a valid url for social media links in `profile.html`.
        11. The last two jQueries makes sure the inputs in `changePassword.html` & `createBlog.html` are not null.

  - ### **templates**
    Templates is where all the `HTML` files are located and it constists of the following:
    1. `changePassword.html` where a registered user is able to change his/her password.
    2. `createBlog.html` where a registered user can create a blog.
    3. `editBlog.html` where the user who created a blog can only edit the blog he/she created.
    4. `index.html` where all the blogs are displayed as a list for everybody (the registered and the non registered ones) to view & read.
    5. `layout.html` where the main layout of the web app is located.
    6. `login.html` where it contains both the login and the register templates where they are seperated by `tabs` & `pill-contents`
    7. `page_not_found.html` displays an error message if the link the user trying to access is not found or forbidden.
    8. `post.html` where a full blog with details is displayed.
    9. `profile.html` where a registered user can view and update his profile.
    10. `terms.html` where the terms and conditions are hard-coded.
    11. `user.html` where anyone can view the profile of any registered user.

  - ### **application.py**
    The core of the web app that contains the following functions:
    1. `index()` which fetches all the blogs from the database(blogs) as a list.
    2. `user(username)` creates a unique link for every registered user available in the database(users) making it possible to view bloggers' profiles.
    3. `post(blog_id)` fetches full details about a specific blog from the database(blogs) & checks if the current logged in user is the owner of the blog, to allow him to edit it.
    4. `login()` logs in the user either using email/password or username/password.
    5. `register()` creates a user in the database(users) if the `username` or `email` doesn't already exists. `reg=True` is passed so that the `login.html` knows which tab to open by default.
    6. `logout()` logs out the user by deleting the current session.
    7. `profile()` fetches user personal information, profile picture and social media links from the database(users) (if exists) in addition to updating them.
    8. `changePassword()` allows the user to securely change/update his password.
    9. `createBlog()` insert a new blog into the database(blogs) including the username of the user who created it.
    10. `editBlog(blog_id)` updates the blog making sure that the user editing it is the one who wrote it.
    11. `allowed_image(filename)` checks if the profile picture extension getting uploaded by the user is valid.
    12. `errorhandler(e)` renders `page_not_found.html` if an unexpected error occur.

  - ### **blog.db**
    The main and only database used by the web app containing two tables:
    1. `users` for handling user's credentials and personal information.
    2. `blogs` for handling everything about blogs including the username of the user who createad a blog.

  - ### **helpers.py**
    Mainly contains two functions:
    1. `login_required(f)` which decorates routes to require login.
    2. `alert_color(color)` which specifies the color of the `bootstrap alert` in case there is an error.

  - ### **requirements.txt**
    Contains all the requirements used by the web app.


# This was CS50