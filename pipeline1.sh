#!/bin/bash

# Verifica se a AWS CLI está instalada
if ! command -v aws &> /dev/null; then
    echo "AWS CLI não está instalada."
    exit 1
fi
# Configura variáveis para a função Lambda e o arquivo de código Python
FUNCTION_NAME="myLambda"
ZIP_FILE="website.zip" # Arquivo zip do site Python
HANDLER="app.lambda_handler" # Ponto de entrada do Python (ex: 'app.lambda_handler')

# 1. Compacta o código Python em um arquivo ZIP
echo "Compactando codigo Python..."
zip -r $ZIP_FILE app.py

# 2. Faz o upload do código para a função Lambda
echo "Atualizando a função Lambda..."
aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP_FILE


# Limpeza do arquivo zipado temporário
rm $ZIP_FILE