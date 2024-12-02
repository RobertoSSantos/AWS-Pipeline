# import sys
# import os
# import zipfile
# import boto3
# from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton
# from PySide6.QtCore import Qt, QThread, Signal

# class DeployWorker(QThread):
#     progress = Signal(int)
#     message = Signal(str)
#     finished = Signal()

#     def __init__(self, function_name, code_files):
#         super().__init__()
#         self.function_name = function_name
#         self.code_files = code_files

#     def run(self):
#         try:
#             self.progress.emit(10)
#             self.message.emit("Iniciando a compactação do código...")

#             # Compacta o código em um arquivo ZIP
#             zip_file_name = f"{self.function_name}.zip"
#             with zipfile.ZipFile(zip_file_name, 'w') as zipf:
#                 for file in self.code_files:
#                     zipf.write(file, os.path.basename(file))
#             self.progress.emit(40)
#             self.message.emit("Compactação concluída.")

#             self.progress.emit(50)
#             self.message.emit("Conectando ao AWS Lambda...")

#             # Conecta ao AWS Lambda usando boto3
#             lambda_client = boto3.client('lambda')

#             # Verifica se a função Lambda já existe
#             try:
#                 response = lambda_client.get_function(FunctionName=self.function_name)
#                 function_exists = True
#                 self.message.emit("Função Lambda existente encontrada. Atualizando a função...")
#             except lambda_client.exceptions.ResourceNotFoundException:
#                 function_exists = False
#                 self.message.emit("Função Lambda não encontrada. Criando uma nova função...")

#             # Lê o conteúdo do arquivo zip
#             with open(zip_file_name, 'rb') as f:
#                 zipped_code = f.read()

#             if function_exists:
#                 # Atualiza a função Lambda existente
#                 lambda_client.update_function_code(
#                     FunctionName=self.function_name,
#                     ZipFile=zipped_code,
#                 )
#             else:
#                 # Cria uma nova função Lambda
#                 role_arn = self.get_execution_role()
#                 lambda_client.create_function(
#                     FunctionName=self.function_name,
#                     Runtime='python3.9',
#                     Role=role_arn,
#                     Handler='lambda_function.lambda_handler',
#                     Code={'ZipFile': zipped_code},
#                     Description='Função Lambda implantada via interface PySide6',
#                     Timeout=15,
#                     MemorySize=128,
#                     Publish=True,
#                 )

#             self.progress.emit(90)
#             self.message.emit("Deploy concluído com sucesso.")

#             self.progress.emit(100)
#             self.message.emit("Processo finalizado.")

#             self.finished.emit()

#             # Remove o arquivo zip temporário
#             if os.path.exists(zip_file_name):
#                 os.remove(zip_file_name)

#         except Exception as e:
#             self.message.emit(f"Erro: {str(e)}")
#             self.finished.emit()

#     def get_execution_role(self):
#         """
#         Retorna o ARN de uma role de execução existente ou cria uma nova.
#         """
#         iam_client = boto3.client('iam')
#         role_name = 'Lambda_Execution_Role'

#         try:
#             role = iam_client.get_role(RoleName=role_name)
#             return role['Role']['Arn']
#         except iam_client.exceptions.NoSuchEntityException:
#             # Cria uma nova role
#             assume_role_policy_document = {
#                 "Version": "2012-10-17",
#                 "Statement": [
#                     {
#                         "Action": "sts:AssumeRole",
#                         "Principal": {
#                             "Service": "lambda.amazonaws.com"
#                         },
#                         "Effect": "Allow",
#                         "Sid": ""
#                     }
#                 ]
#             }
#             role = iam_client.create_role(
#                 RoleName=role_name,
#                 AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
#                 Description='Role de execução para funções Lambda',
#             )
#             # Anexa a política AWSLambdaBasicExecutionRole
#             iam_client.attach_role_policy(
#                 RoleName=role_name,
#                 PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
#             )
#             # Aguarda a propagação da criação da role
#             time.sleep(10)
#             return role['Role']['Arn']

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Deploy para AWS Lambda")

#         # Cria os elementos da interface
#         self.label = QLabel("Clique em 'Iniciar Deploy' para começar o processo.")
#         self.label.setAlignment(Qt.AlignCenter)

#         self.progress_bar = QProgressBar()
#         self.progress_bar.setRange(0, 100)

#         self.start_button = QPushButton("Iniciar Deploy")
#         self.start_button.clicked.connect(self.start_process)

#         # Configura o layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         layout.addWidget(self.progress_bar)
#         layout.addWidget(self.start_button)

#         self.setLayout(layout)

#         self.worker = None

#     def start_process(self):
#         self.label.setText("Preparando o código para o deploy...")
#         self.progress_bar.setValue(0)
#         self.start_button.setEnabled(False)

#         # Código a ser implantado
#         code_files = ['lambda_function.py']

#         # Cria o arquivo 'lambda_function.py' com o código fornecido
#         with open('lambda_function.py', 'w') as f:
#             f.write("""
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, Flask running on Lambda!"

# def lambda_handler(event, context):
#     return {
#         "statusCode": 200,
#         "body": home()
#     }
# """)

#         function_name = 'MyLambdaFunction'  # Nome da função Lambda

#         # Cria e inicia a thread de trabalho
#         self.worker = DeployWorker(function_name, code_files)
#         self.worker.progress.connect(self.update_progress)
#         self.worker.message.connect(self.update_message)
#         self.worker.finished.connect(self.process_finished)
#         self.worker.start()

#     def update_progress(self, value):
#         self.progress_bar.setValue(value)

#     def update_message(self, message):
#         self.label.setText(message)

#     def process_finished(self):
#         self.start_button.setEnabled(True)

# if __name__ == "__main__":
#     import json
#     import time

#     app = QApplication(sys.argv)

#     window = MainWindow()
#     window.resize(500, 200)
#     window.show()

#     sys.exit(app.exec())


from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
import sys

# Código Flask original
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask running on Lambda!"

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": home()
    }

# Interface gráfica
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lambda Simulator")

        # Rótulo para exibir a mensagem
        self.label = QLabel("Clique on the button to run the application")
        self.label.setAlignment(Qt.AlignCenter)

        # Botão para chamar a função 'home()'
        self.button = QPushButton("RUN")
        self.button.clicked.connect(self.call_home)

        # Configura o layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def call_home(self):
        # Simula uma chamada à função 'home()' do Flask
        result = home()
        self.label.setText(f"Status':\n{result}")

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)

    window = MainWindow()
    window.resize(400, 200)
    window.show()

    sys.exit(app_qt.exec())
