from flask import Flask, render_template, request, send_file
import io
import base64
from your_cipher_module import cipher_functions, cipher_descriptions, format_output

app = Flask(__name__)

@app.route("/custom", methods=["GET", "POST"])
def custom_cipher():
    result = ""
    steps = []
    if request.method == "POST":
        text = request.form.get("text", "")
        rules = request.form.get("rules", "")
        encoding = request.form.get("encoding", "").lower()
        transposition = request.form.get("transposition", "").lower()
        equation = request.form.get("equation", "")
        mode = request.form.get("mode", "encrypt")

        original_text = text
        steps.append(f"Original text: {text}")

        # Substitution logic
        if rules:
            rule_map = {}
            try:
                for rule in rules.split(","):
                    k, v = rule.split("=")
                    rule_map[k.strip()] = v.strip()
                if mode == "encrypt":
                    text = "".join([rule_map.get(c, c) for c in text])
                else:
                    reverse_map = {v: k for k, v in rule_map.items()}
                    temp = ""
                    i = 0
                    while i < len(text):
                        matched = False
                        for value in sorted(reverse_map, key=len, reverse=True):
                            if text.startswith(value, i):
                                temp += reverse_map[value]
                                i += len(value)
                                matched = True
                                break
                        if not matched:
                            temp += text[i]
                            i += 1
                    text = temp
                steps.append(f"Applied substitution rules: {rules}")
            except:
                steps.append("⚠️ Error parsing substitution rules.")

        # Encoding/Decoding
        if encoding == "base64":
            try:
                if mode == "encrypt":
                    text = base64.b64encode(text.encode()).decode()
                    steps.append("Encoded using base64")
                else:
                    text = base64.b64decode(text.encode()).decode()
                    steps.append("Decoded from base64")
            except:
                steps.append("⚠️ Error handling base64 encoding.")
        elif encoding == "reverse":
            text = text[::-1]
            steps.append("Reversed the string")

        # Transposition
        if transposition == "even-odd swap":
            transposed = list(text)
            for i in range(0, len(transposed) - 1, 2):
                transposed[i], transposed[i+1] = transposed[i+1], transposed[i]
            text = "".join(transposed)
            steps.append("Swapped even and odd indices")
        elif transposition == "reverse":
            text = text[::-1]
            steps.append("Reversed (transposition)")

        # Equation logic
        if equation:
            try:
                evaluated = ""
                for c in text:
                    value = eval(equation, {"ord": ord, "chr": chr}, {"c": c})
                    evaluated += chr(value % 256) if isinstance(value, int) else str(value)
                text = evaluated
                steps.append(f"Applied equation logic: {equation}")
            except Exception as e:
                steps.append(f"⚠️ Error in equation logic: {e}")

        result = text

    return render_template("custom.html", result=result, steps=steps)

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
