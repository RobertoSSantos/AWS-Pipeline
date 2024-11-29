#!/bin/bash

# Função de exibição de uso
function show_usage() {
    echo "Uso: $0 -p <caminho_do_arquivo> [-f <nome_da_funcao>] [-h <handler>]"
    echo "    -p : Caminho para o arquivo Python a ser zipado (ex: app.py)"
    echo "    -f : Nome da função Lambda (padrão: myLambda)"
    echo "    -h : Handler da função Lambda (padrão: app.lambda_handler)"
    exit 1
}

# Variáveis padrão
FUNCTION_NAME="myLambda"
HANDLER="app.lambda_handler"

# Processa os argumentos
while getopts "p:f:h:" opt; do
    case $opt in
        p) PATH_TO_FILE="$OPTARG" ;;
        f) FUNCTION_NAME="$OPTARG" ;;
        h) HANDLER="$OPTARG" ;;
        *) show_usage ;;
    esac
done

# Verifica se o caminho do arquivo foi fornecido
if [ -z "$PATH_TO_FILE" ]; then
    echo "Erro: O caminho para o arquivo deve ser especificado."
    show_usage
fi

# Verifica se o arquivo existe
if [ ! -f "$PATH_TO_FILE" ]; then
    echo "Erro: Arquivo não encontrado no caminho especificado: $PATH_TO_FILE"
    exit 1
fi

# Verifica se a AWS CLI está instalada
if ! command -v aws &> /dev/null; then
    echo "Erro: AWS CLI não está instalada."
    exit 1
fi

# Compacta o código Python em um arquivo ZIP
ZIP_FILE="website.zip"
echo "Compactando o código Python em $ZIP_FILE..."
zip -r $ZIP_FILE "$PATH_TO_FILE"

# Atualiza a função Lambda com o código compactado
echo "Atualizando a função Lambda \"$FUNCTION_NAME\"..."
aws lambda update-function-code --function-name "$FUNCTION_NAME" --zip-file "fileb://$ZIP_FILE"

# Limpeza do arquivo zipado temporário
echo "Limpando arquivos temporários..."
rm $ZIP_FILE

echo "Atualização da função Lambda concluída com sucesso!"
