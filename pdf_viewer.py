import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QAction, QFileDialog, QVBoxLayout,
    QLineEdit, QPushButton, QWidget, QHBoxLayout, QToolBar, QMessageBox,
    QInputDialog, QListWidget, QSplitter, QStyle
)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence, QIcon, QCursor
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog


class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFビューワ")
        self.resize(1000, 700)

        self.doc = None
        self.current_page_index = 0

        self.label = QLabel("PDFを開いてください", alignment=Qt.AlignCenter)
        self.label.setCursor(Qt.ArrowCursor)

        self.setAcceptDrops(True)

        self.outline_list = QListWidget()
        self.outline_list.itemClicked.connect(self.goto_outline_page)
        self.outline_list.setMaximumWidth(300)
        self.outline_list.setCursor(Qt.PointingHandCursor)

        self.pdf_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.pdf_widget.setLayout(layout)

        splitter = QSplitter()
        splitter.addWidget(self.outline_list)
        splitter.addWidget(self.pdf_widget)
        self.setCentralWidget(splitter)

        self.create_menu()
        self.create_toolbar()
        self.create_page_controls()

        self.search_shortcut = QAction(self)
        self.search_shortcut.setShortcut(QKeySequence("Ctrl+F"))
        self.search_shortcut.triggered.connect(self.search_text)
        self.addAction(self.search_shortcut)

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("ファイル")

        open_action = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon), "開く", self)
        open_action.triggered.connect(lambda: self.open_pdf())  # 修正済み
        file_menu.addAction(open_action)

        save_action = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "保存", self)
        save_action.triggered.connect(self.save_pdf)
        file_menu.addAction(save_action)

        print_action = QAction(self.style().standardIcon(QStyle.SP_DesktopIcon), "印刷", self)
        print_action.triggered.connect(self.print_pdf)
        file_menu.addAction(print_action)

        search_action = QAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "検索", self)
        search_action.triggered.connect(self.search_text)
        file_menu.addAction(search_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        open_icon = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon), "開く", self)
        open_icon.triggered.connect(lambda: self.open_pdf())  # 修正済み
        toolbar.addAction(open_icon)

        save_icon = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton), "保存", self)
        save_icon.triggered.connect(self.save_pdf)
        toolbar.addAction(save_icon)

        print_icon = QAction(self.style().standardIcon(QStyle.SP_DesktopIcon), "印刷", self)
        print_icon.triggered.connect(self.print_pdf)
        toolbar.addAction(print_icon)

        search_icon = QAction(self.style().standardIcon(QStyle.SP_FileDialogContentsView), "検索", self)
        search_icon.triggered.connect(self.search_text)
        toolbar.addAction(search_icon)

    def create_page_controls(self):
        control_widget = QWidget()
        layout = QHBoxLayout()

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("ページ番号")
        layout.addWidget(self.page_input)

        jump_button = QPushButton("ジャンプ")
        jump_button.clicked.connect(self.jump_to_page)
        layout.addWidget(jump_button)

        layout.addStretch()
        control_widget.setLayout(layout)

        self.menuBar().setCornerWidget(control_widget, Qt.TopRightCorner)

    def open_pdf(self, filepath=None):
        if filepath is None:
            filepath, _ = QFileDialog.getOpenFileName(self, "PDFを開く", "", "PDF Files (*.pdf)")
        if filepath:
            try:
                self.doc = fitz.open(filepath)
                self.current_page_index = 0
                self.show_page(0)
                self.load_outline()
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"PDFを開けませんでした：\n{e}")

    def save_pdf(self):
        if not self.doc:
            return
        save_path, _ = QFileDialog.getSaveFileName(self, "名前を付けて保存", "", "PDF Files (*.pdf)")
        if save_path:
            self.doc.save(save_path)
            QMessageBox.information(self, "保存", "PDFを保存しました。")

    def print_pdf(self):
        if not self.doc:
            return
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            page = self.doc.load_page(self.current_page_index)
            pix = page.get_pixmap()
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            painter = QPixmap.fromImage(image).toImage()
            painter.save(printer.outputFileName(), "PDF")

    def show_page(self, index):
        if not self.doc or index < 0 or index >= len(self.doc):
            return

        self.current_page_index = index
        page = self.doc.load_page(index)
        pix = page.get_pixmap()
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))
        self.setWindowTitle(f"PDFビューワ - ページ {index + 1}/{len(self.doc)}")

    def jump_to_page(self):
        if not self.doc:
            return
        try:
            page_number = int(self.page_input.text()) - 1
            if 0 <= page_number < len(self.doc):
                self.show_page(page_number)
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "無効な入力", "正しいページ番号を入力してください。")

    def search_text(self):
        if not self.doc:
            return

        keyword, ok = QInputDialog.getText(self, "検索", "検索ワードを入力してください：")
        if not ok or not keyword:
            return

        for i, page in enumerate(self.doc):
            if keyword in page.get_text():
                self.show_page(i)
                QMessageBox.information(self, "検索結果", f"{i+1} ページ目に見つかりました。")
                return

        QMessageBox.information(self, "検索結果", "見つかりませんでした。")

    def load_outline(self):
        self.outline_list.clear()
        try:
            toc = self.doc.get_toc()
            for entry in toc:
                level, title, page = entry
                self.outline_list.addItem(f"{title} (p.{page})")
        except Exception:
            pass

    def goto_outline_page(self, item):
        text = item.text()
        if "(p." in text:
            try:
                page = int(text.split("(p.")[1].rstrip(")")) - 1
                self.show_page(page)
            except:
                pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(".pdf"):
                event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            filepath = urls[0].toLocalFile()
            self.open_pdf(filepath)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())