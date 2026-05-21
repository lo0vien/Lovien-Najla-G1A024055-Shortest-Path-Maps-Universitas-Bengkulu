# Shortest Path Universitas Bengkulu – Artificial Intellegent

Halo Saya Lovien Najla Dhafiyah, mahasiswi Universitas Bengkulu Program Studi Informatika Angkatan 2024 dengan NPM G1A024055. Project ini dibuat sebagai bagian dari pemenuhan tugas UTS dan UAS mata kuliah Artificial Intellegent. Project ini merupakan sistem pencarian jalur tercepat (Shortest Path) di lingkungan Universitas Bengkulu dengan menggunakan algoritma Dijkstar. Sistem dapat membantu pengguna menentukan rute tercepat antar lokasi kampus secara interaktif menggunakan peta digital.

---

## Deskripsi Project

Sistem ini dirancang untuk menghitung dan menampilkan rute tercepat antar lokasi di kawasan Universitas Bengkulu dengan mempertimbangkan:

* Mode transportasi pengguna
* Kondisi gerbang kampus
* Jam operasional kampus
* Jalur alternatif
* Simulasi waktu manual

Hasil perhitungan rute akan divisualisasikan dalam bentuk peta interaktif lengkap dengan informasi jarak dan estimasi waktu tempuh.

---

## Fitur Website

* Menentukan shortest path antar lokasi kampus
* Menampilkan beberapa rute alternatif
* Simulasi jam operasional kampus
* Deteksi gerbang kampus yang tutup
* Peta interaktif menggunakan Folium
* Informasi estimasi jarak dan waktu

---


### Penjelasan Struktur File

### 1. File app.py

File utama aplikasi berbasis Flask yang berisi seluruh logika program seperti:

* Pemrosesan input pengguna
* Perhitungan rute
* Pengaturan mode transportasi
* Pengelolaan gerbang kampus
* Integrasi dengan OpenRouteService

---

### 2. Folder templates

Folder ini digunakan untuk menyimpan file HTML yang ditampilkan pada website.

* `index.html` → halaman utama aplikasi

---

### 3. Folder static

Folder ini digunakan untuk menyimpan file pendukung tampilan website seperti:

* CSS
* JavaScript

---
### 4. File PowerPoint

Folder ini berisi pemaparan singkat tentang sistem yang dibuat beserta algoritma dan alur kerja yang tertuang dalam bentuk PowerPoint

---
### 5. File Laporan

Folder ini berisi laporan perencanaan model sebelum sistem dibuat.

---
## Kode yang Dihighlight

Berikut beberapa bagian kode penting yang digunakan dalam project ini.

---

### 1. Inisialisasi Flask dan OpenRouteService

```python
app = Flask(__name__)
client = openrouteservice.Client(key='API_KEY')
```

Kode ini digunakan untuk membuat aplikasi Flask serta menghubungkan sistem dengan API OpenRouteService.

---

### 2. Menyimpan Data Lokasi Kampus

```python
locations = {
    'Rektorat': [102.27231460986346, -3.7590495172423495],
    'Perpustakaan': [102.27485462111163, -3.756806076798016],
}
```

Kode ini digunakan untuk menyimpan koordinat lokasi-lokasi penting di Universitas Bengkulu.

---

### 3. Menentukan Gerbang Kampus yang Ditutup

```python
if not is_jam_operasional:
    gerbang_tutup.extend([
        'Gerbang Masuk Depan',
        'Gerbang Keluar Depan'
    ])
```

Kode ini digunakan untuk menutup akses gerbang tertentu di luar jam operasional kampus.

---

### 4. Menampilkan Peta Interaktif

```python
m = folium.Map(
    location=[-3.758, 102.272],
    zoom_start=16,
    tiles='CartoDB positron'
)
```

Kode ini digunakan untuk membuat tampilan peta interaktif menggunakan Folium.

---

### 5. Menampilkan Jalur Rute

```python
folium.GeoJson(
    feature,
    tooltip=f'{label}: {dist_km:.2f} km'
).add_to(m)
```

Kode ini digunakan untuk menampilkan jalur rute pada peta digital.

---

## Cara Menjalankan Program

### 1. Install Dependency

```bash
pip install flask openrouteservice folium
```

---

### 2. Jalankan Program

```bash
python app.py
```

---

### 3. Buka Browser

```text
http://127.0.0.1:5000
```

---

## Cara Kerja Sistem

1. Pengguna memilih lokasi awal dan tujuan.
2. Sistem membaca mode transportasi yang dipilih.
3. Program mengecek jam operasional kampus.
4. Sistem menentukan gerbang yang dapat dilalui.
5. OpenRouteService menghitung jalur tercepat.
6. Peta interaktif ditampilkan menggunakan Folium.
7. Sistem menampilkan:

   * Jalur utama
   * Jalur alternatif
   * Estimasi jarak
   * Estimasi waktu tempuh

---

## Tujuan Pembuatan Website

Project ini dibuat sebagai sarana pembelajaran dalam menerapkan:

* Pemrograman web menggunakan Flask
* Integrasi API
* Pengolahan data lokasi
* Konsep shortest path
* Visualisasi peta digital
* Penggunaan multimedia dan antarmuka interaktif

Selain itu, project ini juga bertujuan membantu pengguna menemukan rute tercepat di lingkungan Universitas Bengkulu secara lebih praktis dan efisien.

---

Terima kasih telah mengunjungi dan membaca README ini.
