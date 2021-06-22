from application import init_app

app = init_app()

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)