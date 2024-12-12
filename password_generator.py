from flask import Flask, request
import pandas as pd
import random
import string

# Define the symbols dictionary
symbols = {
    "ampersand": "&",
    "asterisk": "*",
    "at": "@",
    "caret": "^",
    "comma": ",",
    "curly_brace_close": "}",
    "curly_brace_open": "{",
    "dollar": "$",
    "exclamation": "!",
    "hash": "#",
    "parenthesis_close": ")",
    "parenthesis_open": "(",
    "percent": "%",
    "period": ".",
    "plus": "+",
    "question_mark": "?",
    "tilde": "~",
    "underscore": "_"
}


# Password generator functions
def gen_password_letters_numbers(length):
    letters = string.ascii_letters
    numbers = string.digits
    all_characters = list(letters + numbers) 
    random.shuffle(all_characters)
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password


def gen_password_symbols(length):
    letters = string.ascii_letters
    numbers = string.digits
    all_characters = list(letters + numbers + ''.join(symbols.values())) 
    random.shuffle(all_characters)
    password = ''.join(random.choice(all_characters) for i in range(length))
    return password


password_list = pd.DataFrame(columns=['Name', 'Password'])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global password_list
    if request.method == 'POST':
        name = request.form['name']
        length = int(request.form['length'])
        use_symbols = request.form.get('use_symbols')

        if use_symbols:
            password = gen_password_symbols(length)
        else:
            password = gen_password_letters_numbers(length)

        # Add the new password to the DataFrame
        new_row = pd.DataFrame({'Name': [name], 'Password': [password]})
        password_list = pd.concat([password_list, new_row], ignore_index=True)

        print(password_list)

        password_list.to_csv('passwords.csv', index=False)

        return f"Password for {name}: {password} (Saved to CSV)"

    return '''
        <form method="post">
            Name: <input type="text" name="name"><br>
            Length: <input type="number" name="length"><br>
            Use Symbols: <input type="checkbox" name="use_symbols"><br>
            <input type="submit" value="Generate and Save">
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
