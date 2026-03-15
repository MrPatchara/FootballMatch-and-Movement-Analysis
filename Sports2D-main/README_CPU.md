# การใช้ Sports2D บนเครื่องที่ไม่มี GPU

Sports2D **รันบน CPU ได้** โดยไม่ต้องมีการ์ดจอแยก (ไม่มี CUDA ก็ใช้ได้)

## ติดตั้ง (ไม่ต้องติด CUDA)

```bash
# จากโฟลเดอร์ Sports2D-main หรือที่ที่ clone มา
pip install sports2d
```

หรือติดตั้งจาก source:

```bash
cd Sports2D-main
pip install .
```

ไม่ต้องติด `torch` แบบ CUDA หรือ `onnxruntime-gpu` — เวอร์ชัน CPU ที่มากับ dependency จะถูกใช้เอง

## วิธีรันแบบใช้ CPU

### 1) ใช้ config สำหรับ CPU (แนะนำ)

มีไฟล์ **`Sports2D/Demo/Config_cpu.toml`** ที่ตั้งค่าให้ใช้ CPU และโหมดเบาเพื่อความเร็ว:

```bash
sports2d --config Sports2D/Demo/Config_cpu.toml
```

หรือระบุวิดีโอ:

```bash
sports2d --config Sports2D/Demo/Config_cpu.toml --video_input path/to/your/video.mp4
```

### 2) ใช้คำสั่งบรรทัดเดียว (ไม่ใช้ config ไฟล์)

บังคับ backend เป็น CPU และใช้โหมด lightweight:

```bash
sports2d --backend cpu --device CPU --mode lightweight --video_input path/to/video.mp4
```

หรือรัน demo:

```bash
sports2d --backend cpu --device CPU --mode lightweight
```

### 3) เรียกจาก Python

```python
from Sports2D import Sports2D
import toml
from pathlib import Path

config_path = Path("Sports2D/Demo/Config_cpu.toml")
config_dict = toml.load(config_path)
# เปลี่ยนวิดีโอถ้าต้องการ
# config_dict['base']['video_input'] = 'your_video.mp4'
Sports2D.process(config_dict)
```

## ปรับให้เร็วบน CPU

- ใช้ **`Config_cpu.toml`** (มี `mode = 'lightweight'`, `backend = 'cpu'`, `device = 'CPU'` อยู่แล้ว)
- ลดความละเอียดใน config: ใน `[base]` ตั้ง `input_size = [640, 360]` หรือ [960, 540]
- เพิ่ม `det_frequency` ใน `[pose]` (เช่น 20–50) ให้ detect คนทุก N เฟรม จะเร็วขึ้นแต่ติดตามคนน้อยลง
- ปิดการแสดงผล real-time ถ้าไม่จำเป็น: ใน config ตั้ง `show_realtime_results = false`

## สรุป

| รายการ        | เครื่องมี GPU     | เครื่องไม่มี GPU (ใช้ config นี้) |
|---------------|-------------------|-----------------------------------|
| ติดตั้ง       | pip install sports2d | เหมือนกัน ไม่ต้องติด CUDA        |
| การรัน        | `sports2d` (auto) | `--config Config_cpu.toml` หรือ `--backend cpu --device CPU --mode lightweight` |
| ความเร็ว      | เร็ว              | ช้ากว่า ใช้ lightweight + ลดความละเอียดช่วยได้ |

ผลลัพธ์ (มุมข้อต่อ, TRC, MOT ฯลฯ) เหมือนกัน ไม่ว่าใช้ CPU หรือ GPU
