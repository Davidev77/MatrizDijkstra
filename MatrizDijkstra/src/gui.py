from PyQt5 import QtWidgets, QtCore
from .logic import dijkstra, INFINITY
from .graph_widget import GraphWidget

def app_qss():
    return """
    QWidget {
        background-color: #0B0F19;
        color: #E8EAED;
        font-family: 'Segoe UI', sans-serif;
        font-size: 10pt;
    }
    QMainWindow { background-color: #0B0F19; }
    QLabel { color: #FFE81F; }
    QPushButton { background-color: #1A2333; color: #FFE81F; border: 1px solid #2D3648; border-radius: 6px; padding: 6px 10px; }
    QPushButton:hover { background-color: #223049; }
    QPushButton:pressed { background-color: #0F1726; }
    QPushButton:disabled { color: #8A8F98; border-color: #2A2F3A; }
    QLineEdit, QTextEdit, QPlainTextEdit { background-color: #0F1726; color: #E8EAED; border: 1px solid #2D3648; border-radius: 6px; selection-background-color: #00B2FF; selection-color: #0B0F19; padding: 4px 6px; }
    QScrollArea { border: none; }
    QTableWidget, QTableView { background-color: #0F1726; color: #E8EAED; gridline-color: #2D3648; selection-background-color: #00B2FF; selection-color: #0B0F19; border: 1px solid #2D3648; border-radius: 6px; }
    QHeaderView::section { background-color: #121A2A; color: #FFE81F; padding: 6px; border: 1px solid #2D3648; }
    QTableWidget QTableCornerButton::section { background: #121A2A; border: 1px solid #2D3648; }
    QScrollBar:vertical { background: #0F1726; width: 12px; margin: 0px; }
    QScrollBar::handle:vertical { background: #223049; min-height: 20px; border-radius: 6px; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    QScrollBar:horizontal { background: #0F1726; height: 12px; margin: 0px; }
    QScrollBar::handle:horizontal { background: #223049; min-width: 20px; border-radius: 6px; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
    """

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algoritmo de Dijkstra")
        self.resize(1000, 600)

        # Estado
        self.matrix = None  # lista de listas (float)
        self.table = None
        self.graph_widget = GraphWidget(None)

        # Widgets principales
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        h_layout = QtWidgets.QHBoxLayout(central)

        # Panel izquierdo: controles y tabla
        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left.setMinimumWidth(360)

        # Controles de tamaño
        size_layout = QtWidgets.QHBoxLayout()
        lbl_size = QtWidgets.QLabel("Número de nodos:")
        self.txt_size = QtWidgets.QLineEdit()
        self.txt_size.setFixedWidth(60)
        btn_generate = QtWidgets.QPushButton("Crear matriz")
        btn_generate.clicked.connect(self.crear_matriz)
        size_layout.addWidget(lbl_size)
        size_layout.addWidget(self.txt_size)
        size_layout.addWidget(btn_generate)
        left_layout.addLayout(size_layout)

        # Controles inicio/destino
        hd_layout = QtWidgets.QHBoxLayout()
        lbl_inicio = QtWidgets.QLabel("Inicio:")
        self.txt_inicio = QtWidgets.QLineEdit()
        self.txt_inicio.setFixedWidth(60)
        lbl_dest = QtWidgets.QLabel("Destino:")
        self.txt_destino = QtWidgets.QLineEdit()
        self.txt_destino.setFixedWidth(60)
        btn_calc = QtWidgets.QPushButton("Calcular camino")
        btn_calc.clicked.connect(self.calcular_camino)
        hd_layout.addWidget(lbl_inicio)
        hd_layout.addWidget(self.txt_inicio)
        hd_layout.addWidget(lbl_dest)
        hd_layout.addWidget(self.txt_destino)
        hd_layout.addWidget(btn_calc)
        left_layout.addLayout(hd_layout)

        # Área para la QTableWidget con scroll
        self.table_container = QtWidgets.QScrollArea()
        self.table_container.setWidgetResizable(True)
        left_layout.addWidget(self.table_container)


        # Resultado (texto)
        self.txt_result = QtWidgets.QTextEdit()
        self.txt_result.setReadOnly(True)
        self.txt_result.setFixedHeight(100)
        left_layout.addWidget(self.txt_result)

        h_layout.addWidget(left)

        # Panel derecho: widget de dibujo
        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.addWidget(self.graph_widget)
        h_layout.addWidget(right, 1)

    def crear_matriz(self):
        try:
            n = int(self.txt_size.text())
            if n < 2 or n > 50:
                QtWidgets.QMessageBox.warning(self, "Tamaño inválido", "Ingrese un número entre 2 y 50.")
                return
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Ingrese un entero para el tamaño.")
            return

        table = QtWidgets.QTableWidget(n, n)
        table.setMinimumSize(300, 300)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        for i in range(n):
            for j in range(n):
                item = QtWidgets.QTableWidgetItem()
                if i == j:
                    item.setText("0")
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                else:
                    item.setText("Infinito")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(i, j, item)

        self.table = table
        self.table_container.setWidget(self.table)

    def obtener_matriz_desde_tabla(self):
        if self.table is None:
            return None
        n = self.table.rowCount()
        matriz = [[INFINITY] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                item = self.table.item(i, j)
                text = item.text().strip() if item else ""
                if text.lower() in ("infinito", "inf", ""):
                    matriz[i][j] = INFINITY
                else:
                    try:
                        val = float(text)
                        if val < 0:
                            raise ValueError("Pesos negativos no permitidos")
                        matriz[i][j] = val
                    except Exception:
                        QtWidgets.QMessageBox.warning(self, "Valor inválido",
                            f"Celda ({i+1},{j+1}) contiene un valor no válido. Use número >=0 o 'Infinito'.")
                        return None
        return matriz

    def calcular_camino(self):
        matriz = self.obtener_matriz_desde_tabla()
        if matriz is None:
            return
        n = len(matriz)
        try:
            inicio = int(self.txt_inicio.text()) - 1
            destino = int(self.txt_destino.text()) - 1
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Inicio y Destino deben ser enteros.")
            return
        if not (0 <= inicio < n and 0 <= destino < n):
            QtWidgets.QMessageBox.warning(self, "Indices fuera de rango", "Asegúrese de que los nodos estén en el rango.")
            return
        if inicio == destino:
            QtWidgets.QMessageBox.information(self, "Mismo nodo", "El nodo de inicio no puede ser el mismo que el de destino.")
            return

        camino, distancia = dijkstra(matriz, inicio, destino)
        if distancia == INFINITY or not camino:
            self.txt_result.setPlainText(f"No hay camino entre {inicio+1} y {destino+1}.")
        else:
            camino_str = " ".join(str(x+1) for x in camino)
            self.txt_result.setPlainText(f"El camino más corto es: {camino_str}\nLa distancia total es: {distancia}")

        # guardar matriz y actualizar widget de dibujo en memoria
        self.matrix = matriz
        # opcional: actualizar dibujo inmediatamente
        self.graph_widget.set_matrix(self.matrix)


