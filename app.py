from flask import Flask, render_template, request, jsonify
from saes_crypto.saes_engine import encrypt_with_logs, decrypt_with_logs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_saes():
    data = request.get_json()
    
    input_bin_str = data.get('input_data', '').replace(' ', '')
    key_bin_str = data.get('key', '').replace(' ', '')
    mode = data.get('mode', 'encrypt')
    
    if len(input_bin_str) != 16 or len(key_bin_str) != 16:
        return jsonify({"error": "Input data dan kunci harus tepat bernilai biner 16-bit!"}), 400
        
    try:
        input_val = int(input_bin_str, 2)
        key_val = int(key_bin_str, 2)
    except ValueError:
        return jsonify({"error": "Format input harus berupa angka biner (0 atau 1)!"}), 400
        
    if mode == 'encrypt':
        result_val, subkeys, logs = encrypt_with_logs(input_val, key_val)
    else:
        result_val, subkeys, logs = decrypt_with_logs(input_val, key_val)
        
    subkeys_hex = [hex(k)[2:].upper().zfill(4) for k in subkeys]
    result_bin = bin(result_val)[2:].zfill(16)
    result_hex = hex(result_val)[2:].upper().zfill(4)
    
    return jsonify({
        "result_bin": f"{result_bin[:4]} {result_bin[4:8]} {result_bin[8:12]} {result_bin[12:]}",
        "result_hex": result_hex,
        "subkeys": {
            "K0": subkeys_hex[0],
            "K1": subkeys_hex[1],
            "K2": subkeys_hex[2]
        },
        "logs": logs
    })

if __name__ == '__main__':
    app.run(debug=True)