# **AWS-Pipeline: Deploy Automatizado de Aplicação Python na AWS**

Automatize o deploy de aplicações Flask em ambientes serverless com um simples script Bash. Este projeto utiliza AWS Lambda, AWS CLI e outros serviços AWS para criar uma pipeline eficiente e fácil de usar.

## 🚀 **Recursos do Projeto**
- **Deploy Automatizado**: Envie seu código Python diretamente para o AWS Lambda.
- **Monitoramento**: Visualize logs no AWS CloudWatch.
- **Suporte Futuro**: Integração planejada com triggers do S3.
- **Exposição HTTP**: Integração com o AWS API Gateway para criar endpoints RESTful.

## 🛠️ **Ferramentas Utilizadas**
- **Bash**: Automação e gerenciamento da pipeline.
- **Flask**: Framework para desenvolvimento da aplicação Python.
- **AWS CLI**: Interface para comunicação com os serviços AWS.
- **AWS Lambda** e **API Gateway**: Infraestrutura serverless.
- **WSL (Windows Subsystem for Linux)**: Simulação de ambiente Linux em sistemas Windows.

## 📝 **Execução do Script**
Para realizar o deploy, utilize o seguinte comando:

```bash
./meu_script.sh -p /caminho/para/app.py -f novaLambda -h app.novo_handler
```

- **`-p`**: Caminho do arquivo Python que será zipado.
- **`-f`**: Nome da função Lambda a ser criada ou atualizada.
- **`-h`**: Nome do handler no formato `arquivo.funcao_handler`.

---

## 🖥️ **Guia de Instalação**

### **1. Clone o Repositório**

```bash
git clone https://github.com/usuario/lambdadeployer.git
cd lambdadeployer
```

### **2. Instalar o AWS CLI**
O AWS CLI (Command Line Interface) é essencial para executar comandos diretamente na AWS. Siga os passos abaixo:

#### **2.1. Baixar e Instalar o AWS CLI**

- **No Linux/MacOS:**
  ```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  ```
  Verifique a instalação com:
  ```bash
  aws --version
  ```

- **No Windows:**
  - Baixe o instalador oficial: [AWS CLI para Windows](https://aws.amazon.com/cli/).
  - Execute o arquivo `.msi` e siga as instruções do instalador.
  - Verifique a instalação no **Prompt de Comando** com:
    ```bash
    aws --version
    ```

#### **2.2. Configurar as Credenciais da AWS**
- Acesse o [IAM Management Console](https://console.aws.amazon.com/iam/) e gere uma **Access Key**.
- Configure suas credenciais usando o comando:
  ```bash
  aws configure
  ```
- Preencha as informações:
  - **Access Key ID**: Chave gerada.
  - **Secret Access Key**: Chave secreta.
  - **Região padrão**: Exemplo: `us-east-1`.
  - **Formato de saída**: `json`.

### **3. Instalar o `zip`**
O `zip` é usado para compactar o código Python no script Bash. Siga as instruções para instalação:

- **No Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install zip -y
  ```

- **No Linux (CentOS/Fedora):**
  ```bash
  sudo yum install zip -y
  ```

- **No MacOS:**
  ```bash
  brew install zip
  ```

- **No Windows:**
  O `zip` já vem integrado no sistema ou pode ser instalado via [7-Zip](https://www.7-zip.org/).

---

## 🛠️ **Como Funciona o Script**

O script realiza os seguintes passos:
1. Compacta o código Python em um arquivo ZIP:
   ```bash
   zip -r website.zip app.py
   ```
2. Faz o upload do código para a função Lambda especificada:
   ```bash
   aws lambda update-function-code --function-name myLambda --zip-file fileb://website.zip
   ```
3. Limpa o
