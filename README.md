# Kasti Training Simulator

Mini game berbasis computer vision yang memanfaatkan webcam sebagai media input utama. Pemain menggunakan sarung tangan hijau untuk mengendalikan pemukul (bat) dan memukul bola yang datang menuju layar secara real-time.

Project ini dikembangkan menggunakan Python, OpenCV, dan NumPy tanpa menggunakan game engine maupun framework tambahan. Seluruh proses deteksi objek, pengolahan citra, gesture recognition, collision detection, dan scoring system diimplementasikan secara mandiri.

**Nama:** Atika Najwa Azzahra
**NRP:** 50224241091

---

## Demo

### Screenshot Gameplay

[PLACEHOLDER]

### Screenshot Hand Mask

[PLACEHOLDER]

### Video Demonstrasi

[PLACEHOLDER]

---

## Fitur

* Deteksi sarung tangan hijau menggunakan HSV Color Segmentation
* Morphological Opening dan Closing manual menggunakan NumPy
* Gesture Recognition berbasis gripping gesture
* Weapon sprite overlay menggunakan alpha blending manual
* Bola dengan efek zoom untuk mensimulasikan arah datang bola
* Collision detection antara bat dan bola
* Sistem skor dan nyawa
* Intro screen, countdown, dan game over screen
* Gameplay real-time menggunakan webcam

---

## Teknologi

* Python 3.x
* OpenCV
* NumPy

---

## Struktur Folder

```text
DEMO/
│
├── src/
│   ├── main.py
│   ├── detector.py
│   ├── bat.py
│   ├── ball.py
│   ├── hud.py
│   └── utils.py
│
├── assets/
│   ├── bat.png
│   └── ball.png
│
├── screenshots/
│
└── README.md
```

---

## Cara Menjalankan

Install dependency:

```bash
pip install opencv-python numpy
```

Jalankan program:

```bash
cd src
python main.py
```

Pastikan webcam aktif dan file `bat.png` serta `ball.png` tersedia pada folder `assets`.

---

## Cara Bermain

1. Gunakan sarung tangan berwarna hijau.
2. Pastikan tangan terlihat oleh kamera.
3. Berdiri di luar area kotak kuning yang ditampilkan pada layar.
4. Tunggu proses countdown selesai.
5. Saat bola mendekat dan muncul label **HIT!**, arahkan tangan ke posisi bola.
6. Jika bola berhasil dipukul maka skor bertambah.
7. Jika bola terlewat maka nyawa berkurang.
8. Permainan berakhir ketika seluruh nyawa habis.

### Kontrol

| Tombol | Fungsi                |
| ------ | --------------------- |
| r      | Restart permainan     |
| q      | Keluar dari permainan |

---

## Implementasi

### Hand Detection

Deteksi tangan dilakukan menggunakan segmentasi warna HSV pada area ROI (Region of Interest). Sistem mencari objek berwarna hijau yang diasumsikan sebagai sarung tangan pemain.

### Morphological Processing

Hasil segmentasi masih mengandung noise sehingga dilakukan proses Opening dan Closing yang diimplementasikan secara manual menggunakan operasi Erosion dan Dilation berbasis NumPy.

### Gesture Recognition

Gesture yang digunakan pada permainan adalah gripping gesture. Sistem menentukan kondisi gripping berdasarkan luas area kontur tangan yang terdeteksi.

### Weapon Overlay

Sprite bat ditempelkan pada posisi tangan menggunakan alpha blending manual sehingga dapat mengikuti pergerakan tangan secara real-time.

### Second Object

Objek kedua pada permainan adalah bola yang bergerak dari ukuran kecil menjadi besar. Efek pembesaran ini memberikan ilusi bahwa bola datang dari kejauhan menuju pemain.

### Collision Detection

Tabrakan antara bola dan bat dihitung menggunakan jarak antara pusat bola dengan posisi tangan pemain. Jika jarak lebih kecil dari radius tumbukan yang ditentukan maka bola dianggap berhasil dipukul.

### Scoring System

Aturan penilaian yang digunakan:

* Bola berhasil dipukul : +10 poin
* Bola terlewat : -1 nyawa
* Nyawa habis : Game Over

---

## Hasil Implementasi

Project berhasil mengimplementasikan seluruh komponen utama yang dipersyaratkan pada mini project, yaitu:

* Webcam Input
* HSV Color Segmentation
* Morphological Operation
* Gesture Recognition
* Weapon Overlay
* Second Object
* Collision Detection
* Score System
* Real-Time Gameplay

---

## Repository

[PLACEHOLDER]

---

## Referensi

* OpenCV Documentation
* NumPy Documentation
* OpenCV Color Spaces Documentation
* OpenCV Morphological Operations Documentation
