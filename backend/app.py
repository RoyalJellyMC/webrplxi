from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Ganti dengan user MySQL Anda
        password='',  # Ganti dengan password MySQL Anda
        database='db_jurusan'  # Ganti dengan nama database Anda
    )

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM jurusan')
        rows = cursor.fetchall()
        return jsonify(rows)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = 'INSERT INTO jurusan (nama, deskripsi) VALUES (%s, %s)'
        cursor.execute(sql, (data['nama'], data['deskripsi']))
        conn.commit()
        return jsonify({'message': 'Data berhasil ditambahkan'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
