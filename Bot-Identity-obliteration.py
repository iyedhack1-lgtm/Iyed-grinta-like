from flask import Flask, request, jsonify
import httpx
import time
import concurrent.futures
from threading import Thread
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

def Encrypt_ID(x):
    x = int(x)
    dec = ['80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
    xxx = ['1', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']
    x = x / 128
    if x > 128:
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                m = (n - int(strn)) * 128
                return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
            else:
                strx = int(x)
                y = (x - int(strx)) * 128
                stry = str(int(y))
                z = (y - int(stry)) * 128
                strz = str(int(z))
                n = (z - int(strz)) * 128
                strn = str(int(n))
                return dec[int(n)] + dec[int(z)] + dec[int(y)] + xxx[int(x)]
def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()
tokens = {
'3024331833':'tbxjifgutlw6qb',
'3024362819':'n882qi53zjxhld',
'3024359352':'0x9yiwtwdv3551',
'3024357931':'wj18cv2uy845f4',
'3024326170':'b2f6w2zhw90qxf',
'3024351473':'5z29scw9g6c64f',
'3024340303':'arkiek5er2umk4',
'3024351692':'ay8kxe351jtwvr',
'3024373810':'jygey4j9r9c5fz',
'3024364655':'dolt3lji63vvxl',
'3024332926':'5etucqtylsfb2o',
'3024340628':'rnbazh4hzyj2gx',
}
jwt_tokens = {}
def get_jwt_token(uid, password):
    url = f"https://app-py-amber.vercel.app/get?uid={uid}&password={password}"
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                jwt_tokens[uid] = data['token']
                #print(f"JWT Token for UID {uid} updated successfully.")
            else:
                pass
                #print(f"Failed to get JWT token for UID {uid}: Status is not success.")
        else:
            pass
            #print(f"Failed to get JWT token for UID {uid}: HTTP {response.status_code}")
    except httpx.RequestError as e:
        print(f"Request error for UID {uid}: {e}")
def token_updater():
    while True:
        for uid, password in tokens.items():
            if uid not in jwt_tokens or time.time() - jwt_tokens.get(f"{uid}_timestamp", 0) > 8 * 3600:
                get_jwt_token(uid, password)
                jwt_tokens[f"{uid}_timestamp"] = time.time()
        time.sleep(8 * 3600)
token_thread = Thread(target=token_updater, daemon=True)
token_thread.start()
def get_player_information(player_id, uid):
    encrypted_id = Encrypt_ID(player_id)
    encrypted_api = encrypt_api(f"08{encrypted_id}1007")
    target = bytes.fromhex(encrypted_api)
    url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
    headers = {
        "Authorization": f"Bearer {jwt_tokens.get(uid)}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB47",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)",
        "Host": "clientbp.common.ggbluefox.com",
        "Connection": "close",
        "Accept-Encoding": "gzip, deflate, br",
    }
    try:
        with httpx.Client(verify=False) as client:
            response = client.post(url, headers=headers, data=target)
        if response.status_code == 200:
            return f"GOOD VISIT: {player_id} with UID {uid}"
        else:
            pass
    except httpx.RequestError as e:
        pass
@app.route('/visit', methods=['GET'])
def start_requests():
    player_id = request.args.get('uid')
    if not player_id:
        return jsonify({"status": "error", "message": "uid is required"}), 400
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = []
        for uid in tokens.keys():
            for _ in range(1):
                futures.append(executor.submit(get_player_information, player_id, uid))

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                print(result)
            except Exception as e:
                results.append(f"Exception: {e}")
    return jsonify({
        "status": "success",
        "message": f"{len(futures)} requests sent successfully",
        "results": results
    })
if __name__ == '__main__':
    for uid, password in tokens.items():
        get_jwt_token(uid, password)
    app.run(host='0.0.0.0', port=5000)