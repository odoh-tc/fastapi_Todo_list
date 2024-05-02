# FastAPI Todo List

A simple Todo List application built with FastAPI. This app allows users to create, edit, delete, and view todo items. The backend is developed with FastAPI, while the frontend uses Jinja2 templates for rendering.

---

## Features

- Create, edit, and delete todo items
- User authentication with secure login and registration
- Priority-based todo items
- FastAPI backend with SQLite database

---

## Installation

To set up and run the FastAPI Todo List app locally, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

   ```

4. **Set Environment Variables**

- Create a .env file in the root of the project.
- Add your environment variables (e.g., SECRET_KEY=your-secret-key).

5. **Run the Application**

   ```bash
   uvicorn main:app --reload

   ```

## Usage

After setting up the application, open your web browser and navigate to [http://127.0.0.1:8000/auth](http://127.0.0.1:8000/auth) to access the Todo List app.

- **Registration**: Click "Register" to create a new user account.
- **Login**: Use your credentials to log in.
- **Add Todo**: Click "Add Todo" to create a new todo item.
- **Edit Todo**: Click "Edit" on a todo item to update it.
- **Delete Todo**: Click "Delete" to remove a todo item.

## Deployment

If deploying to a cloud platform (e.g., Render), ensure the following:

- **Dockerfile**: Include a Dockerfile with the correct setup for FastAPI and SQLite.
- **Environment Variables**: Set environment variables through the platform's dashboard. Do not commit sensitive information like API keys.
- **Port Configuration**: Ensure the correct port configuration for the platform (default is 8000).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with a detailed description of your changes. Ensure your code follows the project's coding standards and includes appropriate tests.
