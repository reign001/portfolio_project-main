# Art Marketplace

Art Marketplace is a platform where art lovers can meet, buy, and sell artworks. The application allows users to register, log in, and participate in the marketplace.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributors](#contributors)
- [License](#license)

## Features
- User registration and authentication
- Secure password hashing
- User login/logout functionality
- Buying and selling artworks
- Responsive landing page

## Technologies Used
- **Backend**: Flask, Flask-SQLAlchemy, Jinja
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/art-marketplace.git
    cd art-marketplace
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. Run the application:
    ```bash
    flask run
    ```

## Usage
1. Open your web browser and navigate to `http://127.0.0.1:5000/`.
2. Use the "Login" button on the landing page to either log in or register as a new user.
3. Once logged in, you can browse, buy, or sell artworks.


## Contributors
- **John Oloche Okpe**: Developed both the frontend and backend
- **Adeboye Ademide**: Initially supposed to handle the backend but deferred

## License
This project is an ALX PORTFOLIO PROJECT and as such ALX has every right to the codes.