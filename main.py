#!/usr/bin/env python3
"""
Dashboard - PySide6 macOS-safe application
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QMessageBox
)
from PySide6.QtCore import Qt


# -----------------------------
# Resource handling
# -----------------------------
def resource_path(relative: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative
    return Path(__file__).parent / relative


# -----------------------------
# Main Window
# -----------------------------
class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard")
        self.resize(1000, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)

        # -----------------------------
        # Sidebar
        # -----------------------------
        self.sidebar = QListWidget()
        self.sidebar.addItems([
            "Overview",
            "Analytics",
            "Settings"
        ])
        self.sidebar.setFixedWidth(200)
        self.sidebar.currentRowChanged.connect(self.switch_page)

        # -----------------------------
        # Content area
        # -----------------------------
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setAlignment(Qt.AlignTop)

        self.page_label = QLabel("Overview")
        self.page_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.info_label = QLabel("Dashboard is running using PySide6.")
        self.info_label.setStyleSheet("font-size: 14px;")

        self.content_layout.addWidget(self.page_label)
        self.content_layout.addWidget(self.info_label)

        # -----------------------------
        # Layout combine
        # -----------------------------
        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.content)

        self.sidebar.setCurrentRow(0)

        # -----------------------------
        # Load optional data
        # -----------------------------
        data_file = resource_path("titanium_data.json")
        if data_file.exists():
            try:
                import json
                with open(data_file, "r") as f:
                    data = json.load(f)

                self.data_label = QLabel(
                    f"Loaded data with {len(data)} entries."
                )
                self.content_layout.addWidget(self.data_label)

            except Exception as e:
                QMessageBox.critical(self, "Data Error", str(e))

    # -----------------------------
    # Page switching
    # -----------------------------
    def switch_page(self, index: int):
        pages = {
            0: "Overview",
            1: "Analytics",
            2: "Settings"
        }
        page = pages.get(index, "Unknown")
        self.page_label.setText(page)
        self.info_label.setText(f"You are viewing the {page} page.")


# -----------------------------
# App entry
# -----------------------------
def main():
    app = QApplication(sys.argv)

    # macOS menu bar integration
    app.setAttribute(Qt.AA_DontUseNativeMenuBar, False)

    window = DashboardWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
