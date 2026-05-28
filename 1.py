import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnimalHusbandryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rent_prices = {"ячмень": 120, "пшеница": 150, "подсолнечник": 100}
        self.dialog_obligations = {"ячмень": 50000, "пшеница": 25000, "подсолнечник": 32000}
        self.current_product = "ячмень"
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Определение потребности предприятия - Вариант 6")
        self.setGeometry(100, 100, 900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("Определение потребности предприятия в продукции растениеводства")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        input_group = QGroupBox("Входные данные")
        input_layout = QGridLayout()

        input_layout.addWidget(QLabel("Тип продукции:"), 0, 0)
        self.product_combo = QComboBox()
        self.product_combo.addItems(["ячмень", "пшеница", "подсолнечник"])
        self.product_combo.setCurrentText(self.current_product)
        self.product_combo.currentTextChanged.connect(self.update_product)
        input_layout.addWidget(self.product_combo, 0, 1)

        input_layout.addWidget(QLabel("Размер арендной платы за паи, ц:"), 1, 0)
        self.rent_price_label = QLabel(str(self.rent_prices[self.current_product]))
        input_layout.addWidget(self.rent_price_label, 1, 1)

        input_layout.addWidget(QLabel("Численность работников, чел.:"), 2, 0)
        self.workers_input = QLineEdit()
        input_layout.addWidget(self.workers_input, 2, 1)

        input_layout.addWidget(QLabel("Количество животных, гол.:"), 3, 0)
        self.animals_input = QLineEdit()
        input_layout.addWidget(self.animals_input, 3, 1)

        input_layout.addWidget(QLabel("Годовой норматив расхода на корм на 1 гол., ц:"), 4, 0)
        self.feed_norm_input = QLineEdit()
        input_layout.addWidget(self.feed_norm_input, 4, 1)

        input_layout.addWidget(QLabel("Потребность в реализации по договору, ц:"), 5, 0)
        self.contract_need_label = QLabel(str(self.dialog_obligations[self.current_product]))
        input_layout.addWidget(self.contract_need_label, 5, 1)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        buttons_layout = QHBoxLayout()

        self.calc_pai_btn = QPushButton("Плата за паи")
        self.calc_pai_btn.clicked.connect(self.calculate_pai_payment)
        buttons_layout.addWidget(self.calc_pai_btn)

        self.calc_animal_need_btn = QPushButton("Потребность животноводства")
        self.calc_animal_need_btn.clicked.connect(self.calculate_animal_need)
        buttons_layout.addWidget(self.calc_animal_need_btn)

        self.calc_total_btn = QPushButton("Итоговая потребность")
        self.calc_total_btn.clicked.connect(self.calculate_total_need)
        buttons_layout.addWidget(self.calc_total_btn)

        self.calc_diagram_btn = QPushButton("Диаграмма")
        self.calc_diagram_btn.clicked.connect(self.show_diagram)
        buttons_layout.addWidget(self.calc_diagram_btn)

        main_layout.addLayout(buttons_layout)

        results_group = QGroupBox("Результаты")
        results_layout = QGridLayout()

        results_layout.addWidget(QLabel("Плата за паи, ц:"), 0, 0)
        self.pai_result = QLineEdit("0")
        self.pai_result.setReadOnly(True)
        results_layout.addWidget(self.pai_result, 0, 1)

        results_layout.addWidget(QLabel("Потребность животноводства, ц:"), 1, 0)
        self.animal_need_result = QLineEdit("0")
        self.animal_need_result.setReadOnly(True)
        results_layout.addWidget(self.animal_need_result, 1, 1)

        results_layout.addWidget(QLabel("Итоговая потребность, ц:"), 2, 0)
        self.total_need_result = QLineEdit("0")
        self.total_need_result.setReadOnly(True)
        results_layout.addWidget(self.total_need_result, 2, 1)

        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)

        self.diagram_widget = QWidget()
        diagram_layout = QVBoxLayout(self.diagram_widget)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        diagram_layout.addWidget(self.canvas)
        main_layout.addWidget(self.diagram_widget)
        self.diagram_widget.hide()

    def update_product(self, product):
        self.current_product = product
        self.rent_price_label.setText(str(self.rent_prices[product]))
        self.contract_need_label.setText(str(self.dialog_obligations[product]))

    def calculate_pai_payment(self):
        try:
            workers = float(self.workers_input.text())
            if workers <= 0:
                self.pai_result.setText("Ошибка")
                return
            rent_price = float(self.rent_price_label.text())
            pai_payment = workers * rent_price
            self.pai_result.setText(f"{pai_payment:,.2f}")
        except:
            self.pai_result.setText("Ошибка")

    def calculate_animal_need(self):
        try:
            animals = float(self.animals_input.text())
            feed_norm = float(self.feed_norm_input.text())
            if animals <= 0 or feed_norm <= 0:
                self.animal_need_result.setText("Ошибка")
                return
            animal_need = animals * feed_norm
            self.animal_need_result.setText(f"{animal_need:,.2f}")
        except:
            self.animal_need_result.setText("Ошибка")

    def calculate_total_need(self):
        try:
            pai = float(self.pai_result.text().replace(',', '')) if self.pai_result.text() not in ["0", "Ошибка"] else 0
            animal = float(self.animal_need_result.text().replace(',', '')) if self.animal_need_result.text() not in [
                "0", "Ошибка"] else 0
            contract = float(self.contract_need_label.text())
            total = pai + animal + contract
            self.total_need_result.setText(f"{total:,.2f}")
        except:
            self.total_need_result.setText("Ошибка")

    def show_diagram(self):
        try:
            pai = float(self.pai_result.text().replace(',', '')) if self.pai_result.text() not in ["0", "Ошибка"] else 0
            animal = float(self.animal_need_result.text().replace(',', '')) if self.animal_need_result.text() not in [
                "0", "Ошибка"] else 0
            contract = float(self.contract_need_label.text())
            total = pai + animal + contract

            if total == 0:
                self.diagram_widget.hide()
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            labels = ['Паи', 'Животноводство', 'Договор']
            sizes = [pai, animal, contract]

            wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title(f'Распределение ({self.current_product})')

            legend_labels = [f'{label}: {size:,.1f} ц' for label, size in zip(labels, sizes)]
            ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

            self.canvas.draw()
            self.diagram_widget.show()
        except:
            self.diagram_widget.hide()


def main():
    app = QApplication(sys.argv)
    window = AnimalHusbandryApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()