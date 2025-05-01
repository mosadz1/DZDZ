from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import os
import getpass

def encrypt_file(input_file, output_file, password):
    # توليد مفتاح من كلمة المرور باستخدام PBKDF2
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    
    # توليد متجه ابتدائي (IV)
    iv = get_random_bytes(16)
    
    # إنشاء كائن التشفير
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # قراءة الملف النصي
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # إضافة padding للنص لتكون طوله مضاعف 16
    padding_length = 16 - (len(plaintext) % 16
    plaintext += bytes([padding_length]) * padding_length
    
    # تشفير النص
    ciphertext = cipher.encrypt(plaintext)
    
    # حفظ البيانات المشفرة مع الملح والمتجه الابتدائي
    with open(output_file, 'wb') as f:
        f.write(salt)
        f.write(iv)
        f.write(ciphertext)

def decrypt_file(input_file, output_file, password):
    # قراءة البيانات المشفرة
    with open(input_file, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()
    
    # توليد المفتاح من كلمة المرور
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    
    # إنشاء كائن فك التشفير
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # فك التشفير
    plaintext = cipher.decrypt(ciphertext)
    
    # إزالة padding
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    
    # حفظ النص الأصلي
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# كيفية الاستخدام
if __name__ == "__main__":
    action = input("اختر إجراءً (1 للتشفير، 2 لفك التشفير): ")
    input_file = input("أدخل مسار الملف المدخل: ")
    output_file = input("أدخل مسار الملف المخرج: ")
    password = getpass.getpass("أدخل كلمة المرور: ")
    
    if action == "1":
        encrypt_file(input_file, output_file, password)
        print("تم تشفير الملف بنجاح!")
    elif action == "2":
        decrypt_file(input_file, output_file, password)
        print("تم فك تشفير الملف بنجاح!")
    else:
        print("إدخال غير صحيح")