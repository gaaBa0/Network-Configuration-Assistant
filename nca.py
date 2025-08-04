
import sys
import google.generativeai as genai
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

#Chave API
genai.configure(api_key="#######################################")

#PROMPT_TEMPLATE é o que vai dar contexto ao bot e vai fazê-lo ser mais objetivo com seu resultado
PROMPT_TEMPLATE = """Você é um mestre de automação de redes e configuração de roteadores, switchs, firewalls, mikrotiks e servidores linux e windows.

Seu trabalho é converter o INPUT dado em comandos de CLI do determinado equipamento para completar a tarefa dada.

Output:
- CLI script ou comandos CLI passo-a-passo para o determinado equipamento
- Uma explicação firme de cada comando (se requisitado)
- Gerar apenas o necessário e nada mais.

--- INPUT START
{input}
--- INPUT END

REPLY:
"""

#Cria a classe que vai chamar o app
class CFGAssistant(QWidget):
    #Função chamada automaticamente ao criar a classe para fazer a janela do app
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NCA by MorningStar") #Define o titulo
        self.setGeometry(100, 100, 600, 500) #Dimensão
        self.setWindowIcon(QIcon("C:/Users/marketing/Documents/Programação/Python/mktk/app_icon.ico")) #Ícone

        self.layout = QVBoxLayout() #Tipo do layout
        self.setLayout(self.layout)

        self.history = QTextEdit() #Campo do texto onde fica a conversa atual
        self.history.setReadOnly(True) #Modo leitura
        self.layout.addWidget(QLabel("Histórico de Conversa:"))
        self.layout.addWidget(self.history)

        self.input_field = QLineEdit() #Texto que fica em cima do input
        self.input_field.setPlaceholderText("Descreva a configuração desejada...")
        self.layout.addWidget(self.input_field) #Input de texto

        self.send_button = QPushButton("Enviar") #Botão para enviar
        self.send_button.clicked.connect(self.handle_query)
        self.layout.addWidget(self.send_button)

    def handle_query(self):
        user_input = self.input_field.text().strip() #Puxa o input da outra função
        if not user_input: #Se estiver vazio retorna vazio
            return

        self.history.append(f"👤 Você: {user_input}") #Coloca seu input na caixa de historico
        self.input_field.clear() #Limpa o campo do input
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            prompt = PROMPT_TEMPLATE.format(input=user_input) #Define o prompt com o nosso template e o input do usuario
            model = genai.GenerativeModel(model_name="gemini-2.0-flash") #Escolhe o modelo da i.a
            response = model.generate_content(prompt) #Gera uma resposta de acordo com o template
            reply = response.text.strip() #Transforma a resposta em texto puro
            self.history.append(f"🤖 NCA:{reply}\n") #Coloca a resposta dentro do historico 
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e)) #Retorna erro
        finally:
            QApplication.restoreOverrideCursor()

if __name__ == "__main__": #Inicia o código caso seja executado nele mesmo
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = CFGAssistant()
    window.show()
    sys.exit(app.exec_())
