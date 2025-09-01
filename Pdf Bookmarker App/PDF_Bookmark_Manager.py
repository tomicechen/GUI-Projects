import sys
import os
import fitz  # PyMuPDF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QTreeWidget, QTreeWidgetItem,
    QMessageBox, QInputDialog, QLabel, QScrollArea
)
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtCore import Qt
from pypdf import PdfReader, PdfWriter


class PdfBookmarkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kartick's Bookmark Manager")
        self.setGeometry(200, 100, 1200, 800)

        # PDF data
        self.pdf_path = None
        self.doc = None  # fitz Document
        self.bookmarks = []  # (title, page, level, item)

        # Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # ---- Left side: Tree (bookmarks) + buttons ----
        left_layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Title", "Page"])
        self.tree.header().setDefaultSectionSize(200)
        self.tree.setFont(QFont("Arial", 12))
        self.tree.itemDoubleClicked.connect(self.jump_to_page)
        left_layout.addWidget(self.tree)

        self.btn_load = QPushButton("Load PDF")
        self.btn_load.setFont(QFont("Arial", 12))
        self.btn_load.clicked.connect(self.load_pdf)
        left_layout.addWidget(self.btn_load)

        self.btn_chapter = QPushButton("Add Chapter")
        self.btn_chapter.setFont(QFont("Arial", 12))
        self.btn_chapter.clicked.connect(self.add_chapter)
        left_layout.addWidget(self.btn_chapter)

        self.btn_section = QPushButton("Add Section")
        self.btn_section.setFont(QFont("Arial", 12))
        self.btn_section.clicked.connect(self.add_section)
        left_layout.addWidget(self.btn_section)

        self.btn_edit = QPushButton("Edit Selected")
        self.btn_edit.setFont(QFont("Arial", 12))
        self.btn_edit.clicked.connect(self.edit_selected)
        left_layout.addWidget(self.btn_edit)

        self.btn_remove = QPushButton("Remove Selected")
        self.btn_remove.setFont(QFont("Arial", 12))
        self.btn_remove.clicked.connect(self.remove_selected)
        left_layout.addWidget(self.btn_remove)

        self.btn_export = QPushButton("Export PDF with Bookmarks")
        self.btn_export.setFont(QFont("Arial", 12))
        self.btn_export.clicked.connect(self.export_pdf)
        left_layout.addWidget(self.btn_export)

        self.btn_clear = QPushButton("Clear All")
        self.btn_clear.setFont(QFont("Arial", 12))
        self.btn_clear.clicked.connect(self.clear_all)
        left_layout.addWidget(self.btn_clear)

        main_layout.addLayout(left_layout, 3)

        # ---- Right side: PDF Preview ----
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        self.scroll_area.setWidget(self.preview_container)
        main_layout.addWidget(self.scroll_area, 7)

        # ---- Page number label ----
        self.page_label = QLabel("Page: -/-")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.page_label.setFont(QFont("Arial", 14, QFont.Bold))
        main_layout.addWidget(self.page_label, 1)

        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_page_label)

    # -------- PDF Loading --------
    def load_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        try:
            # Clean with pypdf
            reader = PdfReader(path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            clean_path = path.replace(".pdf", "_clean.pdf")
            with open(clean_path, "wb") as f:
                writer.write(f)

            # Load into fitz for preview
            self.doc = fitz.open(clean_path)
            self.pdf_path = clean_path

            # Show preview
            self.render_preview()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF: {e}")

    # -------- Preview Rendering --------
    def render_preview(self):
        # Clear old preview
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not self.doc:
            return

        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))  # Zoom for readability
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            lbl = QLabel()
            lbl.setPixmap(QPixmap.fromImage(img))
            self.preview_layout.addWidget(lbl)

        self.update_page_label()

    # -------- Add Chapter --------
    def add_chapter(self):
        if not self.doc:
            QMessageBox.warning(self, "Warning", "Load a PDF first.")
            return

        title, ok1 = QInputDialog.getText(self, "Enter Chapter Name", "Chapter Name:")
        if not ok1 or not title:
            return

        page, ok2 = QInputDialog.getInt(
            self, "Enter Page No", "Page Number:", 1, 1, len(self.doc)
        )
        if not ok2:
            return

        item = QTreeWidgetItem([title, str(page)])
        self.tree.addTopLevelItem(item)
        self.bookmarks.append((title, page - 1, 0, item))

    # -------- Add Section --------
    def add_section(self):
        selected = self.tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Select a chapter to add a section.")
            return

        title, ok1 = QInputDialog.getText(self, "Enter Section Name", "Section Name:")
        if not ok1 or not title:
            return

        page, ok2 = QInputDialog.getInt(
            self, "Enter Page No", "Page Number:", 1, 1, len(self.doc)
        )
        if not ok2:
            return

        section_item = QTreeWidgetItem([title, str(page)])
        selected.addChild(section_item)
        self.bookmarks.append((title, page - 1, 1, section_item))

    # -------- Edit Selected --------
    def edit_selected(self):
        selected = self.tree.currentItem()
        if not selected:
            return

        old_title = selected.text(0)
        old_page = int(selected.text(1))

        title, ok1 = QInputDialog.getText(self, "Edit Title", "Title:", text=old_title)
        if not ok1 or not title:
            return

        page, ok2 = QInputDialog.getInt(
            self, "Edit Page", "Page Number:", old_page, 1, len(self.doc)
        )
        if not ok2:
            return

        selected.setText(0, title)
        selected.setText(1, str(page))

        # Update in bookmarks
        for i, (t, p, lvl, item) in enumerate(self.bookmarks):
            if item == selected:
                self.bookmarks[i] = (title, page - 1, lvl, selected)
                break

    # -------- Remove Selected --------
    def remove_selected(self):
        selected = self.tree.currentItem()
        if not selected:
            return

        parent = selected.parent()
        if parent:
            parent.removeChild(selected)
        else:
            index = self.tree.indexOfTopLevelItem(selected)
            self.tree.takeTopLevelItem(index)

        self.bookmarks = [(t, p, lvl, it) for (t, p, lvl, it) in self.bookmarks if it != selected]

    # -------- Jump to Page on Double Click --------
    def jump_to_page(self, item):
        page_index = int(item.text(1)) - 1
        self.scroll_to_page(page_index)

    def scroll_to_page(self, page_index):
        if page_index < 0 or page_index >= len(self.doc):
            return
        widget = self.preview_layout.itemAt(page_index).widget()
        if widget:
            self.scroll_area.ensureWidgetVisible(widget)
        self.page_label.setText(f"Page: {page_index+1}/{len(self.doc)}")

    # -------- Update Page Number on Scroll --------
    def update_page_label(self):
        if not self.doc:
            self.page_label.setText("Page: -/-")
            return

        scrollbar = self.scroll_area.verticalScrollBar()
        val = scrollbar.value()
        for i in range(self.preview_layout.count()):
            widget = self.preview_layout.itemAt(i).widget()
            if widget and widget.y() <= val < widget.y() + widget.height():
                self.page_label.setText(f"Page: {i+1}/{len(self.doc)}")
                break

    # -------- Export PDF with Bookmarks --------
    def export_pdf(self):
        if not self.pdf_path:
            QMessageBox.warning(self, "Warning", "Load a PDF first.")
            return

        base, ext = os.path.splitext(self.pdf_path)
        default_name = base.replace("_clean", "") + "_With_Bookmark.pdf"

        out_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", default_name, "PDF Files (*.pdf)"
        )
        if not out_path:
            return

        reader = PdfReader(self.pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        parent_map = {}
        for title, page, level, item in self.bookmarks:
            if level == 0:
                parent_map[item] = writer.add_outline_item(title, page)
            else:
                parent = item.parent()
                parent_map[item] = writer.add_outline_item(title, page, parent=parent_map.get(parent))

        with open(out_path, "wb") as f:
            writer.write(f)

        # --- Show dialog with Open button ---
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText(f"PDF saved to:\n{out_path}")
        msg.setIcon(QMessageBox.Information)
        open_button = msg.addButton("Open", QMessageBox.AcceptRole)
        msg.addButton("OK", QMessageBox.RejectRole)
        msg.exec()

        if msg.clickedButton() == open_button:
            os.startfile(out_path)  # Works on Windows


    # -------- Clear All --------
    def clear_all(self):
        self.tree.clear()
        self.bookmarks = []
        self.doc = None
        self.pdf_path = None
        self.render_preview()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfBookmarkApp()
    window.show()
    sys.exit(app.exec())
