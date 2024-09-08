from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model import AirportModel

class AirportView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.model = None  # Initialize model as None

    def init_ui(self):
        self.setWindowTitle("Airport Finder")
        self.resize(1000, 850)

        # Параметры подключения
        self.host_label = QLabel("Хост:")
        self.host_entry = QLineEdit()
        self.host_entry.setText("localhost")
        self.database_label = QLabel("База данных:")
        self.database_entry = QLineEdit()
        self.database_entry.setText("flights")
        self.user_label = QLabel("Пользователь:")
        self.user_entry = QLineEdit()
        self.user_entry.setText("User")
        self.password_label = QLabel("Пароль:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)  # скрыть пароль

        # Фильтры
        self.min_lat_label = QLabel("Min latitude:")
        self.min_lat_entry = QLineEdit()
        self.min_lat_entry.setText("30.0")
        self.max_lat_label = QLabel("Max latitude:")
        self.max_lat_entry = QLineEdit()
        self.max_lat_entry.setText("70.0")
        self.min_lon_label = QLabel("Min longitude:")
        self.min_lon_entry = QLineEdit()
        self.min_lon_entry.setText("30.0")
        self.max_lon_label = QLabel("Max longitude:")
        self.max_lon_entry = QLineEdit()
        self.max_lon_entry.setText("70.0")

        # Кнопки
        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.connect_to_database)
        self.apply_button = QPushButton("Применить фильтр")
        self.apply_button.setEnabled(False)  # Кнопка "Применить фильтр" отключена по умолчанию
        self.apply_button.clicked.connect(self.apply_filter)

        # Таблица
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Город", "Страна", "Широта", "Долгота"])

        # Размещение элементов
        main_layout = QVBoxLayout()
        connection_layout = QHBoxLayout()
        connection_layout.addWidget(self.host_label)
        connection_layout.addWidget(self.host_entry)
        connection_layout.addWidget(self.database_label)
        connection_layout.addWidget(self.database_entry)
        connection_layout.addWidget(self.user_label)
        connection_layout.addWidget(self.user_entry)
        connection_layout.addWidget(self.password_label)
        connection_layout.addWidget(self.password_entry)
        connection_layout.addWidget(self.connect_button)
        main_layout.addLayout(connection_layout)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.min_lat_label)
        filter_layout.addWidget(self.min_lat_entry)
        filter_layout.addWidget(self.max_lat_label)
        filter_layout.addWidget(self.max_lat_entry)
        filter_layout.addWidget(self.min_lon_label)
        filter_layout.addWidget(self.min_lon_entry)
        filter_layout.addWidget(self.max_lon_label)
        filter_layout.addWidget(self.max_lon_entry)
        filter_layout.addWidget(self.apply_button)
        main_layout.addLayout(filter_layout)

        main_layout.addWidget(self.table_widget)
        self.setLayout(main_layout)

    def connect_to_database(self):
        host = self.host_entry.text()
        database = self.database_entry.text()
        user = self.user_entry.text()
        password = self.password_entry.text()
        self.model = AirportModel(host, database, user, password)
        if self.model.connect():
            QMessageBox.information(self, "Успешно", "Подключение к базе данных установлено")
            self.connect_button.setEnabled(False)
            self.apply_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Ошибка", "Ошибка при подключении к базе данных")

    def apply_filter(self):
        try:
            min_lat = float(self.min_lat_entry.text())
            max_lat = float(self.max_lat_entry.text())
            min_lon = float(self.min_lon_entry.text())
            max_lon = float(self.max_lon_entry.text())
            if min_lat > max_lat or min_lon > max_lon:
                raise ValueError("Минимальные значения не могут быть больше максимальных.")
            airports = self.model.get_airports(min_lat, max_lat, min_lon, max_lon)
            self.update_table(airports)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректный ввод данных для фильтров: {e}")

    def update_table(self, airports):
        self.table_widget.setRowCount(len(airports))
        for i, airport in enumerate(airports):
            for j, value in enumerate(airport):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)

    def closeEvent(self, event):
        if self.model:
            self.model.close_connection()
        super().closeEvent(event)