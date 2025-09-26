# MovieWeb_App
## About 

This is a Python project with using Flask SQLAlchemy and OOP to create a full-featured, dynamic movie web application using freely available JSON data via an API from `https://www.omdbapi.com/`. Users can create their own profiles which are displayed on the home page. Users can view the library of favorites movies for each profile on a separate page and add, update or delete movies on this page.

## Installation

To install this project, clone the repository and install the dependencies in requirements.txt using `pip install -r requirements.txt`.
Additional you need to sing in at `https://omdbapi.com/` for a free API key.
Also you have to create a file for enviroment variables `.env` to save there your free API key as `API_KEY`.
It is necessary to create the database. For this the comment can removed as before in app.py at the end of code.

## Usage

To use this project, run the following command - `python app.py` or `python3 app.py`. 
You can follow the given link in the terminal. On the home page you can add a new user profile or look at the libraries of existing users. On a profile page you can add, update or delete movies in this library. Also you can see some information of the movies title, the year, director and the movie poster. If the movies are available in the movie database of `omdbapi.com`. 

## Contributing

If you'd like to contribute to this project, please follow these guidelines:
-   create a new branch to experiment with the code and possibly also open a new issue in case of additional content or wishes
-   if you find something interesting and want to share it, create a pull request
-   in case of bugs or problems, open a new issue and describe the bug/problem and mark it with labels