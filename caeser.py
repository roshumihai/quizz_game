def encrypt(text, key=3):
    #This fnc has the role to encrypt using caesar code
    encrypted_text = ''
    for char in text:
        num = ord(char) + key
        new_char = chr(num)
        encrypted_text += new_char
    return encrypted_text


def decrypt(encrypted_text, key=3):
    # This fnc has the role to decrypt using caesar code
    decrypted_text = ''
    for char in encrypted_text:
        decrypted_text += chr(ord(char) - key)
    return decrypted_text