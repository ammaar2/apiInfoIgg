from fastapi import FastAPI, HTTPException
import requests
import base64
from user_agent import generate_user_agent as gen
import uuid
import random

def rest(email):
    crf = "".join(random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(32))
    url = 'https://i.instagram.com/api/v1/accounts/send_password_reset/'
    hed = {
        'Content-Length': '323',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Instagram 6.12.1 Android (30/11; 320dpi; 720x1339; realme; RMX3269; RED8F6; RMX3265; ar_IQ)',
        'Cookie': f'mid=Z0ZQoQABAAFHk8B-qvDkQ4bq_XLc; csrftoken={crf}',
        'Cookie2': '$Version=1',
        'Accept-Language': 'ar-IQ, en-US',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': 'AQ==',
        'Accept-Encoding': 'gzip'
    }
    da = {
        'user_email': email,
        'device_id': str(uuid.uuid4()),
        'guid': str(uuid.uuid4()),
        '_csrftoken': crf
    }
    res = requests.post(url, headers=hed, data=da).json()['obfuscated_email']
    return res

app = FastAPI()

@app.get("/InfoIG/{username}")
def get_insta_hit(username: str):
    try:
        # إنشاء السلسلة المشفرة باستخدام Base64
        oo = f"-1::{username}"
        ee = base64.b64encode(oo.encode('utf-8')).decode('utf-8')

        # تهيئة الهيدر المطلوب باستخدام مكتبة user_agent
        headers = {
            'user-agent': str(gen())
        }

        # إرسال الطلب إلى API الخارجي
        url = f'https://instanavigation.net/api/v1/stories/{ee}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # التأكد من نجاح الطلب

        rr = response.json()

        # استخراج معلومات المستخدم من الاستجابة
        user_info = rr.get('user_info')
        # استدعاء دالة rest باستخدام البريد الإلكتروني المبني على اسم المستخدم
        resp = rest(username + "@gmail.com")

        if not user_info:
            raise HTTPException(status_code=404, detail="لم يتم العثور على معلومات")

        result = {
            "id": user_info.get("id"),
            "full_name": user_info.get("full_name"),
            "username": username,
            "email": f"{username}@gmail.com",
            "followers": user_info.get("followers"),
            "following": user_info.get("following"),
            "is_private": user_info.get("is_private"),
            "posts": user_info.get("posts"),
            "rest": resp,
            "url": f"https://www.instagram.com/{username}/",
            "By": "@jokerpython3"
        }

        return result

    except requests.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
