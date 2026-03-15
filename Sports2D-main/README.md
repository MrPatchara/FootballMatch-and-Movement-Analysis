# Video to Pose & Angles

แปลงวิดีโอเป็นข้อมูล **2D pose** และ **มุมข้อต่อ/ส่วนของร่างกาย** (joint & segment angles) จากวิดีโอหรือกล้อง

- เลือกไฟล์วิดีโอ → เลือกโฟลเดอร์บันทึก → กดประมวลผล  
- ผลลัพธ์: วิดีโอที่วาด skeleton, ไฟล์ pose (TRC), มุม (MOT), กราฟ

## ความต้องการระบบ

- Python 3.9+
- Windows / macOS / Linux

## การติดตั้ง

```bash
# โคลนโปรเจกต์
git clone <url-of-your-repo>
cd <ชื่อโฟลเดอร์โปรเจกต์>

# สร้าง virtual environment (แนะนำ)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# ติดตั้ง
pip install -e .
```

## วิธีใช้

### ผ่าน GUI (แนะนำ)

```bash
python -m Sports2D.gui_app
```

หรือจากโฟลเดอร์โปรเจกต์:

```bash
python Sports2D/gui_app.py
```

1. กด **เลือกไฟล์** เลือกวิดีโอ (mp4, avi, mov, mkv)
2. กด **ประมวลผล**
3. เลือกโฟลเดอร์ที่ต้องการบันทึกผล
4. รอให้ประมวลผลเสร็จ — ผลจะถูกบันทึกในโฟลเดอร์ที่เลือกเท่านั้น

### ผลลัพธ์

ในโฟลเดอร์ที่เลือกจะได้โฟลเดอร์ย่อยของผลลัพธ์ ภายในมีตัวอย่างเช่น:

- วิดีโอที่วาด pose และมุม
- ไฟล์ pose (พิกเซล/เมตร) รูปแบบ TRC
- ไฟล์มุม (MOT) สำหรับ OpenSim
- โฟลเดอร์กราฟ (ถ้าเปิดใช้)

## License

MIT License — ดู [LICENSE](LICENSE)
