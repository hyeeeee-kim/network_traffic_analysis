import os
import psycopg2
from psycopg2.extras import DictCursor
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
from datetime import datetime
import json

# 로컬 환경에서는 .env를 읽고, Azure에서는 패스.
if os.path.exists('.env'):
    load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24)

# 데이터베이스 연결 함수
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        sslmode='require', #Azure를 위해 반드시 추가
        options='-c timezone=Asia/Seoul' # 스키마 설정
    )
    print('get_db_connection', conn)
    conn.autocommit = True
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/attack-type-analysis')
def attack_type_analysis():
    try:
        # 기본값 설정
        start_date = request.args.get('start_date', '2021-02-01')
        end_date = request.args.get('end_date', '2023-01-10')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute('''SELECT "Attack Type", count(*) as count
                        FROM ntd.traffic_total_info 
                        WHERE timestamp > %s AND timestamp < %s
                        GROUP BY "Attack Type"
                        ORDER BY count DESC''', (start_date, end_date))
        traffic_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('attack_type_analysis.html', traffic_data=traffic_data, start_date=start_date, end_date=end_date)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('attack_type_analysis.html', traffic_data=[], start_date='2021-02-01', end_date='2023-01-10')

@app.route('/packet-analysis')
def packet_analysis():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute('''SELECT "Attack Type", avg("Packet Length") as avg_packet_length
                        FROM ntd.traffic_total_info 
                        GROUP BY "Attack Type"
                        ORDER BY avg_packet_length DESC''')
        packet_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('packet_analysis.html', packet_data=packet_data)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('packet_analysis.html', packet_data=[])

@app.route('/protocol-analysis')
def protocol_analysis():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)
        cur.execute('''SELECT "Attack Type", "protocol", count("protocol") as protocol_count
                        FROM ntd.traffic_total_info 
                        GROUP BY "Attack Type", "protocol"
                        ORDER BY "Attack Type", protocol_count DESC''')
        protocol_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('protocol_analysis.html', protocol_data=protocol_data)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('protocol_analysis.html', protocol_data=[])

if __name__ == '__main__':
    app.run(debug=True)