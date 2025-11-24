from PyQt5 import QtWidgets, QtGui, QtCore
import math
from .logic import INFINITY

class GraphWidget(QtWidgets.QWidget):
    def __init__(self, matrix=None, parent=None):
        super().__init__(parent)
        self.matrix = matrix
        self.setMinimumSize(500, 500)
        self.node_radius = 16
        self.node_color = QtGui.QColor("#00B2FF")
        self.edge_color = QtGui.QColor("#9AA0A6")
        self.text_color = QtGui.QColor("#FFE81F")
        self.background_color = QtGui.QColor("#0B0F19")

    def set_matrix(self, matrix):
        self.matrix = matrix
        self.update()

    def sizeHint(self):
        return QtCore.QSize(600, 600)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, self.background_color)

        if not self.matrix or len(self.matrix) == 0:
            painter.setPen(QtGui.QPen(self.text_color))
            painter.drawText(rect, QtCore.Qt.AlignCenter, "Sin matriz")
            painter.end()
            return

        n = len(self.matrix)
        w, h = self.width(), self.height()
        radius = max(10, min(w, h) // 2 - 60)
        cx, cy = w // 2, h // 2

        # Posiciones en círculo
        positions = []
        for i in range(n):
            angle = 2 * math.pi * i / max(1, n)
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))
            positions.append(QtCore.QPointF(x, y))

        painter.setPen(QtGui.QPen(self.edge_color, 2))
        painter.setFont(QtGui.QFont('Segoe UI', 10))

        # Aristas con flechas y pesos
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                w_ij = self.matrix[i][j]
                if w_ij is None or w_ij == INFINITY:
                    continue

                p1 = positions[i]
                p2 = positions[j]
                angle = math.atan2(p2.y() - p1.y(), p2.x() - p1.x())

                end_x = p2.x() - (self.node_radius + 4) * math.cos(angle)
                end_y = p2.y() - (self.node_radius + 4) * math.sin(angle)
                end_pt = QtCore.QPointF(end_x, end_y)

                painter.setPen(QtGui.QPen(self.edge_color, 2))
                painter.drawLine(p1, end_pt)

                # Etiqueta de peso (desplazada si hay arista contraria distinta)
                mid_x = (p1.x() + p2.x()) / 2
                mid_y = (p1.y() + p2.y()) / 2
                offset_x = 0
                offset_y = 0
                w_ji = self.matrix[j][i] if 0 <= j < n and 0 <= i < n else INFINITY
                if w_ji != INFINITY and w_ji != w_ij:
                    shift = 10
                    dx = p2.x() - p1.x()
                    dy = p2.y() - p1.y()
                    length = math.hypot(dx, dy) or 1.0
                    px = -dy / length
                    py = dx / length
                    offset_x = px * shift
                    offset_y = py * shift

                painter.setPen(QtGui.QPen(self.text_color))
                painter.drawText(QtCore.QPointF(mid_x + offset_x, mid_y + offset_y), str(w_ij))

                # Flecha
                self._draw_arrow(painter, end_pt, angle)

        # Nodos
        painter.setFont(QtGui.QFont('Segoe UI', 11, QtGui.QFont.Bold))
        for idx, pos in enumerate(positions):
            rect = QtCore.QRectF(
                pos.x() - self.node_radius,
                pos.y() - self.node_radius,
                self.node_radius * 2,
                self.node_radius * 2,
            )
            painter.setBrush(QtGui.QBrush(self.node_color))
            painter.setPen(QtGui.QPen(self.edge_color))

            painter.drawEllipse(rect)
            painter.setPen(QtGui.QPen(self.text_color))
            painter.drawText(rect, QtCore.Qt.AlignCenter, str(idx + 1))

        painter.end()

    def _draw_arrow(self, painter: QtGui.QPainter, end_pt: QtCore.QPointF, angle: float):
        size = 10
        left = QtCore.QPointF(
            end_pt.x() - size * math.cos(angle - math.pi / 6),
            end_pt.y() - size * math.sin(angle - math.pi / 6),
        )
        right = QtCore.QPointF(
            end_pt.x() - size * math.cos(angle + math.pi / 6),
            end_pt.y() - size * math.sin(angle + math.pi / 6),
        )
        painter.drawLine(end_pt, left)
        painter.drawLine(end_pt, right)