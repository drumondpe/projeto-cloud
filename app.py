from flask import Flask, request, redirect, render_template, url_for
import boto3
import uuid
from datetime import datetime
import os

app = Flask(__name__)

# Configuração do cliente DynamoDB
table_name = "jameStack-UserManagement"
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table(table_name)

@app.route('/')
def index():
    response = table.scan()
    users = response.get('Items', [])
    users.sort(key=lambda x: x['created_at'], reverse=True)
    return render_template('index.html', users=users)

@app.route("/health")
def health_check():
    return "OK"

@app.route('/user', methods=['POST'])
def create_user():
    name = request.form['name']
    email = request.form['email']
    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    try:
        table.put_item(
           Item={
                'Id': user_id,
                'Name': name,
                'Email': email,
                'created_at': created_at
            }
        )
        return redirect('/')
    except Exception as e:
        return f"Erro ao inserir dados: {str(e)}", 500

@app.route('/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        try:
            table.update_item(
                Key={'Id': user_id},
                UpdateExpression="set Name=:n, Email=:e",
                ExpressionAttributeValues={':n': name, ':e': email},
                ReturnValues="UPDATED_NEW"
            )
            return redirect('/')
        except Exception as e:
            return f"Erro ao atualizar dados: {str(e)}", 500
    else:
        response = table.get_item(Key={'Id': user_id})
        user = response.get('Item', {})
        return render_template('edit.html', user=user)

@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        table.delete_item(Key={'Id': user_id})
        return redirect('/')
    except Exception as e:
        return f"Erro ao excluir dados: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
