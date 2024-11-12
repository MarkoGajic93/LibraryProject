## Usage

To set up and run the application, follow these steps:

1. **Create a PostgreSQL Database**
   - Create a database named `library`.

2. **Create a `.env` File**
   - In the project root folder, create a file named `.env` and include the following environment variables:
     ```plaintext
     FLASK_SECRET_KEY="your_secret_key"
     FLASK_ENV="development"
     FLASK_APP="run"
     POSTGRES_USER="your_postgres_username"
     POSTGRES_PASSWORD="your_postgres_password"
     ```

3. **Initialize the Database**
   - Run the database initialization script:
     `db/db_init.py`

4. **Start the Application**
   - Launch the application by running:
     `run.py`

**Note:**
To login as admine use - email: `admin@example.com`, password: `admin`
