# CornerShelf
  Cornershelf is a web app where users can create their own cookbooks and add recipes to those cookbooks. Check out others cookbooks to find delicious recipes or to add inspiration to your own cookbook. You can login to the app and start saving recipes with google OAuth. Or just look through others cookbooks without logging in at all.

## Installation
  To properly run the web app on your local machine you will need **python**, **sql**, **flask**, and **sqlAlchemy** installed on your machine.

  To allow for successful logins you will need to set up a google OAuth credential.
    1. Go to Google's OAuth [page](https://console.developers.google.com/apis).
    2. Create a project and after select **Credentials** from the menu on the left. Create am **OAuth CLient ID**.
    3. Configure the consent screen and select Web Application.
    4. Be sure to set the *Authorized Javascript Origins* to the http://localhost:5000 (or whichever channel you are using).
    5. Once you have set your origins, download the client secret as a JSON file in your root file and name it client_secrets.json.
  Once you have your client_ID and secret you will need to insert your client_ID into the appropriate (referenced) spot in the templates/login.html file.

  Next set up the database by running `python cornershelfsetup_db.py`.

  You can now run the web app on your machine by running `python cornershelf.py` and accessing `http://localhost:5000/cornershelf`

## Navigating the app.
  CornerShelf webapp has public cookbook and recipe views to any user or not logged in visitor. If you wish to create a cookbook you will need to log in using google authorization. Once you have logged in and been added as a user to the database (only name and email are saved) you can add recipes to your cookbook. You will have access to pages that the public does not such as adding recipes, editing recipes. and deleting recipes.

  Once you have finished adding and revising your recipes you can log out completely erasing your session. You can still access the site but will now only be able to view public pages.
