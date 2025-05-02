import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


st.write("Model yükleniyor...")
try:
    model = joblib.load('diabetes_rf_model.pkl')
    scaler = joblib.load('scaler.pkl')
    st.write("Model ve scaler başarıyla yüklendi.")
except Exception as e:
    st.error(f"Model veya scaler yüklenirken hata oluştu: {e}")
    st.stop()


st.title("🩺 Diyabet Tahmin Uygulaması")
st.write("Bu uygulama, Random Forest modeli kullanarak diyabet riskinizi tahmin eder. Sağlık bilgilerinizi girerek risk durumunuzu öğrenebilirsiniz.")


medical_bounds = {
    'Glucose': (70.0, 200.0),
    'BloodPressure': (60.0, 90.0),
    'SkinThickness': (10.0, 40.0),
    'Insulin': (16.0, 166.0),
    'BMI': (18.5, 45.0),
    'Diyabet_Oykusu': (0.0, 1.0),
    'Pregnancies': (0.0, 10.0),
    'Age': (21.0, 70.0)
}

st.sidebar.header("📋 Hasta Bilgilerini Girin")
st.sidebar.write("Lütfen aşağıdaki bilgileri dikkatle girin. Tıbbi aralıklar otomatik olarak kontrol edilir.")
pregnancies = st.sidebar.number_input("Gebelik Sayısı (Pregnancies)", min_value=0, max_value=10, value=0, help="Kaç kez hamile kaldınız? (Maksimum 10)")
glucose = st.sidebar.number_input("Glukoz Seviyesi (mg/dL)", min_value=70.0, max_value=200.0, value=70.0, help="2 saatlik oral glikoz tolerans testindeki plazma glukoz seviyesi.")
blood_pressure = st.sidebar.number_input("Kan Basıncı (mmHg)", min_value=60.0, max_value=90.0, value=72.0, help="Diyastolik kan basıncı (mmHg).")
skin_thickness = st.sidebar.number_input("Triceps Deri Kalınlığı (mm)", min_value=10.0, max_value=40.0, value=28.0, help="Triceps deri kalınlığı, obeziteyle ilişkili bir ölçümdür.")
insulin = st.sidebar.number_input("İnsülin Seviyesi (µU/mL)", min_value=16.0, max_value=166.0, value=20.0, help="2 saatlik serum insülin seviyesi (µU/mL).")
bmi = st.sidebar.number_input("Vücut Kitle İndeksi (BMI)", min_value=18.5, max_value=45.0, value=31.95, help="Vücut kitle indeksi (kg/m²).")
diyabet_oykusu = st.sidebar.selectbox("Diyabet Öyküsü (Diyabet_Oykusu)", options=[0, 1], index=0, help="Ailede diyabet öyküsü: 0 (Yok), 1 (Var).")
age = st.sidebar.number_input("Yaş (Age)", min_value=21, max_value=70, value=29, help="Yaşınız (yıl).")


def prepare_input_data(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diyabet_oykusu, age):
    data = {
        'Pregnancies': min(max(pregnancies, medical_bounds['Pregnancies'][0]), medical_bounds['Pregnancies'][1]),
        'Glucose': min(max(glucose, medical_bounds['Glucose'][0]), medical_bounds['Glucose'][1]),
        'BloodPressure': min(max(blood_pressure, medical_bounds['BloodPressure'][0]), medical_bounds['BloodPressure'][1]),
        'SkinThickness': min(max(skin_thickness, medical_bounds['SkinThickness'][0]), medical_bounds['SkinThickness'][1]),
        'Insulin': min(max(insulin, medical_bounds['Insulin'][0]), medical_bounds['Insulin'][1]),
        'BMI': min(max(bmi, medical_bounds['BMI'][0]), medical_bounds['BMI'][1]),
        'Diyabet_Oykusu': min(max(diyabet_oykusu, medical_bounds['Diyabet_Oykusu'][0]), medical_bounds['Diyabet_Oykusu'][1]),
        'Age': min(max(age, medical_bounds['Age'][0]), medical_bounds['Age'][1])
    }
    if glucose != data['Glucose']:
        st.warning(f"Glukoz değeri tıbbi aralıklarla sınırlandırıldı: {data['Glucose']}")
    if insulin != data['Insulin']:
        st.warning(f"İnsülin değeri tıbbi aralıklarla sınırlandırıldı: {data['Insulin']}")
    if skin_thickness != data['SkinThickness']:
        st.warning(f"Deri kalınlığı değeri tıbbi aralıklarla sınırlandırıldı: {data['SkinThickness']}")
    if pregnancies != data['Pregnancies']:
        st.warning(f"Gebelik sayısı tıbbi aralıklarla sınırlandırıldı: {data['Pregnancies']}")
    if age != data['Age']:
        st.warning(f"Yaş tıbbi aralıklarla sınırlandırıldı: {data['Age']}")
    input_df = pd.DataFrame([data])
    input_scaled = scaler.transform(input_df)
    return pd.DataFrame(input_scaled, columns=input_df.columns)


if st.sidebar.button("Tahmin Yap"):
    input_data = prepare_input_data(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diyabet_oykusu, age)
    prediction_proba = model.predict_proba(input_data)[0]
    prediction = 1 if prediction_proba[1] >= 0.5 else 0

   
    st.header("Tahmin Sonucu")
    if prediction == 0:
        st.success("Diyabetsiz (No Diabetes)")
        st.write("Diyabet riski tespit edilmedi. Sağlıklı yaşam tarzına devam edin! TÜRKDIAB Rehberi'ne göre düzenli egzersiz ve dengeli beslenme önerilir.")
    else:
        st.error("Diyabetli (Diabetes)")
        st.write("Diyabet riski tespit edildi. Lütfen bir doktora danışın ve düzenli tarama yaptırın. TÜRKDIAB Rehberi'ne göre glukoz seviyenizi kontrol ettirin (APG ≥ 126 mg/dl diyabet).")

    
    st.subheader("Tahmin Olasılıkları")
    st.write(f"Diyabetsiz Olasılığı: {prediction_proba[0]:.2f}")
    st.write(f"Diyabetli Olasılığı: {prediction_proba[1]:.2f}")

   
    st.subheader("Özelliklerin Önemi (Sıralı Grafik)")
    feature_importances = {'Insulin': 0.480, 'SkinThickness': 0.141, 'Glucose': 0.137, 'BMI': 0.070, 'Age': 0.067, 'Diyabet_Oykusu': 0.042, 'Pregnancies': 0.031, 'BloodPressure': 0.030}
    features = list(feature_importances.keys())
    importances = list(feature_importances.values())
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.barplot(x=importances, y=features, ax=ax, palette='viridis')
    ax.set_title("Feature Importance (Sıralı)")
    ax.set_xlabel("Importance Score")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)


st.sidebar.header("ℹ️ Uygulama Hakkında")
st.sidebar.write("""
Bu uygulama, diyabet riskini tahmin etmek için geliştirilmiştir. Random Forest modeli, Pima Indian kadınlarından toplanan tıbbi verilerle (%95.50 doğruluk oranıyla) eğitilmiştir. Model, aşağıdaki özelliklere dayanır:

- **Gebelik Sayısı**: Daha fazla gebelik, gestasyonel diyabet riskini artırabilir.
- **Glukoz Seviyesi**: Açlık plazma glukozu, diyabet tanısında kritik bir göstergedir (TÜRKDIAB: ≥ 126 mg/dl diyabet).
- **Kan Basıncı**: Yüksek tansiyon, diyabetle ilişkilidir (TÜRKDIAB: ≥ 140/90 mmHg risk faktörü).
- **Triceps Deri Kalınlığı**: Obeziteyle doğrudan ilişkilidir. Triceps bölgesindeki deri kalınlığı, vücuttaki yağ dağılımını gösterir ve diyabet riskini değerlendirmede önemli bir ölçüttür.
- **İnsülin Seviyesi**: İnsülin direnci, Tip 2 diyabetin erken bir göstergesidir.
- **BMI**: Vücut kitle indeksi, obeziteyi ölçer (TÜRKDIAB: ≥ 25 kg/m² risk faktörü).
- **Diyabet Öyküsü**: Ailede diyabet varlığı genetik yatkınlığı gösterir.
- **Yaş**: 45 yaş üstü bireylerde diyabet riski artar.

**Not**: Bu tahmin bir tanı değildir. Sonuçlarınızı bir doktorla değerlendirin ve TÜRKDIAB Diyabet Tanı ve Tedavi Rehberi 2024’ü inceleyin.
""")


st.sidebar.subheader("📊 Model Performansı")
st.sidebar.write("**Test Seti Doğruluğu:** 0.9550")
st.sidebar.write("**Diyabetsiz (Precision/Recall/F1):** 0.97 / 0.94 / 0.95")
st.sidebar.write("**Diyabetli (Precision/Recall/F1):** 0.94 / 0.97 / 0.96")
st.sidebar.write("""
Bu metrikler, modelin hem diyabetli hem de diyabetsiz sınıfları yüksek doğrulukla tahmin ettiğini gösterir. Precision, doğru tahmin oranını; Recall, gerçek pozitiflerin yakalanma oranını; F1-Score ise bu ikisinin dengesini temsil eder.
""")