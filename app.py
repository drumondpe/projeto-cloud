from flask import Flask, request, redirect, render_template, url_for
import boto3
import uuid
from datetime import datetime
import os

app = Flask(__name__)

name_ = "jameStack-MyApplicationData"
dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table(name_)

@app.route('/')
def index():
    response = table.scan()
    items = response.get('Items', [])
    for item in items:
        if 'created_at' not in item:
            item['created_at'] = '1970-01-01T00:00:00.000000'  
    items.sort(key=lambda x: x['created_at'], reverse=True)
    return render_template('index.html', posts=items)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    content = request.form['content']    
    post_id = str(uuid.uuid4())    
    created_at = datetime.utcnow().isoformat()
    try:
        response = table.put_item(
           Item={'Id': post_id, 'Title': title, 'Content': content, 'created_at': created_at}
        )
        return redirect('/')
    except Exception as e:
        print(f"Erro ao inserir dados: {str(e)}")
        return redirect('/')
    
@app.route('/delete/<post_id>', methods=['POST'])
def delete(post_id):
    try:
        response = table.delete_item(
            Key={'Id': post_id}
        )
        return redirect('/')
    except Exception as e:
        print(f"Erro ao excluir dados: {str(e)}")
        return redirect('/')
    
@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            response = table.update_item(
                Key={'Id': post_id},
                UpdateExpression="set Title=:t, Content=:c",
                ExpressionAttributeValues={':t': title, ':c': content                },
                ReturnValues="UPDATED_NEW")
            return redirect('/')
        except Exception as e:
            print(f"Erro ao atualizar dados: {str(e)}")
            return redirect('/')
    try:
        response = table.get_item(
            Key={'Id': post_id}
        )
        item = response.get('Item', {})
        return render_template('edit.html', post=item)
    except Exception as e:
        print(f"Erro ao recuperar dados: {str(e)}")
        return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)