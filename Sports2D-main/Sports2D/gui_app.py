#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Video to Pose & Angles – ตัวแปลงวิดีโอเป็น Pose & Angle Analysis

เลือกไฟล์วิดีโอ → กดประมวลผล → เลือกโฟลเดอร์บันทึก (ผลจะเซฟที่โฟลเดอร์ที่เลือกเท่านั้น)
"""

from __future__ import annotations

import sys
import threading
from pathlib import Path
from typing import Optional

# รันจากโฟลเดอร์โปรเจกต์: python -m Sports2D.gui_app หรือ python Sports2D/gui_app.py
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

from Sports2D.Sports2D import process as sports2d_process


# โทนดำ-แดง (แดงเข้ม)
DARK_BG = "#1a1a1a"
DARK_PANEL = "#252525"
DARK_INPUT = "#2d2d2d"
RED_ACCENT = "#8b1828"
RED_ACCENT_HOVER = "#a01d30"
TEXT_WHITE = "#e8e8e8"
TEXT_MUTED = "#9a9a9a"

STYLESHEET = f"""
    QMainWindow, QWidget {{
        background-color: {DARK_BG};
        color: {TEXT_WHITE};
    }}
    QLabel {{
        color: {TEXT_WHITE};
    }}
    QLineEdit {{
        background-color: {DARK_INPUT};
        color: {TEXT_WHITE};
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 8px 10px;
        selection-background-color: {RED_ACCENT};
    }}
    QLineEdit:focus {{
        border-color: {RED_ACCENT};
    }}
    QPushButton {{
        background-color: {DARK_PANEL};
        color: {TEXT_WHITE};
        border: 1px solid #444;
        border-radius: 6px;
        padding: 8px 14px;
    }}
    QPushButton:hover {{
        background-color: #333;
        border-color: {RED_ACCENT};
    }}
    QPushButton:pressed {{
        background-color: {RED_ACCENT};
        border-color: {RED_ACCENT};
    }}
    QPushButton:disabled {{
        background-color: #252525;
        color: {TEXT_MUTED};
        border-color: #333;
    }}
    QPushButton#processBtn {{
        background-color: {RED_ACCENT};
        border-color: {RED_ACCENT};
        font-weight: 600;
    }}
    QPushButton#processBtn:hover:enabled {{
        background-color: {RED_ACCENT_HOVER};
        border-color: {RED_ACCENT_HOVER};
    }}
    QPushButton#browseBtn {{
        background-color: #2a2a2a;
    }}
    QStatusBar {{
        background-color: {DARK_PANEL};
        color: {TEXT_MUTED};
        border-top: 1px solid #2a2a2a;
    }}
"""


class ProcessingWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        video_path: Path,
        result_dir: Path,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._video_path = video_path
        self._result_dir = Path(result_dir)

    def run(self) -> None:
        try:
            video_path = self._video_path
            video_dir = video_path.parent
            result_dir = self._result_dir
            result_dir.mkdir(parents=True, exist_ok=True)
            output_dir_name = f"{video_path.stem}_Sports2D"
            output_dir = result_dir / output_dir_name

            config = {
                "base": {
                    "video_input": [video_path.name],
                    "video_dir": str(video_dir),
                    "result_dir": str(result_dir),
                    "nb_persons_to_detect": 1,
                    "person_ordering_method": "highest_likelihood",
                    "show_realtime_results": False,
                    "save_vid": True,
                    "save_img": False,
                    "save_pose": True,
                    "calculate_angles": True,
                    "save_angles": True,
                },
                "post-processing": {
                    "show_graphs": False,
                    "save_graphs": True,
                },
            }

            sports2d_process(config)

            if not output_dir.exists():
                raise FileNotFoundError(f"ไม่พบโฟลเดอร์ผลลัพธ์: {output_dir}")
            self.finished.emit(str(output_dir.resolve()))

        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:
            import traceback
            self.error.emit(f"{exc!r}\n\n{traceback.format_exc()}")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Video to Pose & Angles")
        self.setMinimumSize(400, 140)
        self.resize(440, 160)
        self.setStyleSheet(STYLESHEET)

        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(12)

        # แถบหัวข้อ
        title = QLabel("Video to Pose & Angles", self)
        title.setStyleSheet(
            f"font-size: 16px; font-weight: 600; color: {TEXT_WHITE}; "
            f"border-bottom: 2px solid {RED_ACCENT}; padding-bottom: 6px; margin-bottom: 2px;"
        )
        layout.addWidget(title)

        # แถบที่ 2: เลือกไฟล์
        file_row = QHBoxLayout()
        file_row.setSpacing(8)
        self.video_path_edit = QLineEdit(self)
        self.video_path_edit.setPlaceholderText("เลือกรายการวิดีโอ...")
        self.video_path_edit.setReadOnly(True)

        browse_btn = QPushButton("เลือกไฟล์", self)
        browse_btn.setObjectName("browseBtn")
        browse_btn.clicked.connect(self.select_video)

        file_row.addWidget(self.video_path_edit, stretch=1)
        file_row.addWidget(browse_btn)
        layout.addLayout(file_row)

        # แถบที่ 3: ปุ่มประมวลผล
        self.process_btn = QPushButton("ประมวลผล", self)
        self.process_btn.setObjectName("processBtn")
        self.process_btn.setEnabled(False)
        self.process_btn.setMinimumHeight(36)
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)

        # Status bar
        status = QStatusBar(self)
        self.setStatusBar(status)
        self.status_label = QLabel("พร้อมใช้งาน", self)
        status.addWidget(self.status_label)

        self._current_video_path: Optional[Path] = None

    def select_video(self) -> None:
        file_filter = "Video (*.mp4 *.avi *.mov *.mkv);;All (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "เลือกไฟล์วิดีโอ", "", file_filter
        )
        if not file_path:
            return
        self._current_video_path = Path(file_path)
        self.video_path_edit.setText(str(self._current_video_path))
        self.process_btn.setEnabled(True)
        self.status_label.setText("เลือกไฟล์แล้ว กดประมวลผล")

    def start_processing(self) -> None:
        if not self._current_video_path:
            QMessageBox.warning(self, "คำเตือน", "กรุณาเลือกไฟล์วิดีโอก่อน")
            return

        # ถามโฟลเดอร์บันทึกก่อน แล้วเซฟไปที่นั่นโดยตรง (ไม่เซฟข้างไฟล์วิดีโอ)
        video_dir = self._current_video_path.parent
        target_dir = QFileDialog.getExistingDirectory(
            self,
            "เลือกโฟลเดอร์บันทึกผล",
            str(video_dir),
        )
        if not target_dir:
            return

        self.process_btn.setEnabled(False)
        self.status_label.setText("กำลังประมวลผล... รอสักครู่")

        worker = ProcessingWorker(
            self._current_video_path,
            result_dir=Path(target_dir),
        )
        worker.finished.connect(self.on_processing_finished)
        worker.error.connect(self.on_processing_error)
        threading.Thread(target=worker.run, daemon=True).start()

    def on_processing_finished(self, output_dir: str) -> None:
        self.process_btn.setEnabled(True)
        self.status_label.setText("เสร็จแล้ว")
        QMessageBox.information(
            self, "เสร็จสิ้น", f"บันทึกผลลัพธ์ที่:\n{output_dir}"
        )

    def on_processing_error(self, message: str) -> None:
        self.process_btn.setEnabled(True)
        self.status_label.setText("เกิดข้อผิดพลาด")
        QMessageBox.critical(self, "เกิดข้อผิดพลาด", message)


def run_gui() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
