from flask import Flask, request, redirect, render_template, url_for
import boto3
import uuid
from datetime import datetime
import os

app = Flask(__name__)

# Configurar o cliente DynamoDB
table_name = "jameStack-MyApplicationData"
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table(table_name)

@app.route('/')
def index():
    # Recuperar todos os posts da tabela DynamoDB
    response = table.scan()
    items = response.get('Items', [])

    # Verificar se cada item tem o campo 'created_at' e ordená-los pela data de criação, do mais recente para o mais antigo
    for item in items:
        if 'created_at' not in item:
            item['created_at'] = '1970-01-01T00:00:00.000000'  # Data default para itens sem o campo
    items.sort(key=lambda x: x['created_at'], reverse=True)

    # Renderizar os posts em uma página HTML
    return render_template('index.html', posts=items)

@app.route('/post', methods=['POST'])
def post():
    # Capturar dados do formulário
    title = request.form['title']
    content = request.form['content']
    
    # Gerar um UUID único para cada nova entrada
    post_id = str(uuid.uuid4())
    
    # Obter a data e hora atuais
    created_at = datetime.utcnow().isoformat()

    # Inserir os dados na tabela DynamoDB
    try:
        response = table.put_item(
           Item={
                'Id': post_id,
                'Title': title,
                'Content': content,
                'created_at': created_at
            }
        )
        return redirect('/')
    except Exception as e:
        print(f"Erro ao inserir dados: {str(e)}")
        return redirect('/')

@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if request.method == 'POST':
        # Capturar dados do formulário
        title = request.form['title']
        content = request.form['content']

        # Atualizar os dados na tabela DynamoDB
        try:
            response = table.update_item(
                Key={
                    'Id': post_id
                },
                UpdateExpression="set Title=:t, Content=:c",
                ExpressionAttributeValues={
                    ':t': title,
                    ':c': content
                },
                ReturnValues="UPDATED_NEW"
            )
            return redirect('/')
        except Exception as e:
            print(f"Erro ao atualizar dados: {str(e)}")
            return redirect('/')

    # Recuperar o post atual
    try:
        response = table.get_item(
            Key={
                'Id': post_id
            }
        )
        item = response.get('Item', {})
        return render_template('edit.html', post=item)
    except Exception as e:
        print(f"Erro ao recuperar dados: {str(e)}")
        return redirect('/')

@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    # Excluir os dados na tabela DynamoDB
    try:
        response = table.delete_item(
            Key={
                'Id': post_id
            }
        )
        return redirect('/')
    except Exception as e:
        print(f"Erro ao excluir dados: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)