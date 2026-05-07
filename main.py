import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QPushButton, QCheckBox, QLabel,
    QVBoxLayout, QGridLayout, QHBoxLayout,
    QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


# ══════════════════════════════════════════════
#  DatabaseManager  (ตามสไลด์หน้า 7-11)
# ══════════════════════════════════════════════
class DatabaseManager:
    def __init__(self, db_name="user.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL,
            year TEXT,
            admin INTEGER DEFAULT 0
        )
        """
        self.cursor.execute(sql)
        self.conn.commit()

    # ── CREATE ──────────────────────────────
    def add_user(self, name, year, is_admin):
        sql = "INSERT INTO users (name, year, admin) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (name, year, 1 if is_admin else 0))
        self.conn.commit()

    # ── READ ────────────────────────────────
    def get_all_users(self):
        sql = "SELECT * FROM users"
        self.cursor.execute(sql)
        return self.cursor.fetchall()   # คืนค่า List ของข้อมูล

    # ── UPDATE ──────────────────────────────
    def update_user(self, user_id, name, year, is_admin):
        sql = "UPDATE users SET name=?, year=?, admin=? WHERE id=?"
        self.cursor.execute(sql, (name, year, 1 if is_admin else 0, user_id))
        self.conn.commit()

    # ── DELETE ──────────────────────────────
    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id=?"
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


# ══════════════════════════════════════════════
#  MainWindow
# ══════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("โปรแกรมทดสอบ - user.ui")
        self.setMinimumSize(860, 580)
        self.selected_id = None

        self.db = DatabaseManager()   # เรียกใช้ Database (สไลด์ p.7)
        self._build_ui()
        self._apply_style()
        self._connect_signals()
        self.load_data()              # โหลดข้อมูลทันทีตอนเปิดโปรแกรม

    # ─────────────────────────────────────────
    # Build UI
    # ─────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(6)

        # ── QTableWidget ──
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "NAME", "YEAR", "Admin"])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        hh = self.tableWidget.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        main_layout.addWidget(self.tableWidget)

        # ── Form ──
        form = QWidget()
        grid = QGridLayout(form)
        grid.setContentsMargins(6, 6, 6, 6)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        grid.setColumnStretch(2, 1)   # spacer column

        # Row 0: Name
        self.labelName    = QLabel("Name")
        self.lineEditName = QLineEdit()
        self.lineEditName.setMinimumWidth(260)
        self.lineEditName.setPlaceholderText("ชื่อ-นามสกุล")
        self.btnAdd    = QPushButton("Add");    self.btnAdd.setObjectName("btnAdd")
        self.btnUpdate = QPushButton("Update"); self.btnUpdate.setObjectName("btnUpdate")
        for w in (self.btnAdd, self.btnUpdate):
            w.setMinimumWidth(100)

        grid.addWidget(self.labelName,    0, 0)
        grid.addWidget(self.lineEditName, 0, 1)
        grid.addWidget(self.btnAdd,       0, 3)
        grid.addWidget(self.btnUpdate,    0, 4)

        # Row 1: Year + Admin + Del
        self.labelYear    = QLabel("Year")
        year_box = QHBoxLayout()
        self.lineEditYear = QLineEdit()
        self.lineEditYear.setMaximumWidth(130)
        self.lineEditYear.setPlaceholderText("ปี")
        self.checkBoxAdmin = QCheckBox("Admin")
        year_box.addWidget(self.lineEditYear)
        year_box.addSpacing(8)
        year_box.addWidget(self.checkBoxAdmin)
        year_box.addStretch()
        self.btnDel = QPushButton("Del"); self.btnDel.setObjectName("btnDel")
        self.btnDel.setMinimumWidth(100)

        grid.addWidget(self.labelYear, 1, 0)
        grid.addLayout(year_box,       1, 1)
        grid.addWidget(self.btnDel,    1, 3)

        main_layout.addWidget(form)

        # ── Menu bar ──
        mb = self.menuBar()
        mb.addMenu("File")
        mb.addMenu("Type Here")

    # ─────────────────────────────────────────
    # Style
    # ─────────────────────────────────────────
    def _apply_style(self):
        self.setStyleSheet("""
        QMainWindow { background: #f0f4f8; }
        QMenuBar {
            background: #1e3a5f; color: #fff;
            font-size: 13px; padding: 2px 4px;
        }
        QMenuBar::item:selected { background: #2e5080; }
        QTableWidget {
            background: #fff;
            alternate-background-color: #f0f6ff;
            gridline-color: #d0dae6;
            border: 1px solid #c8d9ee;
            border-radius: 6px; font-size: 13px; color: #2d4059;
        }
        QHeaderView::section {
            background: #1e3a5f; color: #fff;
            padding: 8px 12px; font-weight: bold;
            font-size: 13px; border: none;
        }
        QTableWidget::item:selected { background: #dbeafe; color: #1e3a5f; }
        QLabel  { font-size: 13px; font-weight: bold; color: #4a6080; }
        QLineEdit {
            background: #f8fafc; border: 1px solid #c8d9ee;
            border-radius: 5px; padding: 5px 9px;
            font-size: 13px; color: #2d4059;
        }
        QLineEdit:focus { border: 1px solid #3b82f6; background: #fff; }
        QCheckBox { font-size: 13px; color: #4a6080; }
        QPushButton {
            font-size: 13px; font-weight: bold;
            padding: 6px 18px; border-radius: 6px;
            border: none; color: #fff;
        }
        QPushButton#btnAdd            { background: #2563eb; }
        QPushButton#btnAdd:hover      { background: #1d4ed8; }
        QPushButton#btnAdd:pressed    { background: #1e40af; }
        QPushButton#btnUpdate         { background: #0f766e; }
        QPushButton#btnUpdate:hover   { background: #0d6560; }
        QPushButton#btnUpdate:pressed { background: #0a534e; }
        QPushButton#btnDel            { background: #dc2626; }
        QPushButton#btnDel:hover      { background: #b91c1c; }
        QPushButton#btnDel:pressed    { background: #991b1b; }
        """)

    # ─────────────────────────────────────────
    # Signals
    # ─────────────────────────────────────────
    def _connect_signals(self):
        self.btnAdd.clicked.connect(self.create_data)       # สไลด์ p.8
        self.btnUpdate.clicked.connect(self.update_data)    # สไลด์ p.10
        self.btnDel.clicked.connect(self.delete_data)       # สไลด์ p.11
        self.tableWidget.itemSelectionChanged.connect(self.select_data)  # p.10

    # ─────────────────────────────────────────
    # READ — โหลดข้อมูลใส่ตาราง (สไลด์ p.9)
    # ─────────────────────────────────────────
    def load_data(self):
        result = self.db.get_all_users()
        self.tableWidget.setRowCount(0)       # ล้างตารางเก่าก่อนเสมอ
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 3:        # คอลัมน์ Admin แสดงเป็น badge
                    is_admin = bool(data)
                    item = QTableWidgetItem("✔ Admin" if is_admin else "—")
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("#1e40af") if is_admin else QColor("#64748b"))
                    if is_admin:
                        item.setBackground(QColor("#dbeafe"))
                    self.tableWidget.setItem(row_number, column_number, item)
                else:
                    self.tableWidget.setItem(
                        row_number, column_number,
                        QTableWidgetItem(str(data))
                    )

    # ─────────────────────────────────────────
    # CREATE (สไลด์ p.8)
    # ─────────────────────────────────────────
    def create_data(self):
        name  = self.lineEditName.text().strip()
        year  = self.lineEditYear.text().strip()
        admin = self.checkBoxAdmin.isChecked()

        if name and year:
            self.db.add_user(name, year, admin)
            QMessageBox.information(self, "Success", "บันทึกข้อมูลเรียบร้อย!")
            self.lineEditName.clear()
            self.lineEditYear.clear()
            self.checkBoxAdmin.setChecked(False)
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "กรุณากรอกชื่อและปี")

    # ─────────────────────────────────────────
    # SELECT ROW → ใส่ข้อมูลลง form (สไลด์ p.10)
    # ─────────────────────────────────────────
    def select_data(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        self.selected_id = self.tableWidget.item(row, 0).text()   # เก็บ ID ไว้ใช้ตอน update/delete
        self.lineEditName.setText(self.tableWidget.item(row, 1).text())
        self.lineEditYear.setText(self.tableWidget.item(row, 2).text())
        admin_text = self.tableWidget.item(row, 3).text()
        self.checkBoxAdmin.setChecked("Admin" in admin_text)

    # ─────────────────────────────────────────
    # UPDATE (สไลด์ p.10)
    # ─────────────────────────────────────────
    def update_data(self):
        if self.selected_id:    # เช็คว่ามีการเลือก ID หรือยัง
            name  = self.lineEditName.text().strip()
            year  = self.lineEditYear.text().strip()
            admin = self.checkBoxAdmin.isChecked()
            self.db.update_user(self.selected_id, name, year, admin)
            self.load_data()    # รีเฟรชตาราง
            self.lineEditName.clear()
            self.lineEditYear.clear()
            self.checkBoxAdmin.setChecked(False)
            self.selected_id = None
            QMessageBox.information(self, "Success", "แก้ไขข้อมูลเรียบร้อย")
        else:
            QMessageBox.warning(self, "Warning", "กรุณาเลือกรายการที่ต้องการแก้ไข")

    # ─────────────────────────────────────────
    # DELETE (สไลด์ p.11)
    # ─────────────────────────────────────────
    def delete_data(self):
        if self.selected_id:
            confirm = QMessageBox.question(
                self, "Confirm", "ต้องการลบข้อมูลนี้ใช่หรือไม่?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.db.delete_user(self.selected_id)
                self.load_data()   # รีเฟรชตาราง
                self.lineEditName.clear()
                self.lineEditYear.clear()
                self.checkBoxAdmin.setChecked(False)
                self.selected_id = None
        else:
            QMessageBox.warning(self, "Warning", "กรุณาเลือกรายการที่ต้องการลบ")

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)


# ══════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
