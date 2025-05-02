Diyabet Tahmin Uygulaması 🩺
<p align="center">
   <img src="Pictures\diyabet_ve_beslenme.jpg" alt="Resim" width="300" />
</p>

Bu proje, diyabet riskini tahmin etmek için geliştirilmiş bir Streamlit tabanlı web uygulamasıdır. Random Forest modeli kullanılarak eğitilen bu uygulama, kullanıcıların sağlık bilgilerini girerek diyabet risklerini öğrenmelerini sağlar. Proje, Pima Indian kadınlarından toplanan tıbbi verilerle eğitilmiştir ve TÜRKDIAB Diyabet Tanı ve Tedavi Rehberi 2024’ten alınan önerilerle desteklenmiştir.
📋 Proje Özeti
Bu uygulama, bireylerin diyabet riskini değerlendirmelerine yardımcı olmak amacıyla geliştirilmiştir. Kullanıcılar, sağlık bilgilerini girerek diyabet risklerini öğrenebilir ve TÜRKDIAB Rehberi’ne dayalı öneriler alabilir. Proje, hem farkındalık yaratmayı hem de bireylerin sağlık durumlarını daha iyi anlamalarını hedefler.
Veri Seti ve Değişiklikler
Projemiz, Pima Indian Diyabet Veri Seti’ni temel almıştır. Orijinal veri seti aşağıdaki sütunlardan oluşur:

Pregnancies: Gebelik sayısı
Glucose: 2 saatlik oral glikoz tolerans testindeki plazma glukoz seviyesi (mg/dL)
BloodPressure: Diyastolik kan basıncı (mmHg)
SkinThickness: Triceps deri kalınlığı (mm)
Insulin: 2 saatlik serum insülin seviyesi (µU/mL)
BMI: Vücut kitle indeksi (kg/m²)
DiabetesPedigreeFunction: Diyabet pedigrisi fonksiyonu (genetik yatkınlık skoru)
Age: Yaş (yıl)
Outcome: Diyabet durumu (0: Diyabetsiz, 1: Diyabetli)

Neler Yaptık?
Veri setini daha anlamlı hale getirmek ve modelin doğruluğunu artırmak için şu adımları uyguladık:

DiabetesPedigreeFunction sütununun adı Diyabet_Oykusu olarak değiştirildi ve 0 (ailede diyabet yok) veya 1 (ailede diyabet var) şeklinde ikili bir özelliğe dönüştürüldü. Bu, genetik yatkınlığın daha net bir şekilde modellenmesini sağladı.
Eksik veya sıfır değerler temizlendi. Örneğin, glukoz, insülin ve BMI gibi sütunlarda sıfır değerler tespit edildi ve bu değerler medyan veya uygun yöntemlerle değiştirildi.
Tıbbi aralıklar kontrol edilerek aykırı değerler sınırlandırıldı:
Glukoz: 70-200 mg/dL
İnsülin: 16-166 µU/mL
BMI: 18.5-45 kg/m²
Yaş: 21-70 yıl


Veriyi ölçeklendirmek için RobustScaler kullanıldı. Bu, aykırı değerlere karşı daha dayanıklı bir ölçeklendirme sağladı.
Veri seti dengesizdi (diyabetli ve diyabetsiz sınıflar arasında fark vardı). Bu durumu dengelemek için veri seti üzerinde dengeli bir train-test ayrımı yapıldı.

Model ve Eğitim Süreci
Modelimizi eğitmek için Random Forest algoritmasını tercih ettik. Random Forest, hem yüksek doğruluk sunması hem de özellik önem sıralamasını sağlaması açısından uygun bir seçimdir. Eğitim sürecinde şu adımları izledik:

Veri seti %80 eğitim ve %20 test olarak ayrıldı.
Hiperparametre optimizasyonu (GridSearchCV) ile en iyi parametreler bulundu:
max_depth: 8
max_features: 5
min_samples_split: 5
n_estimators: 100


Model, bu parametrelerle eğitildi ve %95.50 doğruluk oranı elde edildi.
Özellik önem sıralaması yapılarak hangi özelliklerin daha belirleyici olduğu analiz edildi (örneğin, insülin ve glukoz seviyeleri en yüksek öneme sahipti).

🌟 Özellikler

Kullanıcı Dostu Arayüz: Streamlit ile geliştirilen uygulama, kullanıcıların sağlık bilgilerini kolayca girebileceği geniş bir form sunar.

<p align="center">
   <img src="Pictures\streamlit_web_gorsel.png" alt="Uygulama Arayüzü" width="300" />
</p>


Yüksek Doğruluk: Random Forest modeli, %95.50 doğruluk oranıyla diyabet riskini tahmin eder.
Tıbbi Öneriler: TÜRKDIAB Diyabet Tanı ve Tedavi Rehberi 2024’e dayalı öneriler sunar (örneğin, glukoz seviyesinin kontrol edilmesi gerektiği durumlarda).
Özellik Önemi: Modelin hangi özelliklere daha fazla önem verdiği, sıralı bir grafikle gösterilir.
Güvenli Girdi Kontrolü: Tıbbi aralıklarla sınırlandırılmış girişler sayesinde hatalı veri girişi önlenir.

🛠️ Kurulum
Gereksinimler

Python 3.11 veya üstü
Gerekli Python kütüphaneleri: streamlit, pandas, joblib, matplotlib, seaborn, scikit-learn

Kurulum Adımları

Bu depoyu klonlayın:
git clone https://github.com/kullaniciadi/diyabet-tahmin-uygulamasi.git
cd diyabet-tahmin-uygulamasi

(kullaniciadi kısmını kendi GitHub kullanıcı adınızla değiştirin.)

Gerekli kütüphaneleri yükleyin:
pip install streamlit pandas joblib matplotlib seaborn scikit-learn


Uygulamayı başlatın:
streamlit run streamlit_app.py



📊 Model Performansı

Test Seti Doğruluğu: 0.9550
Diyabetsiz (Precision/Recall/F1): 0.97 / 0.94 / 0.95
Diyabetli (Precision/Recall/F1): 0.94 / 0.97 / 0.96

Bu metrikler, modelin hem diyabetli hem de diyabetsiz sınıfları yüksek doğrulukla tahmin ettiğini gösterir.
⚠️ Önemli Notlar

Bu uygulama bir tanı aracı değildir. Tahmin sonuçlarınızı bir doktorla değerlendirin.
Daha fazla bilgi için TÜRKDIAB Diyabet Tanı ve Tedavi Rehberi 2024 dökümanını inceleyebilirsiniz.
Triceps deri kalınlığı, obeziteyle doğrudan ilişkilidir ve diyabet riskini değerlendirmede önemli bir ölçüttür.

📖 Kullanım

Uygulamayı başlattıktan sonra sol tarafta yer alan formu doldurun.
Gebelik sayısı, glukoz seviyesi, kan basıncı, triceps deri kalınlığı, insülin seviyesi, BMI, diyabet öyküsü ve yaş bilgilerinizi girin.
"Tahmin Yap" butonuna tıklayın.
Tahmin sonucunuzu ve olasılıklarınızı sağ tarafta göreceksiniz. Diyabet riski tespit edilirse, TÜRKDIAB Rehberi’ne dayalı öneriler sunulacaktır.
Özellik önem grafiği, hangi sağlık özelliklerinin tahmin için daha önemli olduğunu gösterir.

📜 Lisans
Bu proje, MIT Lisansı altında lisanslanmıştır. Aşağıdaki şartlar geçerlidir:
MIT License
Copyright (c) 2025 Emre Engin
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
📬 İletişim
Proje ile ilgili sorularınız veya önerileriniz için GitHub Issues üzerinden iletişime geçebilirsiniz.

Bu proje, diyabet farkındalığını artırmak ve bireylerin sağlık durumlarını değerlendirmelerine yardımcı olmak için geliştirilmiştir. 🚀
