# Import the create_app function from the website module
from website import create_app

# Call the create_app function to initialize the Flask app
app = create_app()

# Check if the script is being run directly (as the main module)
if __name__ == '__main__':
    app.run(debug=True)