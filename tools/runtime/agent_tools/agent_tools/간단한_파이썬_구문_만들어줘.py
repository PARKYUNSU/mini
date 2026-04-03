def greet_user(name="World"):
    """
    A simple function to greet a user.
    """
    try:
        message = f"Hello, {name}!"
        print(message)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage of the simple Python statement
    greet_user("Python User")
    greet_user() # Calls with default name