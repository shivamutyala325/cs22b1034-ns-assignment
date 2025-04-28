from flask import Flask, render_template, request
import pyDes

app = Flask(__name__)

def des_encrypt(data, key):
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    encrypted_data = des.encrypt(data)
    return encrypted_data.hex()  # Return as hex string for display

def des_decrypt(data, key):
    des = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    decrypted_data = des.decrypt(bytes.fromhex(data))
    return decrypted_data.decode()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    message = request.form['message']
    key = request.form['key']
    operation = request.form['operation']
    result = ''

    if len(key) != 8:
        result = "Key must be exactly 8 characters long."
    else:
        try:
            if operation == 'encrypt':
                result = des_encrypt(message, key)
            else:
                result = des_decrypt(message, key)
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
