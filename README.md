## Smart Human Resources CV Analysis Candidate Segmentation System

PDF formatındaki özgeçmişleri yükleyerek otomatik analiz yapan bir web uygulaması.

Uygunluk skoru hesaplar, pozisyona göre yetkinlik eşleştirmesi yapar, deneyim seviyesini belirler ve sonuçları bir dashboard üzerinden gösterir.


https://github.com/user-attachments/assets/103f8095-5612-496a-8460-450f480f53d1


# Özellikler

- PDF özgeçmişlerden metin çıkarma
- Pozisyona özel yetkinlik eşleştirme (kural tabanlı + semantik benzerlik)
- Makine öğrenmesi tabanlı uygunluk tahmini
- Deneyim yılı çıkarma ve seviye belirleme (Junior / Mid / Senior)
- Pozisyon önerisi (kullanıcı pozisyon seçmezse)
- Açıklanabilir sonuçlar (eşleşen / eksik / ekstra yetkinlikler)
- SQLite veritabanı ile analiz geçmişinin saklanması
- Basit ve temiz dashboard (toplam aday, uygun / uygun değil oranları, pozisyon ve seviye dağılımları)

# Kullanılan Teknolojiler

- Python / Flask
- Sentence Transformers (semantik eşleştirme)
- scikit-learn (basit ML modeli)
- PyPDF2 (PDF okuma)
- SQLite (veritabanı)
