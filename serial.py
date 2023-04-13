#######################################################################################################################################################################
# Bom dia, meninas.

# Mesmo tendo saído do CNPEM, achei que poderia ao menos usar meu tempo livre para tentar ajudar vocês. Sendo assim, passei alguns dias pesquisando e acho que encontrei uma forma de fazer com que o programa faça o tal loop de atualização de valores. 

# Então, este código seria para ler valores vindo de uma comunicação serial e exibi-los no botão. 
# O segredo está na função self.timer.timeout.connect(self.read_serial): 
#   >"timer" é o nome que damos ao nosso temporizador, importado via 'from PyQt6.QtCore import QTimer';
#   >timeout.connect(self.read_serial) é responsável por executar a função 'read_serial()' quando o timer zera (o que ocorre a cada 3s, como definido por 'self.timer.start(3000)')

# Sugiro que esudem este código e busquem implementar algo parecido na interface.py

# Abraços.
#######################################################################################################################################################################

import sys
import serial
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 150)
        self.port = serial.Serial('COM4', 9600, timeout=0.1) #Comentário Define a conexão serial. Aqui, vocês precisam mudar os parâmetros de acordo com a sua conexão.
        self.data = ""
        self.timer = QTimer(self) #Comentário Nomeia o timer como "timer"
        self.timer.timeout.connect(self.read_serial) #Comentário Quando o timer zerar, o prograa chama a função "read_serial()"
        self.timer.start(3000) #Comentário Define que o timer zera a cada 3s
        self.button = QPushButton(self) #Comentário Cria o botão no qual vamos exibir nosso número vindo do serial.
        self.button.setGeometry(50, 50, 200, 50)
        self.button.setText("No Data Yet")
        self.label = QLabel(self) #Comentário Cria um label para mostrar a situação do programa
        self.label.setGeometry(50, 100, 200, 20)
        self.label.setText("Waiting for data...")
        
    def read_serial(self):
        if self.port.in_waiting > 0: #Comentário Se há dados vindo pelo serial...
            self.data = self.port.readline().decode().strip() #Comentário Lê os dados e os salva na string "data"
            self.button.setText(self.data) #Comentário Define o texto do botão como a string "data", que recebeu os valores vindos do serial. 
            self.label.setText("Data received successfully!")
    
    def closeEvent(self, event):
        self.timer.stop()
        self.port.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
