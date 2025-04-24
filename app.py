from flask import Flask, render_template, jsonify, request
import json
import requests
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# API OpenWeatherMap (punya kamu)
API_KEY = '20ab31b3b8cff36e764b8b7814e1be5e'

# Data Profil
profil = {
    "nama": "Abdila Asy Syafiq",
    "deskripsi": "Web Developer | Portfolio",
    "kontak": {
        "email": "dilcuyyz@gmail.com",
        "linkedin": "https://www.linkedin.com/in/abdila-asy-syafiq"
    },
    "project": [
        {
            "nama": "Project 1",
            "deskripsi": "Website E-Commerce Hijab Saya.",
            "gambar": "project1.png",
            "link": "https://dilcuyy.github.io/Alsaahir/"
        },
        {
            "nama": "Project 2",
            "deskripsi": "Portofolio pertama saya.",
            "gambar": "project2.png",
            "link": "https://dilcuyy.github.io/My-LinkTree/Portofolio.html"
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html', profil=profil)

def get_weather(location):
    if location == 'Pekayon':
        lat, lon = -6.2615, 106.9831
    elif location == 'Mustikajaya':
        lat, lon = -6.2883, 107.0132
    else:
        return "Lokasi tidak dikenal."

    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        return f"Gagal ambil data. Status: {response.status_code}, Pesan: {response.json().get('message')}"

    data = response.json()

    main_weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"Cuaca di {location} saat ini: {main_weather}, suhu {temp}°C."

def get_time():
    # WIB = UTC+7
    wib = timezone(timedelta(hours=7))
    now = datetime.now(wib)
    return now.strftime("Sekarang pukul %H:%M:%S WIB, tanggal %d-%m-%Y.")

@app.route('/chatbot')
def chatbot():
    user_message = request.args.get('message', '').lower()

    if "halo" in user_message:
        response = "Halo juga, ada yang bisa dibantu?"
    elif "siapa kamu" in user_message:
        response = "Saya adalah chatbot dari portofolio Abdila Asy Syafiq."
    elif "project" in user_message:
        response = "Saya sedang mengerjakan beberapa project menarik! Cek di bagian project di halaman ini."
    elif "terima kasih" in user_message:
        response = "Sama-sama! Senang bisa membantu."
    elif "bagaimana kabarmu" in user_message:
        response = "Saya baik-baik saja, terima kasih sudah bertanya!"
    elif "kapan website ini dibuat" in user_message:
        response = "Website ini dibuat sebagai bagian dari portofolio saya. Dibuat pada tahun 2025."
    elif "dimana kamu tinggal" in user_message:
        response = "Sebagai chatbot, saya tidak tinggal di tempat tertentu. Saya ada di server web!"
    elif "siapa pembuat website ini" in user_message:
        response = "Website ini dibuat oleh Abdila Asy Syafiq sebagai portofolio pribadi."
    elif "apa bahasa pemrograman yang digunakan" in user_message:
        response = "Website ini dibangun dengan menggunakan Python (Flask) dan HTML/CSS untuk frontend."
    elif "bisa bantu apa" in user_message:
        response = "Tentu! Saya bisa memberikan informasi tentang project saya, kontak saya, waktu saat ini, dan cuaca di sekitar Pekayon atau Mustikajaya."
    elif "siapa pacar abdil" in user_message:
        response = "Pacar abdil adalah Christin Latip, dia cantik banget."
    elif "hehe" in user_message:
        response = "hahahahaha lucu ya."
    elif "kontak" in user_message:
        response = """
        Berikut adalah informasi kontak saya:
        <br><br>
        <strong>Email:</strong> dilcuyyz@gmail.com<br>
        <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/abdila-asy-syafiq" target="_blank">Abdila A..</a><br>
        <strong>GitHub:</strong> <a href="https://github.com/abdilaasyy" target="_blank">dilcuyy</a><br>
        <strong>Twitter:</strong> <a href="https://x.com/@dil_1907" target="_blank">@dil_1907</a><br>
        <strong>Instagram:</strong> <a href="https://www.instagram.com/a.dilasy" target="_blank">a.dilasy</a>
        """
    elif "cuaca" in user_message:
        response = "Silakan pilih lokasi: Pekayon atau Mustikajaya."
    elif "pekayon" in user_message:
        response = get_weather("Pekayon")
    elif "mustikajaya" in user_message:
        response = get_weather("Mustikajaya")
    elif "waktu" in user_message or "jam" in user_message:
        response = get_time()
    else:
        response = "Maaf, saya tidak mengerti pertanyaan Anda."

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

