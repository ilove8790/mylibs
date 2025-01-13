# myGui.py

import os
import numpy as np
from typing import Literal
from PySide6.QtCore import Signal, Qt, QSettings
from PySide6.QtGui import (
    QImage, QColor, QPixmap, QImageWriter, QAction, QPalette,
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QFileDialog, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QHeaderView, QComboBox, QMenu,
)
MY_COLOR_MAPPING = {
    'Red': QColor(255, 0, 0), 'red': QColor(255, 0, 0),
    'Green': QColor(0, 255, 0), 'green': QColor(0, 255, 0),
    'Blue': QColor(0, 0, 255), 'blue': QColor(0, 0, 255),
    'Cyan': QColor(0, 200, 255), 'cyan': QColor(0, 200, 255),
    'Magenta': QColor(255, 0, 255), 'magenta': QColor(255, 0, 255),
    'Yellow': QColor(255, 200, 0), 'yellow': QColor(255, 200, 0),
    'Black': QColor(0, 0, 0), 'black': QColor(0, 0, 0),
    'White': QColor(255, 255, 255), 'white': QColor(255, 255, 255),
    'LightRed': QColor(240, 128, 128), 'lightred': QColor(240, 128, 128), #'lightcoral'
    'LightGreen': QColor(144, 238, 144), 'lightgreen': QColor(144, 238, 144), #'lightgreen'
    'LightBlue': QColor(173, 216, 240), 'lightblue': QColor(173, 216, 240), #'lightblue'
    'Redish': QColor(255, 200, 200), 'redish': QColor(255, 200, 200), #'lightcoral'
    'Greenish': QColor(200, 255, 200), 'greenish': QColor(200, 255, 200), #'lightgreen'
    'Bluish': QColor(200, 200, 255), 'bluish': QColor(200, 200, 255), #'lightblue'
}


class MySettings(QSettings):
    """ Setting 값을 지정, 저장하는 클래스

    Args:
        settings_path (str): file_path for "settings.ini"
    """
    def __init__(self, settings_path: str):
        super().__init__(settings_path, QSettings.Format.IniFormat)

    def set(self, key: str, value):
        if str(value).lower() == "true":
            value = "True"
        elif str(value).lower() == "false":
            value = "False"
        self.setValue(key, f"{value}")
        self.sync()

    def get(self, key: str, default_value="") -> str:
        result = str(self.value(key, default_value))
        if str(result).lower() == "true":
            result = "True"
        elif str(result).lower() == "false":
            result = "False"
        return result

    def reload(self):
        self.sync()

    def set_default(self, key: str, default_value):
        if not self.contains(key):
            self.setValue(key, f"{default_value}")
            self.sync()


class MyCanvasImageWidget(QWidget):
    def __init__(self, initial_image_path=None, size=None):
        super().__init__()

        if initial_image_path is None:
            if size is None:
                width, height = 480, 540
            else:
                width, height = size[0], size[1]
            self.image_path = QImage(width, height, QImage.Format.Format_RGB32)
            self.image_path.fill(QColor(255,255,255))
        else:
            if size is None:
                width, height = 480, 540
            else:
                width, height = size[0], size[1]
            self.image_path = initial_image_path
        self.last_save_dir = ""
        self.final_filename = ""
        self.load_image()

        layout = QVBoxLayout()
        self.set_layout_spacing(layout, 0, 0, 0)

        # Create a QLabel to display the image
        self.label_image = QLabel()

        self.label_image.setScaledContents(True)
        self.label_image.setPixmap(self.image)
        self.label_image.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label_image)
        self.setLayout(layout)

    def load_image(self):
        if isinstance(self.image_path, str):
            if os.path.isfile(self.image_path):
                _, image_path_ext = os.path.splitext(self.image_path)
                image_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
                if image_path_ext.lower() in image_exts:
                    self.image = QPixmap(self.image_path)
        elif isinstance(self.image_path, QImage):
            self.image = QPixmap.fromImage(self.image_path)
        elif isinstance(self.image_path, QPixmap):
            self.image = self.image_path
        elif isinstance(self.image_path, np.ndarray):
            height, width = self.image_path.shape[:2]
            bytes_per_line = width * self.image_path.itemsize
            qimage = QImage(self.image_path.tobytes(), width, height, bytes_per_line,
                            format=QImage.Format.Format_Grayscale8)
            self.image = QPixmap.fromImage(qimage)

    def copy_image(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.image)

    def save_image(self, default_filename):
        self.final_filename, _ = QFileDialog.getSaveFileName(self, "Save Image as",
            default_filename, "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;All Files (*)")

        if self.final_filename:
            image_writer = QImageWriter(self.final_filename)
            image_writer.write(self.image.toImage())
        self.last_save_dir = os.path.dirname(self.final_filename)

    def get_filename_saved(self):
        return self.final_filename

    def set_image(self, new_image_path):
        self.image_path = new_image_path
        self.load_image()
        self.label_image.setPixmap(self.image)

    # set layout contents_margins, space between widgets
    def set_layout_spacing(self, layout, marginsLR, marginsTB, spacing):  # 여백: Left, Top, Right, Bottom
        layout.setContentsMargins(marginsLR, marginsTB, marginsLR, marginsTB)
        layout.setSpacing(spacing)



class MyCanvasTableWidget(QTableWidget):
    def __init__(self, initial_image_path=None, size=None):
        super().__init__()

        if initial_image_path is None:
            if size is None:
                width, height = 480, 540
            else:
                width, height = size[0], size[1]
            self.image_path = QImage(width, height, QImage.Format.Format_RGB32)
            self.image_path.fill(QColor(255,255,255))
        else:
            if size is None:
                width, height = 480, 540
            else:
                width, height = size[0], size[1]
            self.image_path = initial_image_path
        self.last_save_dir = ""
        self.load_image()

        layout = QVBoxLayout()
        self.set_layout_spacing(layout, 0, 0, 0)

        # Create a QLabel to display the image
        self.label_image = QLabel(self)

        self.label_image.setScaledContents(True)
        self.label_image.setPixmap(self.image)
        self.label_image.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label_image)
        self.setLayout(layout)

    def load_image(self):
        if isinstance(self.image_path, str):
            if os.path.isfile(self.image_path):
                _, image_path_ext = os.path.splitext(self.image_path)
                image_exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
                if image_path_ext.lower() in image_exts:
                    self.image = QPixmap(self.image_path)
        elif isinstance(self.image_path, QImage):
            self.image = QPixmap.fromImage(self.image_path)
        elif isinstance(self.image_path, QPixmap):
            self.image = self.image_path
        elif isinstance(self.image_path, np.ndarray):
            height, width = self.image_path.shape[:2]
            bytes_per_line = width * self.image_path.itemsize
            qimage = QImage(self.image_path.tobytes(), width, height, bytes_per_line,
                            format=QImage.Format.Format_Grayscale8)
            self.image = QPixmap.fromImage(qimage)

    def copy_image_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.image)

    def save_image_as_image(self, filename):
        image_path, _ = QFileDialog.getSaveFileName(self, "Save Image as",
            filename, "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;All Files (*)")

        if image_path:
            image_writer = QImageWriter(image_path)
            image_writer.write(self.image.toImage())
        self.last_save_dir = os.path.dirname(image_path)

    def set_image(self, new_image_path):
        self.image_path = new_image_path
        self.load_image()
        self.label_image.setPixmap(self.image)

    # set layout contents_margins, space between widgets
    def set_layout_spacing(self, layout, marginsLR, marginsTB, spacing):  # 여백: Left, Top, Right, Bottom
        layout.setContentsMargins(marginsLR, marginsTB, marginsLR, marginsTB)
        layout.setSpacing(spacing)



class MyTableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # QTableWidget 생성 및 데이터 추가
        table = QTableWidget(self)
        table.setRowCount(3)
        table.setColumnCount(3)
        for i in range(3):
            for j in range(3):
                item = QTableWidgetItem(f"Row {i}, Col {j}")
                table.setItem(i, j, item)

        layout.addWidget(table)
        self.setLayout(layout)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.window_hidden.emit()  # 창이 닫힐때 시그널을 보낸다

    window_hidden = Signal()



class MyTableWidget(QTableWidget):
    """
    QTableWidget을 기반으로 사용자 정의 클래스를 만들어,
    칼럼 헤더와 행 헤더를 리스트 형태로 받아 테이블의 행, 열을 자동으로 설정하고,
    각 셀의 값을 수정하고, 테이블 스타일을 지정할 수 있다.
    """
    def __init__(self, column_headers=None, row_headers=None, corner_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 칼럼 및 행 헤더 리스트가 제공되면 테이블의 크기를 설정
        if column_headers:
            self.setColumnCount(len(column_headers))
            self.setHorizontalHeaderLabels(column_headers)
            self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setColumnCount(1)
            # self.horizontalHeader().hide()
            self.horizontalHeader().setVisible(False)

        if row_headers:
            self.setRowCount(len(row_headers))
            self.setVerticalHeaderLabels(row_headers)
            self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setRowCount(1)
            # self.verticalHeader().hide()
            self.verticalHeader().setVisible(False)

        # # 열, 행 헤더를 중앙 정렬로 설정
        # for row in range(self.rowCount()):
        #     for col in range(self.columnCount()):
        #         self.set_cell_align(row, col, "center")
        #         # cell_item = self.item(row, col)
        #         # cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        #         # self.setItem(row, col, cell_item)

        # 셀 크기 설정
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.verticalHeader().setStretchLastSection(True)

        # 테이블 셀 선택 설정
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectColumns)
        # self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 테이블 테두리 및 행번호 숨기기
        self.setShowGrid(False)#True)
        # self.setGridStyle(Qt.PenStyle.NoPen)#.SolidLine)  # Qt::PenStyle::DotLine
        # self.verticalHeader().setVisible(False)

        # 기본 스타일 설정
        self.setStyleSheet("""
            QTableWidget { border: none; }
            QTableWidget::item {padding-left: 2px; padding-right: 2px; }
            QHeaderView::section {background-color: whitesmoke; border: none}
            """)
            # "QHeaderView::section:vertical {background-color: transparent; }", # 마지막 헤더 이후 영역의 색상 제거
        # self.horizontalHeader().setStyleSheet("""
        #     QHeaderView::section:horizontal { border: none; }
        #         # border-top: none; border-bottom: none;  #1px solid lightgrey;
        #         # border-left: none; border-right: none; }
        #     """)
        # self.verticalHeader().setStyleSheet("""
        #     QHeaderView::section:vertical {
        #         border-top: none; border-bottom: none;
        #         border-left: none; border-right: 1px solid lightgrey; }
        #     """)
        if corner_text:
            self.label_corner = QLabel(corner_text, self)
        else:
            self.label_corner = QLabel("", self)
        self.label_corner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_corner.setStyleSheet("font-weight: bold;")
        self.label_corner.setGeometry(0, 0, 
            self.verticalHeader().width(), self.horizontalHeader().height()
        )

        # 테이블 선택시 열 단위로 셀 값을 클립보드에 복사
        def copy_selected_cells():
            selected_items = self.selectedItems()
            selected_values = [item.text() for item in selected_items]
            copied_text = '\n'.join(selected_values)
            QApplication.clipboard().setText(copied_text)

        self.itemSelectionChanged.connect(copy_selected_cells)
        self.itemClicked.connect(copy_selected_cells)


    def set_table_style(self, style_sheet):
        """테이블의 스타일을 설정"""
        self.setStyleSheet(style_sheet)


    def set_column_name(self, column_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setHorizontalHeaderItem(column_index, item)


    def set_row_name(self, row_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setVerticalHeaderItem(row_index, item)


    def set_cell_value(self, row, col, value, align: Literal["center", "left", "right"]="center"):
        """셀에 값과 문자 정렬을 설정"""
        item = QTableWidgetItem(str(value))
        self.setItem(row, col, item)
        self.set_cell_align(row, col, align)


    def get_cell_value(self, row, col) -> str:
        """셀의 값을 반환"""
        item = self.item(row, col)
        return item.text() if item else ""


    def set_cell_align(self, row, col, align: Literal["center", "left", "right"]="center"):
        """셀의 문자 정렬 설정(align 기본값은 center)"""
        item = self.item(row, col)
        if item is not None:
            align_flag = Qt.AlignmentFlag.AlignCenter
            if align == "left":
                align_flag = Qt.AlignmentFlag.AlignLeft
            elif align == "right":
                align_flag = Qt.AlignmentFlag.AlignRight

            item.setTextAlignment(align_flag | Qt.AlignmentFlag.AlignVCenter)


    def set_cell_editable(self, row, col, value, align: Literal["center", "left", "right"]="center"):
        """셀에 값과 문자 정렬을 설정"""
        item = QTableWidgetItem(str(value))
        self.setItem(row, col, item)
        self.set_cell_align(row, col, align)


    def set_column_width(self, col_index: int, width: int):
        """"특정 열의 폭을 설정(width=0: 자동)"""
        self.setColumnWidth(col_index, width)


    def set_column_visible(self, col_index, hide: bool):
        """특정 열의 보임/숨김을 설정"""
        self.hideColumn(col_index) if hide else self.showColumn(col_index)


    def set_corner_label(self, corner_text: str="",
                         fgcolor: str="", bgcolor: str="",
                         align: Literal["center", "left", "right"]="center"):
        qalign = Qt.AlignmentFlag.AlignCenter
        if align == "left":
            qalign = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif align == "right":
            qalign = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, MY_COLOR_MAPPING['white'])
        palette.setColor(QPalette.ColorRole.WindowText, MY_COLOR_MAPPING['black'])
        if fgcolor in MY_COLOR_MAPPING.keys():
            palette.setColor(QPalette.ColorRole.WindowText, MY_COLOR_MAPPING[fgcolor])
        if bgcolor in MY_COLOR_MAPPING.keys():
            palette.setColor(QPalette.ColorRole.Window, MY_COLOR_MAPPING[bgcolor])

        self.label_corner.setAlignment(qalign)
        self.label_corner.setText(corner_text)
        self.label_corner.setAutoFillBackground(True)
        self.label_corner.setPalette(palette)


    def update_table(self, data: list, align: Literal["center", "left", "right"]="center"):
        """셀의 값을 모두를 한번에 갱신"""
        # nrows, ncols = self.rowCount(), self.columnCount()
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.set_cell_value(row, col, value, align)
                # item = QTableWidgetItem(cell)
                # self.set_cell_align(row, col, align=align)
                # self.setItem(row, col, item)



class MyTableWidget_Editable(QTableWidget):
    """
    QTableWidget을 기반으로 사용자 정의 클래스를 만들어,
    칼럼 헤더와 행 헤더를 리스트 형태로 받아 테이블의 행, 열을 자동으로 설정하고,
    각 셀의 값을 수정하고, 테이블 스타일을 지정할 수 있다.
    """
    def __init__(self, column_headers=None, row_headers=None, corner_text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 칼럼 및 행 헤더 리스트가 제공되면 테이블의 크기를 설정
        if column_headers:
            self.setColumnCount(len(column_headers))
            self.setHorizontalHeaderLabels(column_headers)
            self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setColumnCount(1)
            # self.horizontalHeader().hide()
            self.horizontalHeader().setVisible(False)

        if row_headers:
            self.setRowCount(len(row_headers))
            self.setVerticalHeaderLabels(row_headers)
            self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setRowCount(1)
            # self.verticalHeader().hide()
            self.verticalHeader().setVisible(False)

        # # 열, 행 헤더를 중앙 정렬로 설정
        # for row in range(self.rowCount()):
        #     for col in range(self.columnCount()):
        #         self.set_cell_align(row, col, "center")
        #         # cell_item = self.item(row, col)
        #         # cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        #         # self.setItem(row, col, cell_item)

        # 셀 크기 설정
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.verticalHeader().setStretchLastSection(True)

        # 테이블 셀 선택 설정
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectColumns)
        # self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)

        # 테이블 테두리 및 행번호 숨기기
        self.setShowGrid(False)#True)
        # self.setGridStyle(Qt.PenStyle.NoPen)#.SolidLine)  # Qt::PenStyle::DotLine
        # self.verticalHeader().setVisible(False)

        # 기본 스타일 설정
        self.setStyleSheet("""
            QTableWidget { border: none; }
            QTableWidget::item {padding-left: 2px; padding-right: 2px; }
            QHeaderView::section {background-color: whitesmoke; border: none}
            """)
            # "QHeaderView::section:vertical {background-color: transparent; }", # 마지막 헤더 이후 영역의 색상 제거
        # self.horizontalHeader().setStyleSheet("""
        #     QHeaderView::section:horizontal { border: none; }
        #         # border-top: none; border-bottom: none;  #1px solid lightgrey;
        #         # border-left: none; border-right: none; }
        #     """)
        # self.verticalHeader().setStyleSheet("""
        #     QHeaderView::section:vertical {
        #         border-top: none; border-bottom: none;
        #         border-left: none; border-right: 1px solid lightgrey; }
        #     """)
        if corner_text:
            self.label_corner = QLabel(corner_text, self)
        else:
            self.label_corner = QLabel("", self)
        self.label_corner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_corner.setStyleSheet("font-weight: bold;")
        self.label_corner.setGeometry(
            0, #self.verticalHeader().width(),  # 시작위치 X
            0, #self.horizontalHeader().height(),  # 시작위치 Y
            self.verticalHeader().width(),  # 너비
            self.horizontalHeader().height()  # 높이
        )

        # 테이블 선택시 열 단위로 셀 값을 클립보드에 복사
        def copy_selected_cells():
            selected_items = self.selectedItems()
            selected_values = [item.text() for item in selected_items]
            copied_text = '\n'.join(selected_values)
            QApplication.clipboard().setText(copied_text)

        self.itemSelectionChanged.connect(copy_selected_cells)
        self.itemClicked.connect(copy_selected_cells)


    def set_table_style(self, style_sheet):
        """테이블의 스타일을 설정"""
        self.setStyleSheet(style_sheet)


    def set_column_name(self, column_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setHorizontalHeaderItem(column_index, item)


    def set_row_name(self, row_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setVerticalHeaderItem(row_index, item)


    def set_cell_value(self, row, col, value, align: Literal["center", "left", "right"]="center"):
        """셀에 값과 문자 정렬을 설정"""
        item = QTableWidgetItem(str(value))
        self.setItem(row, col, item)
        self.set_cell_align(row, col, align)


    def get_cell_value(self, row, col) -> str:
        """셀의 값을 반환"""
        item = self.item(row, col)
        return item.text() if item else ""


    def set_column_width(self, col_index: int, width: int):
        """"특정 열의 폭을 설정(width=0: 자동)"""
        self.setColumnWidth(col_index, width)


    def set_column_visible(self, col_index, hide: bool):
        """특정 열의 보임/숨김을 설정"""
        self.hideColumn(col_index) if hide else self.showColumn(col_index)


    def set_cell_align(self, row, col, align: Literal["center", "left", "right"]="center"):
        """셀의 문자 정렬 설정(align 기본값은 center)"""
        item = self.item(row, col)
        if item is not None:
            align_flag = Qt.AlignmentFlag.AlignCenter
            if align == "left":
                align_flag = Qt.AlignmentFlag.AlignLeft
            elif align == "right":
                align_flag = Qt.AlignmentFlag.AlignRight

            item.setTextAlignment(align_flag | Qt.AlignmentFlag.AlignVCenter)


    def set_corner_label(self, corner_text: str="",
                         fgcolor: str="", bgcolor: str="",
                         align: Literal["center", "left", "right"]="center"):
        qalign = Qt.AlignmentFlag.AlignCenter
        if align == "left":
            qalign = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif align == "right":
            qalign = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, MY_COLOR_MAPPING['white'])
        palette.setColor(QPalette.ColorRole.WindowText, MY_COLOR_MAPPING['black'])
        if fgcolor in MY_COLOR_MAPPING.keys():
            palette.setColor(QPalette.ColorRole.WindowText, MY_COLOR_MAPPING[fgcolor])
        if bgcolor in MY_COLOR_MAPPING.keys():
            palette.setColor(QPalette.ColorRole.Window, MY_COLOR_MAPPING[bgcolor])

        self.label_corner.setAlignment(qalign)
        self.label_corner.setText(corner_text)
        self.label_corner.setAutoFillBackground(True)
        self.label_corner.setPalette(palette)


    def update_table(self, data: list, align: Literal["center", "left", "right"]="center"):
        """셀의 값을 모두를 한번에 갱신"""
        # nrows, ncols = self.rowCount(), self.columnCount()
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.set_cell_value(row, col, value, align)
                # item = QTableWidgetItem(cell)
                # self.set_cell_align(row, col, align=align)
                # self.setItem(row, col, item)



class MyTableWidget_Popup(QTableWidget):
    """
    QTableWidget을 기반으로 팝업되는 테이블 창을 만들어,
    칼럼 헤더와 행 헤더를 리스트 형태로 받아 테이블의 행, 열을 자동으로 설정하고,
    각 셀의 값을 수정하고, 테이블 스타일을 지정할 수 있다.
    """
    def __init__(self, column_headers=None, row_headers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 칼럼 및 행 헤더 리스트가 제공되면 테이블의 크기를 설정
        if column_headers:
            self.setColumnCount(len(column_headers))
            self.setHorizontalHeaderLabels(column_headers)
            self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setColumnCount(1)
            self.horizontalHeader().setVisible(True)

        if row_headers:
            self.setRowCount(len(row_headers))
            self.setVerticalHeaderLabels(row_headers)
            self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.setRowCount(1)
            self.verticalHeader().setVisible(True)

        # 셀 크기 설정
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.verticalHeader().setStretchLastSection(True)

        # 테이블 셀 선택 모드 설정 (기본은 개별 셀 선택 가능)
        # self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectColumns)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        # self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 오른쪽 클릭 메뉴 설정
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)


        # 테이블 테두리선, 행번호 보이기/숨기기
        self.setShowGrid(True)
        # self.setGridStyle(Qt.PenStyle.NoPen)#.SolidLine)  # Qt::PenStyle::DotLine

        # 기본 스타일 설정
        # self.setStyleSheet("""
        #     QTableWidget { border: none; }
        #     QTableWidget::item {padding-left: 2px; padding-right: 2px; }
        #     QHeaderView::section {background-color: whitesmoke; border: none}
        #     """)
        #     # "QHeaderView::section:vertical {background-color: transparent; }", # 마지막 헤더 이후 영역의 색상 제거
        # self.horizontalHeader().setStyleSheet("""
        #     QHeaderView::section:horizontal { border: none; }
        #         # border-top: none; border-bottom: none;  #1px solid lightgrey;
        #         # border-left: none; border-right: none; }
        #     """)
        # self.verticalHeader().setStyleSheet("""
        #     QHeaderView::section:vertical {
        #         border-top: none; border-bottom: none;
        #         border-left: none; border-right: 1px solid lightgrey; }
        #     """)

        # # 테이블 선택시 열 단위로 셀 값을 클립보드에 복사
        # def copy_selected_cells():
        #     selected_items = self.selectedItems()
        #     selected_values = [item.text() for item in selected_items]
        #     copied_text = '\n'.join(selected_values)
        #     QApplication.clipboard().setText(copied_text)

        # self.itemSelectionChanged.connect(copy_selected_cells)
        # self.itemClicked.connect(copy_selected_cells)


    def show_context_menu(self, position):
        context_menu = QMenu(self)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy_selected)
        context_menu.addAction(copy_action)

        context_menu.exec(self.mapToGlobal(position))


    def copy_selected(self):
        selected_items = self.selectedItems()
        clipboard = QApplication.clipboard()

        if not selected_items:
            return

        selected_ranges = self.selectedRanges()
        copy_data = []

        # 선택된 열의 헤더명 추가
        if selected_ranges:
            header_data = []
            for col in range(selected_ranges[0].leftColumn(), selected_ranges[0].rightColumn() + 1):
                header_data.append(self.horizontalHeaderItem(col).text())
            copy_data.append("\t".join(header_data))

        # 선택된 셀 데이터 추가
        for area in selected_ranges:
            for row in range(area.topRow(), area.bottomRow() + 1):
                row_data = []
                for col in range(area.leftColumn(), area.rightColumn() + 1):
                    item = self.item(row, col)
                    row_data.append(item.text() if item else "")
                copy_data.append("\t".join(row_data))

        clipboard.setText("\n".join(copy_data))


    def set_table_style(self, style_sheet):
        """테이블의 스타일을 설정"""
        self.setStyleSheet(style_sheet)


    def set_column_name(self, column_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setHorizontalHeaderItem(column_index, item)


    def set_row_name(self, row_index, new_name):
        item = QTableWidgetItem(str(new_name))
        self.setVerticalHeaderItem(row_index, item)


    def set_cell_value(self, row, col, value, align: Literal["center", "left", "right"]="center"):
        """셀에 값과 문자 정렬을 설정"""
        item = QTableWidgetItem(str(value))
        self.setItem(row, col, item)
        self.set_cell_align(row, col, align)


    def get_cell_value(self, row, col) -> str:
        """셀의 값을 반환"""
        item = self.item(row, col)
        return item.text() if item else ""


    def set_column_width(self, col_index: int, width: int):
        """"특정 열의 폭을 설정(width=0: 자동)"""
        self.setColumnWidth(col_index, width)


    def set_column_visible(self, col_index, hide: bool):
        """특정 열의 보임/숨김을 설정"""
        self.hideColumn(col_index) if hide else self.showColumn(col_index)


    def set_cell_align(self, row, col, align: Literal["center", "left", "right"]="center"):
        """셀의 문자 정렬 설정(align 기본값은 center)"""
        item = self.item(row, col)
        if item is not None:
            align_flag = Qt.AlignmentFlag.AlignCenter
            if align == "left":
                align_flag = Qt.AlignmentFlag.AlignLeft
            elif align == "right":
                align_flag = Qt.AlignmentFlag.AlignRight

            item.setTextAlignment(align_flag | Qt.AlignmentFlag.AlignVCenter)


    def update_table(self, data: list, align: Literal["center", "left", "right"]="center"):
        """셀의 값을 모두를 한번에 갱신"""
        # nrows, ncols = self.rowCount(), self.columnCount()
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.set_cell_value(row, col, value, align)
                # item = QTableWidgetItem(cell)
                # self.set_cell_align(row, col, align=align)
                # self.setItem(row, col, item)



class MyTableForm(QTableWidget):
    def __init__(self, header: list, values: list):
        super().__init__()

        # 테이블 위젯 생성
        self.table = table = QTableWidget()

        # 임시 데이타 지정
        if not values:
            values= [["Null", "Null"], ["Null", "Null"]]
        nrows, ncols = len(values), len(values[0])
        table.setRowCount(nrows)
        table.setColumnCount(ncols)

        # 헤더 미지정시 헤더 없음 처리
        if len(header) > 0:
            table.setHorizontalHeaderLabels(header)
            # col_widths = []
            # col_widths_result = []
            # for col, item in enumerate(header):
            #     self.table.setColumnWidth(col, 20)#len(item))
            #     col_widths.append(len(item))
            #     col_widths_result.append(self.table.columnWidth(col))
            # print(f"table_col_widths: {col_widths} >> {col_widths_result}")
        else:
            table.horizontalHeader().hide()

        # 테이블에 임시데이터 추가
        for row in range(nrows):
            for col in range(ncols):
                cell_item = QTableWidgetItem(values[row][col])
                cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, col, cell_item)

        # 셀 크기 설정
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        # table.horizontalHeader().setStyleSheet(Style_QTable_Header)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # table.verticalHeader().setStretchLastSection(True)

        # 테이블 셀 선택 설정
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectColumns)
        # self.table_summary.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)


        # 테이블 테두리 및 행번호 숨기기
        table.setShowGrid(False)#True)
        # table.setGridStyle(Qt.PenStyle.NoPen)#.SolidLine)  # Qt::PenStyle::DotLine
        table.verticalHeader().setVisible(False)

        # # 그리드 라인 색상 설정
        # palette = table.palette()
        # palette.setColor(QPalette.ColorRole.Base, QColor('white'))
        # palette.setColor(QPalette.ColorRole.AlternateBase, QColor('lightgrey'))
        # table.setPalette(palette)

        # 테이블 외곽선 숨기기
        table.setStyleSheet(
            """
            QTableWidget { border: none; }
            QTableWidget::item { padding-left: 2px; padding-right: 2px; }
            QHeaderView::section {
                border-top: 1px solid lightgrey; border-bottom: 1px solid lightgrey;
                border-left: none; border-right: none; }
            """)

        # # 테이블 크기를 셀 크기에 맞추기
        # total_width = table.verticalHeader().width() + table.frameWidth()*2*2
        # for col in range(table.columnCount()):
        #     total_width += table.columnWidth(col)
        # total_height = table.horizontalHeader().height() + table.frameWidth()*2*2
        # for row in range(table.rowCount()):
        #     total_height += table.rowHeight(row)
        # table.setFixedSize(total_width, total_height)

        # 테이블 선택시 열 단위로 셀 값을 클립보드에 복사
        def copy_selected_cells():
            selected_items = self.table.selectedItems()
            selected_values = [item.text() for item in selected_items]
            copied_text = '\n'.join(selected_values)
            QApplication.clipboard().setText(copied_text)

        table.itemSelectionChanged.connect(copy_selected_cells)
        table.itemClicked.connect(copy_selected_cells)
        # self.table = table

    def Table(self) -> QTableWidget:
        return self.table


    def update_table(self, new_data: list, align: Literal["center", "left", "right"]="center"):
        nrows, ncols = self.table.rowCount(), self.table.columnCount()
        if len(new_data) > nrows or len(new_data[0]) > ncols:
            new_data = [["Error!!", ""], ["Data size", "exceeds table."]]

        if align.lower() == "left":
            align_flag = Qt.AlignmentFlag.AlignLeft
        elif align.lower() == "right":
            align_flag = Qt.AlignmentFlag.AlignRight
        else:
            align_flag = Qt.AlignmentFlag.AlignCenter

        for row, items in enumerate(new_data):
            for col, item in enumerate(items):
                cell_item = QTableWidgetItem(item)
                cell_item.setTextAlignment(align_flag | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, cell_item)

    def get(self, row: int, col: int) -> str:
        item = self.table.item(row, col)
        if item:
            return item.text()
        return ""



class MyTableWidget_withInnerComboFilter(QTableWidget):
    """1행에 콤보필터를 가진 테이블 위젯

    Parameters:
    -----------
    headers : list of string
        Names of each column.
    data : list
        Data for each cell of table

    Examples:
    ---------
    >>> headers = ["Header 1", "Header 2", "Header 3", "Header 4"]
    >>> data = [["Cell 1-1", "Cell 1-2", "Cell 1-3", "Cell 1-4"],
                ["Cell 2-1", "Cell 2-2", "Cell 2-3", "Cell 2-4"], ]
    >>> table = QxTableWithComboFilter(headers, data)
    """

    def __init__(self, headers, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = headers
        self.data = data
        self.setColumnCount(len(headers))
        self.setRowCount(len(data) + 1)  # 필터 행 추가
        self.setHorizontalHeaderLabels(headers)
        self.populate_table(data)
        self.filters = [QComboBox() for _ in headers]
        self.init_filters()

    def populate_table(self, data):
        for row, items in enumerate(data, start=1):
            for col, item in enumerate(items):
                cell_item = QTableWidgetItem(item)
                cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, cell_item)

    def init_filters(self):
        for col, combo in enumerate(self.filters):
            unique_values = sorted(set(self.item(row, col).text() for row in range(1, self.rowCount())))
            combo.addItem("All")  # 모든 항목을 표시하는 기본 옵션
            combo.addItems(unique_values)
            combo.currentIndexChanged.connect(self.apply_filters)
            self.setCellWidget(0, col, combo)
        self.setRowHidden(0, False)  # 필터 행 표시

    def apply_filters(self):
        filter_texts = [combo.currentText() for combo in self.filters]

        for row in range(1, self.rowCount()):
            item_visible = True
            for col, filter_text in enumerate(filter_texts):
                if filter_text != "All" and filter_text not in self.item(row, col).text():
                    item_visible = False
                    break
            self.setRowHidden(row, not item_visible)

    # def update_data(self):
    #     self.populate_table(data)



class MyTableWidget_withUpperComboFilter(QTableWidget):
    """1행에 콤보필터를 가진 테이블 위젯

    Parameters:
    -----------
    headers : list of string
        Names of each column.
    data : list
        Data for each cell of table

    Examples:
    ---------
    >>> headers = ["Header 1", "Header 2", "Header 3", "Header 4"]
    >>> data = [["Cell 1-1", "Cell 1-2", "Cell 1-3", "Cell 1-4"],
                ["Cell 2-1", "Cell 2-2", "Cell 2-3", "Cell 2-4"], ]
    >>> table = QxTableWithComboFilter(headers, data)
    """

    def __init__(self, headers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.headers = headers
        self.filters = []

        # 콤보 박스를 포함한 필터 레이아웃 설정
        self.filter_layout = QHBoxLayout()
        for header in headers:
            combo_filter = QComboBox()
            combo_filter.addItem(f"All {header}")
            combo_filter.currentIndexChanged.connect(self.apply_filters)
            self.filter_layout.addWidget(combo_filter)
            self.filters.append(combo_filter)

        layout.addLayout(self.filter_layout)

        # 테이블 위젯 설정
        self.table = QTableWidget(0, len(headers))  # 초기에는 행이 없음, 열만 정의
        self.table.setHorizontalHeaderLabels(headers)
        layout.addWidget(self.table)

    def add_data(self):
        # 예시 데이터를 추가합니다
        data = [
            [10, 20, "Option 1", "Cell 1-4"],
            [5, 15, "Option 2", "Cell 2-4"],
            [30, 25, "Option 3", "Cell 3-4"],
            [20, 10, "Option 4", "Cell 4-4"]
        ]

        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + len(data))

        for row, items in enumerate(data, start=current_row_count):
            for col, item in enumerate(items):
                cell_item = QTableWidgetItem(str(item))
                cell_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, cell_item)

                # 콤보 박스에 필터 옵션 추가
                if str(item) not in [self.filters[col].itemText(i) for i in range(self.filters[col].count())]:
                    self.filters[col].addItem(str(item))

    def apply_filters(self):
        for row in range(self.table.rowCount()):
            row_hidden = False
            for col, combo_filter in enumerate(self.filters):
                if combo_filter.currentIndex() != 0:
                    item = self.table.item(row, col)
                    if item and item.text() != combo_filter.currentText():
                        row_hidden = True
                        break
            self.table.setRowHidden(row, row_hidden)



class MyTableWidget_simple(QTableWidget):
    """
    기본형 테이블

    Parameters:
    -----------
    headers : list of string
        Names of each column.

    Examples:
    ---------
    >>> headers = ["Header 1", "Header 2", "Header 3", "Header 4"]
    >>> data = [["Cell 1-1", "Cell 1-2", "Cell 1-3", "Cell 1-4"],
                ["Cell 2-1", "Cell 2-2", "Cell 2-3", "Cell 2-4"], ]
    >>> table = QxTableWithComboFilter(headers)
    >>> table.set_cell_value(data)
    """

    def __init__(self, headers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = headers
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setMinimumSectionSize(50)
        self.setSelectionMode(QAbstractItemView.selectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        # 헤더 클릭 이벤트 연결
        self.horizontalHeader().sectionClicked.connect(self.copy_column)
        self.verticalHeader().sectionClicked.connect(self.handle_row_click)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            item = self.itemAt(event.pos())
            if item:
                self.show_context_menu(event.pos(), item)
        super().mousePressEvent(event)

    def copy_column(self, logicalIndex):
        column_data = []
        for row in range(self.rowCount()):
            item = self.item(row, logicalIndex)
            if item:
                column_data.append(item.text())
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(column_data))
        print(f"Copied column {logicalIndex} data to clipboard.")

    def copy_row(self, logicalIndex):
        row_data = []
        for col in range(self.columnCount()):
            item = self.item(logicalIndex, col)
            if item:
                row_data.append(item.text())
        clipboard = QApplication.clipboard()
        clipboard.setText("\t".join(row_data))
        print(f"Copied row {logicalIndex} data to clipboard.")

    def handle_row_click(self, logicalIndex):
        col0_item = self.item(logicalIndex, 0)
        col1_item = self.item(logicalIndex, 1)
        col0_text = col0_item.text() if col0_item else ""
        col1_text = col1_item.text() if col1_item else ""
        print(f"Row {logicalIndex} Column 0: {col0_text}, Column 1: {col1_text}")

    def show_context_menu(self, position, item):
        context_menu = QMenu(self)

        copy_action = QAction("Copy Cell", self)
        copy_action.triggered.connect(lambda: self.copy_cell(item))
        context_menu.addAction(copy_action)

        # 서브메뉴 추가
        sub_menu = QMenu("Sub Menu", self)

        sub_action1 = QAction("Sub Action 1", self)
        sub_action1.triggered.connect(lambda: self.sub_action_1(item))
        sub_menu.addAction(sub_action1)

        sub_action2 = QAction("Sub Action 2", self)
        sub_action2.triggered.connect(lambda: self.sub_action_2(item))
        sub_menu.addAction(sub_action2)

        context_menu.addMenu(sub_menu)

        context_menu.exec(self.mapToGlobal(position))

    def copy_cell(self, item):
        clipboard = QApplication.clipboard()
        clipboard.setText(item.text())
        print(f"Copied cell data: {item.text()}")

    def sub_action_1(self, item):
        print(f"Sub Action 1 triggered on cell: {item.text()}")

    def sub_action_2(self, item):
        print(f"Sub Action 2 triggered on cell: {item.text()}")



class MyTableWidget_subMenu(QTableWidget):
    """
    마우스 오른버튼 클릭시 서브메뉴를 보여주는 테이블

    Parameters:
    -----------
    headers : list of string
        Names of each column.
    data : list
        Data for each cell of table

    Examples:
    ---------
    >>> headers = ["Header 1", "Header 2", "Header 3", "Header 4"]
    >>> data = [["Cell 1-1", "Cell 1-2", "Cell 1-3", "Cell 1-4"],
                ["Cell 2-1", "Cell 2-2", "Cell 2-3", "Cell 2-4"], ]
    >>> table = QxTableWithComboFilter(headers, data)
    """

    def __init__(self, headers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = headers
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setMinimumSectionSize(50)
        self.setSelectionMode(QAbstractItemView.selectionMode.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        # 헤더 클릭 이벤트 연결
        self.horizontalHeader().sectionClicked.connect(self.copy_column)
        self.verticalHeader().sectionClicked.connect(self.handle_row_click)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            item = self.itemAt(event.pos())
            if item:
                self.show_context_menu(event.pos(), item)
        super().mousePressEvent(event)

    def copy_column(self, logicalIndex):
        column_data = []
        for row in range(self.rowCount()):
            item = self.item(row, logicalIndex)
            if item:
                column_data.append(item.text())
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(column_data))
        print(f"Copied column {logicalIndex} data to clipboard.")

    def copy_row(self, logicalIndex):
        row_data = []
        for col in range(self.columnCount()):
            item = self.item(logicalIndex, col)
            if item:
                row_data.append(item.text())
        clipboard = QApplication.clipboard()
        clipboard.setText("\t".join(row_data))
        print(f"Copied row {logicalIndex} data to clipboard.")

    def handle_row_click(self, logicalIndex):
        col0_item = self.item(logicalIndex, 0)
        col1_item = self.item(logicalIndex, 1)
        col0_text = col0_item.text() if col0_item else ""
        col1_text = col1_item.text() if col1_item else ""
        print(f"Row {logicalIndex} Column 0: {col0_text}, Column 1: {col1_text}")

    def show_context_menu(self, position, item):
        context_menu = QMenu(self)

        copy_action = QAction("Copy Cell", self)
        copy_action.triggered.connect(lambda: self.copy_cell(item))
        context_menu.addAction(copy_action)

        # 서브메뉴 추가
        sub_menu = QMenu("Sub Menu", self)

        sub_action1 = QAction("Sub Action 1", self)
        sub_action1.triggered.connect(lambda: self.sub_action_1(item))
        sub_menu.addAction(sub_action1)

        sub_action2 = QAction("Sub Action 2", self)
        sub_action2.triggered.connect(lambda: self.sub_action_2(item))
        sub_menu.addAction(sub_action2)

        context_menu.addMenu(sub_menu)

        context_menu.exec(self.mapToGlobal(position))

    def copy_cell(self, item):
        clipboard = QApplication.clipboard()
        clipboard.setText(item.text())
        print(f"Copied cell data: {item.text()}")

    def sub_action_1(self, item):
        print(f"Sub Action 1 triggered on cell: {item.text()}")

    def sub_action_2(self, item):
        print(f"Sub Action 2 triggered on cell: {item.text()}")



class WaitingPopup(QMainWindow):
    """ 실행중일때 대기화면 표시후, 완료시 자동소멸하는 안내창
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information")
        layout = QVBoxLayout()
        label = QLabel("Please Wait in progress...")
        layout.addWidget(label)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 300, 100)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.show()



# set layout contents_margins, space between widgets
def set_layout_spacing(layout, marginsLR, marginsTB, spacing):  # 여백: Left, Top, Right, Bottom
    layout.setContentsMargins(marginsLR, marginsTB, marginsLR, marginsTB)
    layout.setSpacing(spacing)



def __example__make_doc(shape, dtype=None, order='C'):
    """Return a new matrix of given shape and type, without initializing entries.

    Parameters
    ----------
    shape : int or tuple of int
        Shape of the empty matrix.
    dtype : data-type, optional
        Desired output data-type.
    order : {'C', 'F'}, optional
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.

    See Also
    --------
    numpy.empty : Equivalent array function.
    matlib.zeros : Return a matrix of zeros.

    Notes
    -----
    Unlike other matrix creation functions (e.g. `matlib.zeros`,
    `matlib.ones`), `matlib.empty` does not initialize the values of the
    matrix, and may therefore be marginally faster.

    Examples
    --------
    >>> import numpy.matlib
    >>> np.matlib.empty((2, 2))    # filled with random data
    matrix([[  6.76425276e-320,   9.79033856e-307], # random
            [  7.39337286e-309,   3.22135945e-309]])
    >>> np.matlib.empty((2, 2), dtype=int)
    matrix([[ 6600475,        0], # random
            [ 6586976, 22740995]])

    """
    return order



