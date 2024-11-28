import sys 
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import design
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Создаем FigureCanvas и добавляем его в self.widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.widget.setLayout(layout)

        self.pushButtonCalculate.clicked.connect(self.simulate)
        self.pushButtonClean.clicked.connect(self.clean)
    
    def clean(self):
        self.figure.clear()
        self.canvas.draw()  

    def simulate(self):
        # Генерация случайных данных для примера
        np.random.seed(0)  # Установите семя для воспроизводимости
        components = self.spinBoxComponents.value()  # Получаем количество компонентов из spinBox
        data = np.random.rand(1000, 5)  # Генерация 1000 образцов, 5 признаков (сенсоров)

        # Преобразуем данные в DataFrame для удобства
        df = pd.DataFrame(data, columns=[f'Sensor_{i+1}' for i in range(data.shape[1])])

        # Стандартизация данных
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)

        # Применение PCA с количеством компонентов из spinBox
        pca = PCA(n_components=components)  # Уменьшаем размерность до указанного количества
        principal_components = pca.fit_transform(scaled_data)

        # Создаем DataFrame для главных компонент
        pc_df = pd.DataFrame(data=principal_components, columns=[f'Principal Component {i+1}' for i in range(components)])

        # Очищаем фигуру перед отрисовкой нового графика
        self.figure.clear()

        # Создаем новый subplot
        ax = self.figure.add_subplot(111)

        # Отображаем только первые два главных компонента, если их больше
        if components >= 2:
            ax.scatter(pc_df['Principal Component 1'], pc_df['Principal Component 2'], alpha=0.7)
            ax.set_title('PCA of Multisensor Data')
            ax.set_xlabel('Principal Component 1')
            ax.set_ylabel('Principal Component 2')
            ax.grid() 
            ax.axhline(0, color='black', lw=0.5, ls='--')
            ax.axvline(0, color='black', lw=0.5, ls='--')
        else:
            ax.text(0.5, 0.5, 'Not enough components to plot', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

        # Обновляем canvas
        self.canvas.draw()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main() 
