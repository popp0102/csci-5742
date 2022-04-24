import html

def get_user_input_without_sanitization3():
    user_input = input("Please enter something")
    return user_input

def get_user_input_without_sanitization():
    input("Please enter something")

def get_user_input_without_sanitization2():
    return input("Please enter something")

def get_user_input_with_sanitization():
    print("Please enter something")
    user_input = input()
    user_input = html.escape(user_input)
    return user_input

user_input = get_user_input_without_sanitization()
print("You entered: " + user_input)

user_input = get_user_input_without_sanitization2()
print("You entered: " + user_input)

user_input = get_user_input_without_sanitization3()
print("You entered: " + user_input)

user_input = get_user_input_with_sanitization()
print("You entered: " + user_input)

