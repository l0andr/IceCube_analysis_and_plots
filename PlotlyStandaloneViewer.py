"""

Small function to be able to display plotly plots in Qt windows

"""

import os
import sys

import plotly
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication


class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig, exec=True, window_title=None):
        if window_title is None:
            window_title = 'PlotlyViewer'
        # Create a QApplication instance or use the existing one if it exists
        self.app = QApplication.instance() if QApplication.instance() else QApplication(sys.argv)

        super().__init__()
        tmp_filename = "plotly_tmp"
        i = 0
        while os.path.exists(f"{tmp_filename}{i}.html"):
            i += 1
        tmp_filename = f"{tmp_filename}{i}.html"
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), tmp_filename))
        plotly.offline.plot(fig, filename=self.file_path, auto_open=False)
        self.load(QUrl.fromLocalFile(self.file_path))
        self.setWindowTitle(window_title)
        self.show()

        if exec:
            self.app.exec_()

    def closeEvent(self, event):
        os.remove(self.file_path)
