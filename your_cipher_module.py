# Cipher Module - Contains all logic, descriptions, and categorization for use in GUI

import base64
import urllib.parse
import quopri

# --- Cipher Logic Functions ---
def caesar_encrypt(text, shift=3):
    result = []
    steps = []
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            steps.append(f"{char} -> {new_char}")
            result.append(new_char)
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def atbash_encrypt(text):
    result = []
    steps = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            translated = chr(base + (25 - (ord(char) - base)))
            steps.append(f"{char} -> {translated}")
            result.append(translated)
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def rot13_encrypt(text):
    result = []
    steps = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            rotated = chr((ord(char) - base + 13) % 26 + base)
            steps.append(f"{char} -> {rotated}")
            result.append(rotated)
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def vigenere_encrypt(text, key, decrypt=False):
    result = []
    steps = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            shift = -shift if decrypt else shift
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            steps.append(f"{char} using {key[key_index % len(key)]} -> {new_char}")
            result.append(new_char)
            key_index += 1
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def morse_encrypt(text):
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', '0': '-----', ' ': '/'
    }
    result = []
    steps = []
    for char in text.upper():
        morse = MORSE_CODE_DICT.get(char, '')
        result.append(morse)
        steps.append(f"{char} -> {morse}")
    return ' '.join(result), steps

def base64_encrypt(text):
    encoded = base64.b64encode(text.encode()).decode()
    return encoded, [f"Base64 encoded: {encoded}"]

def binary_encrypt(text):
    result = ' '.join(format(ord(char), '08b') for char in text)
    return result, [f"{char} -> {format(ord(char), '08b')}" for char in text]

def hex_encrypt(text):
    result = ' '.join(format(ord(char), '02x') for char in text)
    return result, [f"{char} -> {format(ord(char), '02x')}" for char in text]

def url_encode_encrypt(text):
    encoded = urllib.parse.quote(text)
    return encoded, [f"URL Encoded: {encoded}"]

def quoted_printable_encrypt(text):
    encoded = quopri.encodestring(text.encode()).decode()
    return encoded, [f"Quoted-printable: {encoded}"]

def base32_encrypt(text):
    encoded = base64.b32encode(text.encode()).decode()
    return encoded, [f"Base32 encoded: {encoded}"]

def base85_encrypt(text):
    encoded = base64.b85encode(text.encode()).decode()
    return encoded, [f"Base85 encoded: {encoded}"]

def ascii_code_encrypt(text):
    result = ' '.join(str(ord(char)) for char in text)
    return result, [f"{char} -> {ord(char)}" for char in text]

def unicode_escape_encrypt(text):
    result = text.encode('unicode_escape').decode()
    return result, [f"{char} -> {repr(char.encode('unicode_escape'))[2:-1]}" for char in text]

def rot47_encrypt(text):
    result = []
    steps = []
    for char in text:
        if 33 <= ord(char) <= 126:
            new_char = chr(33 + ((ord(char) + 14) % 94))
            steps.append(f"{char} -> {new_char}")
            result.append(new_char)
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def reverse_alphabet_encrypt(text):
    result = []
    steps = []
    for char in text:
        if char.isupper():
            new_char = chr(ord('Z') - (ord(char) - ord('A')))
            steps.append(f"{char} -> {new_char}")
            result.append(new_char)
        elif char.islower():
            new_char = chr(ord('z') - (ord(char) - ord('a')))
            steps.append(f"{char} -> {new_char}")
            result.append(new_char)
        else:
            steps.append(f"{char} unchanged")
            result.append(char)
    return ''.join(result), steps

def text_inversion_encrypt(text):
    result = text[::-1]
    return result, [f"Text reversed: {result}"]

def emoji_cipher_encrypt(text):
    base_emoji = 0x1F600  # 😀
    result = []
    steps = []
    for i, char in enumerate(text):
        emoji = chr(base_emoji + (ord(char) % 80))
        result.append(emoji)
        steps.append(f"{char} -> {emoji}")
    return ''.join(result), steps

# --- Cipher Function Mapping ---
cipher_functions = {
    'Classical:Caesar Cipher (Shift 3)': caesar_encrypt,
    'Classical:Atbash Cipher': atbash_encrypt,
    'Classical:ROT13 Cipher': rot13_encrypt,
    'Classical:Vigenère Cipher (Key=KEY)': vigenere_encrypt,
    'Encoding:Morse Code': morse_encrypt,
    'Encoding:Base64': base64_encrypt,
    'Encoding:Binary': binary_encrypt,
    'Encoding:Hexadecimal': hex_encrypt,
    'Encoding:URL Encoding': url_encode_encrypt,
    'Encoding:Quoted-Printable': quoted_printable_encrypt,
    'Encoding:Base32': base32_encrypt,
    'Encoding:Base85': base85_encrypt,
    'Encoding:ASCII Code': ascii_code_encrypt,
    'Encoding:Unicode Escape': unicode_escape_encrypt,
    'Obfuscation:ROT47': rot47_encrypt,
    'Obfuscation:Reverse Alphabet': reverse_alphabet_encrypt,
    'Obfuscation:Text Inversion': text_inversion_encrypt,
    'Encoding:Emoji Cipher': emoji_cipher_encrypt
}

# --- Descriptions for GUI Tooltip or Help Text ---
cipher_descriptions = {
    'Classical:Caesar Cipher (Shift 3)': "Shifts each letter by 3 places in the alphabet. Non-letters are unchanged.",
    'Classical:Atbash Cipher': "Replaces each letter with its counterpart from the opposite side of the alphabet.",
    'Classical:ROT13 Cipher': "Each letter is rotated 13 positions in the alphabet. It's symmetric, applying twice restores the original.",
    'Classical:Vigenère Cipher (Key=KEY)': "Uses a repeating keyword to shift letters using Caesar ciphers with different shifts.",
    'Encoding:Morse Code': "Converts letters and numbers into sequences of dots and dashes.",
    'Encoding:Base64': "Encodes text into a base-64 representation, often used in data transmission.",
    'Encoding:Binary': "Represents each character using an 8-bit binary code.",
    'Encoding:Hexadecimal': "Encodes characters as their hexadecimal ASCII values.",
    'Encoding:URL Encoding': "Encodes special characters in URLs using percent-encoding.",
    'Encoding:Quoted-Printable': "Used in email to encode special or non-ASCII characters safely.",
    'Encoding:Base32': "Encodes data using 32-character representation. More space-efficient than Base64 for some applications.",
    'Encoding:Base85': "Encodes binary data into ASCII characters using base-85 representation.",
    'Encoding:ASCII Code': "Converts each character into its ASCII numerical representation.",
    'Encoding:Unicode Escape': "Encodes characters using Python's unicode escape format (e.g., \\uXXXX).",
    'Obfuscation:ROT47': "Rotates visible ASCII characters by 47 places. Useful for simple text obfuscation.",
    'Obfuscation:Reverse Alphabet': "Maps A⇔Z, B⇔Y, etc., flipping letters around the alphabet.",
    'Obfuscation:Text Inversion': "Reverses the entire input string.",
    'Encoding:Emoji Cipher': "Converts each character to a pseudo-random emoji based on its code point."
}

# --- Export Formatting Function ---
def format_output(cipher_name, input_text, output_text, steps):
    description = cipher_descriptions.get(cipher_name, "")
    lines = [
        f"Cipher Used: {cipher_name}",
        f"Description: {description}",
        f"Input Text: {input_text}",
        f"Output Text: {output_text}",
        "\nSteps:",
        *steps
    ]
    return "\n".join(lines)