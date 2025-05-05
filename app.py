import streamlit as st
import pandas as pd

import joblib

import numpy as np

from prometheus_client import Counter, Histogram, start_http_server, REGISTRY
import time
import socket
import os


METRIC_NAMES = ['diabetes_prediction_requests_total', 'diabetes_prediction_duration_seconds']

for name in list(REGISTRY._names_to_collectors.keys()):
    if name in METRIC_NAMES:
        collector = REGISTRY._names_to_collectors[name]
        REGISTRY.unregister(collector)


if os.getenv('KUBERNETES_SERVICE_HOST'):
    print("Kubernetes ortamında çalışıyorum, Prometheus başlatılıyor.")
    start_http_server(8001) 
else:
    print("Yerel ortamda çalışıyorum, Prometheus başlatılmadı.")

prediction_counter = Counter('diabetes_prediction_requests_total', 'Total number of prediction requests')
prediction_duration = Histogram('diabetes_prediction_duration_seconds', 'Duration of prediction requests in seconds')



model = joblib.load('diabetes_rf_model.pkl')
scaler = joblib.load('scaler.pkl')


st.set_page_config(layout="centered")
st.markdown(
    """
    <style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 5px;
    }
    h1 {
        color: #4a90e2;
        font-size: 48px;
        text-align: center;
        margin-bottom: 15px;
    }
    h2 {
        color: #6abf69;
        font-size: 36px;
        text-align: center;
        margin-top: 25px;
    }

    /* Input grupları */
    .input-group {
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        text-align: left;
    }

    .input-group label {
        font-size: 22px;
        color: #d46b9e;
        font-weight: bold;
        display: block;
        margin-bottom: 2px;
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 2px;
    }

    .input-group .description {
        font-size: 16px;
        color: #5a9bd5;
        margin-bottom: 2px;
        display: block;
    }

    .input-group input {
        font-size: 18px;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #4a90e2;
        background-color: #ffffff;
        width: 100%;
        box-sizing: border-box; /* İçerik kutuya sığar */
    }

    .stButton>button {
        width: 250px;
        height: 50px;
        font-size: 22px;
        background-color: #4a90e2;
        color: white;
        border-radius: 5px;
        border: none;
        display: block;
        margin: 30px auto;
    }

    .stButton>button:hover {
        background-color: #357abd;
    }

    .info-box {
        background-color: #f0f7fd;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-size: 18px;
        color: #5a9bd5;
        text-align: center;
    }

    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
        font-size: 24px;
        color: #2e7d32;
        text-align: center;
    }

    .warning-box {
        background-color: #fce4d6;
        padding: 15px;
        border-radius: 5px;
        margin-top: 15px;
        font-size: 24px;
        color: #bf360c;
        text-align: center;
    }

    @media (max-width: 600px) {
        .input-group {
            max-width: 100%;
        }

        .input-group label {
            font-size: 20px;
        }

        .input-group .description {
            font-size: 14px;
        }

        .input-group input {
            font-size: 16px;
            padding: 8px;
        }

        .stButton>button {
            width: 100%;
            height: 45px;
            font-size: 20px;
        }

        h1 {
            font-size: 36px;
        }

        h2 {
            font-size: 28px;
        }

        .info-box, .success-box, .warning-box {
            font-size: 16px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title('Diyabet Tahmin Uygulaması 🩺')
st.markdown(
    '<p style="text-align: center; font-size: 24px;">Bu uygulama, Random Forest modeli kullanarak sağlık bilgilerinizi analiz eder ve diyabet riskinizi tahmin eder. Sonuçlar yalnızca genel bir bilgi sunar.</p>',
    unsafe_allow_html=True
)


st.markdown(
    '<div style="text-align: center; font-size: 20px; color: #2e6da4; background-color: #e6f3fa; padding: 15px; border-radius: 5px; margin-bottom: 25px;">'
    'Diyabet, kan şekerinin yükselmesiyle (hiperglisemi) oluşan kronik bir hastalıktır. Açlık kan şekeri 126 mg/dL üzeri veya toklukta 200 mg/dL üzeri diyabet belirtisi olabilir.'
    '</div>',
    unsafe_allow_html=True
)


st.header('Hasta Bilgileri Girişi')
col1, col2 = st.columns(2)

def render_input_group(label_text, description_text, key_suffix, min_val, max_val, default_val):
    st.markdown(f"""
        <div class="input-group">
            <label>{label_text}</label>
            <div class="description">{description_text}</div>
        </div>
    """, unsafe_allow_html=True)
    return st.number_input('', min_value=min_val, max_value=max_val, value=default_val, key=key_suffix)

with col1:
    pregnancies = render_input_group("Gebelik Sayısı", "Gebelik sayınızı girin (0-20).", 'pregnancies', 0, 20, 0)
    glucose = render_input_group("Açlık Glukoz Seviyesi (mg/dL)", "Sabah aç karnına ölçüm yapın (örneğin, 70-200 mg/dL).", 'glucose', 70.0, 200.0, 90.0)
    skin_thickness = render_input_group("Triceps Deri Kalınlığı (mm)", "Kolunuzun arka kısmındaki deri kalınlığı (kumpas ile ölçülür).", 'skin_thickness', 0.0, 100.0, 20.0)
    bmi = render_input_group("Vücut Kitle İndeksi (BMI) (kg/m²)", "Kilonuz (kg) / boyunuzun (m) karesi (18.5-45).", 'bmi', 18.5, 45.0, 25.0)

with col2:
    blood_pressure = render_input_group("Kan Basıncı (mmHg)", "Diyastolik kan basıncı (örneğin, 60-90 mmHg).", 'blood_pressure', 0.0, 150.0, 70.0)
    insulin = render_input_group("İnsülin Seviyesi (µU/mL)", "2 saatlik insülin seviyenizi girin (16-166 µU/mL).", 'insulin', 16.0, 166.0, 50.0)
    diabetes_pedigree = render_input_group("Diyabet Öyküsü (0: Yok, 1: Var)", "Ailenizde diyabet varsa 1, yoksa 0.", 'diabetes_pedigree', 0.0, 1.0, 0.0)
    age = render_input_group("Yaş (yıl)", "Yaşınızı yıl cinsinden girin (21-70).", 'age', 21, 70, 30)


if st.button('Tahmin Et'):
    prediction_counter.inc()  
    start_time = time.time()  

  
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]])
    input_data_scaled = scaler.transform(input_data)
   
    prediction = model.predict(input_data_scaled)

    
    duration = time.time() - start_time
    prediction_duration.observe(duration)


    if prediction[0] == 0:
        st.markdown('<div class="success-box">Tahmin Sonucu: Diyabet Yok</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="info-box">Diyabet riski düşük görünüyor. Sağlıklı yaşam tarzına devam edin ve düzenli kontrol yaptırın.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="info-box">'
            '<b>Uzman Önerileri:</b> Dengeli beslenin: Tam tahıllı gıdalar, sebzeler, meyveler ve sağlıklı yağlar (zeytinyağı gibi) tüketin. Şekerli içecekler ve işlenmiş gıdalardan kaçının. '
            'Günde 30 dakika yürüyüş veya bisiklet gibi orta düzeyde egzersiz yapın. Sigara ve alkolü bırakın, D vitamini takviyesi alın. Stres için meditasyon veya yoga uygulayın, 7-8 saat uyuyun. '
            'Yılda bir kan testi ile sağlık kontrolü yaptırın.'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="warning-box">Tahmin Sonucu: Diyabet Riski Var</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="warning-box">Bu bir model tahminidir, lütfen bir uzmana danışın.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="info-box">'
            '<b>Uzman Önerileri:</b> Karbonhidrat alımını azaltın (beyaz ekmek ve tahıllı gıdalardan uzak durun), şekerli içeceklerden kaçının, düzenli yürüyüş yapın (günde 30 dakika), '
            'stres yönetimi için meditasyon veya yoga uygulayın, D vitamini takviyesi alın ve bir diyetisyen desteğiyle sağlıklı bir yaşam tarzı benimseyin.'
            '</div>',
            unsafe_allow_html=True
        )

    
    st.markdown(
        '<div class="info-box">'
        '<b>Not:</b> Bu araç teşhis koymaz, yalnızca tahmini bir değerlendirme sunar. Türkiye Diyabet Vakfı Rehberi 2024’e göre, açlık glukoz seviyesi 126 mg/dL üzeri veya BMI 30 üzerindeyse bir uzmana danışılmalıdır.'
        '</div>',
        unsafe_allow_html=True
    )