from flask import Flask, render_template, request, send_file
import io
from your_cipher_module import cipher_functions, cipher_descriptions, format_output

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    steps = []
    description = ''
    text = ''
    cipher_name = ''
    mode = 'encrypt'
    key = ''
    show_key = False

    if request.method == 'POST':
        text = request.form.get('text', '')
        cipher_name = request.form.get('cipher', '')
        mode = request.form.get('mode', 'encrypt')
        key = request.form.get('key', '')

        if cipher_name in cipher_functions:
            func = cipher_functions[cipher_name]
            try:
                if 'Vigenère' in cipher_name:
                    show_key = True
                    if not key:
                        result, steps = 'Error: Key required.', []
                    else:
                        result, steps = func(text, key, decrypt=(mode == 'decrypt'))
                else:
                    if mode == 'decrypt' and 'decrypt' in func.__code__.co_varnames:
                        result, steps = func(text, decrypt=True)
                    else:
                        result, steps = func(text)
                description = cipher_descriptions.get(cipher_name, '')
            except Exception as e:
                result, steps = f"Error: {str(e)}", []

    return render_template(
        'index.html',
        result=result,
        steps=steps,
        cipher_functions=sorted(cipher_functions.keys()),
        description=description,
        show_key=show_key,
        request=request,
        input_text=text,
        cipher_name=cipher_name,
        mode=mode,
        key=key
    )

@app.route('/download', methods=['POST'])
def download():
    text = request.form.get('text', '')
    cipher_name = request.form.get('cipher', '')
    result = request.form.get('result', '')
    key = request.form.get('key', '')
    mode = request.form.get('mode', 'encrypt')

    if cipher_name in cipher_functions:
        func = cipher_functions[cipher_name]
        try:
            if 'Vigenère' in cipher_name:
                result, steps = func(text, key, decrypt=(mode == 'decrypt'))
            else:
                result, steps = func(text, decrypt=(mode == 'decrypt')) if 'decrypt' in func.__code__.co_varnames else func(text)
        except Exception as e:
            result = f"Error: {str(e)}"
            steps = []

        formatted = format_output(cipher_name, text, result, steps)
        buffer = io.BytesIO()
        buffer.write(formatted.encode('utf-8'))
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="cipher_output.txt", mimetype='text/plain')

    return "Invalid cipher selection", 400

if __name__ == '__main__':
    app.run(debug=True)
