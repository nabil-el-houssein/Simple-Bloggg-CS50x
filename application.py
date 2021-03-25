from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import re
import os
import datetime
import validators

from helpers import alert_color, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Path to upload pictures to
app.config["IMAGE_UPLOADS"] = '/home/ubuntu/project/static/images/profile_pics'

# Allowed image types
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blog.db")


@app.route("/")
def index():
    """Show all the blogs"""

    blogs = db.execute("SELECT * FROM blogs ORDER BY id DESC")

    return render_template("index.html", blogs=blogs)


@app.route("/profile/<username>")
def user(username):
    """Unique Profile for each user"""

    users = db.execute("SELECT * FROM users WHERE username=?", username)

    # If user is not found; render page_not_found
    if len(users) != 1:
        return render_template("page_not_found.html")

    return render_template("user.html", users=users)


@app.route("/post/<blog_id>")
def post(blog_id):
    """Unique blog post based on id"""

    # Get the current logged in user username to check if he is the owner of the blog
    username = ""
    if session.get("user_id"):
        username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]

    blogs = db.execute("SELECT * FROM blogs WHERE id=?", blog_id)

    # If blog is not found; render page_not_found
    if len(blogs) != 1:
        return render_template("page_not_found.html")

    return render_template("post.html", blogs=blogs, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in the user"""

    if request.method == "POST":

        # Gets the login credential and password from template
        cred = request.form.get("loginCred").strip()
        password = request.form.get("loginPassword")

        if not cred or not password:
            flash("Please complete all the fields")
            alert_color("warning")
            return redirect("/login")

        # Checks if email exists and log in the user
        if '@' in cred:
            email = db.execute("SELECT * FROM users WHERE email=?", cred)
            if len(email) != 1 or not check_password_hash(email[0]["password"], password):
                flash("Invalid Email Address or Password")
                alert_color("danger")
                return redirect("/login")
            elif len(email) == 1 and check_password_hash(email[0]["password"], password):
                session["user_id"] = email[0]["id"]
                flash("Logged in successfully")
                alert_color("success")
                return redirect("/")

        # Checks if username exists and log in the user
        else:
            username = db.execute("SELECT * FROM users WHERE username=?", cred)
            if len(username) != 1 or not check_password_hash(username[0]["password"], password):
                flash("Invalid Username or Password")
                alert_color("danger")
                return redirect("/login")
            elif len(username) == 1 and check_password_hash(username[0]["password"], password):
                session["user_id"] = username[0]["id"]
                flash("Logged in successfully")
                alert_color("success")
                return redirect("/")

    # If the user is already logged in redirect to main
    if session.get("user_id") is not None:
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Create a new user"""

    if request.method == "POST":

        # Gets all the user info
        name = request.form.get("registerName").strip()
        username = request.form.get("registerUsername").strip()
        email = request.form.get("registerEmail").strip()
        password = request.form.get("registerPassword")
        confirm_password = request.form.get("registerConfirmPassword")

        # Checks if all the fields are filled
        if not name or not username or not email or not password or not confirm_password:
            flash("Please complete all the fields")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if length of password is correct
        elif len(password) < 8 and len(password) > 25:
            flash("Password must contain 8-25 characters")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if passwords match
        elif password != confirm_password:
            flash("Passwords do not Match")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if username is valid (only contains numbers, letters , hyphens and underscores)
        elif not re.match("^[A-Za-z0-9_-]*$", username):
            flash("Username is not valid")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if email address is valid
        elif not re.match(r"^[^@]+@[^@]+\.[^@]+", email):
            flash("Email is not valid")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if username already exists
        username_exists = db.execute("SELECT * FROM users WHERE username=?", username)

        if len(username_exists) != 0:
            flash("Username already exists")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Checks if email already in use
        email_exists = db.execute("SELECT * FROM users WHERE email=?", email)

        if len(email_exists) != 0:
            flash("Email already in use")
            alert_color("warning")
            return render_template("login.html", reg=True)

        # Insert user into table
        db.execute("INSERT INTO users(username, email, name, password, account_created) VALUES(?, ?, ?, ?, datetime('now'))",
                   username, email, name, generate_password_hash(password))

        # Logs the user in
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = user[0]["id"]

        # Success message
        flash("Registered successfully")
        alert_color("success")

        return redirect("/")

    # If the user is already logged in redirect to main
    if session.get("user_id") is not None:
        return redirect("/")

    # Renders login.html showing the register tab
    return render_template("login.html", reg=True)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Success message
    flash("Logged out successfully")
    alert_color("success")

    # Redirect user to main page
    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User Profile"""

    # Gets the current user from the database
    users = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])

    if request.method == "POST":

        # Gets info from edit profile
        profession = request.form.get("profession")
        address = request.form.get("address")
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        website = request.form.get("website")
        github = request.form.get("github")
        twitter = request.form.get("twitter")
        instagram = request.form.get("instagram")
        facebook = request.form.get("facebook")

        if request.files["image"]:

            image = request.files["image"]

            # Ensuring the image has a filename
            if image.filename == "":
                flash("Picture has no filename")
                alert_color("warning")
                return redirect("/profile")

            # Check if the extension is allowed
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                # assign username as file name
                ext = filename.rsplit(".", 1)[1]

                filename = users[0]["username"] + "." + ext

                # Save image in the system
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

                # Save image name in database
                db.execute("UPDATE users SET image_path=? WHERE username=?", filename, users[0]["username"])

            else:
                flash("Image Upload Failed")
                alert_color("warning")
                return redirect("/profile")

        # Checks if birthdate is valid
        if birthdate:
            try:
                datetime.datetime.strptime(birthdate, '%d-%m-%Y')
            except ValueError:
                flash("Birthdate format is invalid")
                alert_color("warning")
                return redirect("/profile")

        # Checks if the selected gender is valid
        if gender not in ["Male", "Female", "Prefer Not To Say", None]:
            flash("Selected gender is not allowed")
            alert_color("warning")
            return redirect("/profile")

        # Checks if phone is valid
        elif not re.match("^[0-9+\-\)\(]*$", phone):
            flash("Phone number is invalid")
            alert_color("warning")
            return redirect("/profile")

        # Checks if website is valid
        elif website and not validators.url(website):
            flash("Invalid Website Link")
            alert_color("warning")
            return redirect("/profile")

        # Checks if github is valid
        elif github and not validators.url(github):
            flash("Invalid Github Link")
            alert_color("warning")
            return redirect("/profile")

        # Checks if twitter is valid
        elif twitter and not validators.url(twitter):
            flash("Invalid Twitter Link")
            alert_color("warning")
            return redirect("/profile")

        # Checks if instagram is valid
        elif instagram and not validators.url(instagram):
            flash("Invalid Instagram Link")
            alert_color("warning")
            return redirect("/profile")

        # Checks if facebook is valid
        elif facebook and not validators.url(facebook):
            flash("Invalid facebook Link")
            alert_color("warning")
            return redirect("/profile")

        # Updates User profile and redirects to profile page
        db.execute("UPDATE users SET bio=?, address=?, birthdate=?, gender=?, phone=?, website=?, github=?, twitter=?, instagram=?, facebook=? WHERE username=?",
                   profession, address, birthdate, gender, phone, website, github, twitter, instagram, facebook, users[0]["username"])
        flash("Profile Updated!")
        alert_color("success")
        return redirect("/profile")

    return render_template("profile.html", users=users)


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Changes User Password"""

    if request.method == "POST":

        # Gets passwords from template
        old_pass = request.form.get("oldPass")
        new_pass = request.form.get("newPass")
        confirm_pass = request.form.get("confirmPass")

        user = db.execute("SELECT password FROM users WHERE id=?", session["user_id"])
        # Checks if fields are not empty
        if not old_pass or not new_pass or not confirm_pass:
            flash("Please complete all the fields")
            alert_color("warning")
            return redirect("/changePassword")

        # Checks if old pass is correct
        elif not check_password_hash(user[0]["password"], old_pass):
            flash("Old Password is Incorrect")
            alert_color("warning")
            return redirect("/changePassword")

        # Checks password length
        elif len(new_pass) < 8 or len(new_pass) > 25:
            flash("Password must contain 8-25 characters")
            alert_color("warning")
            return redirect("/changePassword")

        # Checks if password matches
        elif new_pass != confirm_pass:
            flash("Passwords do not match")
            alert_color("warning")
            return redirect("/changePassword")

        # Checks if the new pass is the same as the old one
        elif new_pass == old_pass:
            flash("New Password can't be the same as Old one")
            alert_color("warning")
            return redirect("/changePassword")

        # Saves the new pass
        db.execute("UPDATE users SET password=? WHERE id=?", generate_password_hash(new_pass), session["user_id"])
        flash("Password Updated Successfully")
        alert_color("success")
        return redirect("/profile")

    return render_template("changePassword.html")


@app.route("/createBlog", methods=["GET", "POST"])
@login_required
def createBlog():
    """Create a New Blog"""

    if request.method == "POST":

        # Gets the blog details
        title = request.form.get("title")
        desc = request.form.get("desc")
        subtitle = request.form.get("subTitle")

        # Checks if the fields are null
        if not title or not subtitle or not desc:
            flash("Please complete all the fields")
            alert_color("warning")
            return redirect("/createBlog")

        # Gets username based on session id
        username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]

        # Insert blog into database
        db.execute("INSERT INTO blogs(username, title, subtitle, desc, date_posted) VALUES(?, ?, ?, ?, date('now'))",
                   username, title, subtitle, desc)

        return redirect("/")

    return render_template("createBlog.html")


@app.route("/post/editBlog/<blog_id>", methods=["GET", "POST"])
@login_required
def editBlog(blog_id):
    """Edit Blog"""

    # Checks if the user who wants to edit is the owner of the blog
    editor_username = db.execute("SELECT username FROM blogs WHERE id=?", blog_id)[0]["username"]

    current_username = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])[0]["username"]

    if editor_username == current_username:

        if request.method == "POST":
            # Gets the blog details
            title = request.form.get("title")
            desc = request.form.get("desc")
            subtitle = request.form.get("subTitle")

            # Checks if the fields are null
            if not title or not subtitle or not desc:
                flash("Please complete all the fields")
                alert_color("warning")
                return redirect(url_for("editBlog", blog_id=blog_id))

            # Insert blog into database and redirect to updated post
            db.execute("UPDATE blogs SET title=?, subtitle=?, desc=?, date_updated=date('now') WHERE id=?", title, subtitle, desc, blog_id)
            flash("Successfully Updated")
            alert_color("success")
            return redirect(url_for("post", blog_id=blog_id))

        blogs = db.execute("SELECT * FROM blogs WHERE id=?", blog_id)
        return render_template("editBlog.html", blogs=blogs)

    else:
        return render_template("page_not_found.html")


def allowed_image(filename):
    """Check if image file extension is valid"""

    if not "." in filename:
        return false

    # Split extension from file name
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is allowed
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("page_not_found.html")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)