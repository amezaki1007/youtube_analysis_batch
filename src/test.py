import os
from datetime import datetime

import mysql.connector

# MySQLデータベース接続設定
db_config = {
    'host': '172.29.80.1',      # ホスト名
    'user': 'amezaki',       # ユーザー名
    'password': 'blackbird',   # パスワード
    'database': 'youtube_analysis'  # データベース名
}

def connect_to_database():
    """データベースへの接続を確立する"""
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQLデータベースに接続しました")
        return connection
    except mysql.connector.Error as err:
        print(f"エラー: {err}")
        return None

def create_test_table(connection):
    """testテーブルが存在しない場合は作成する"""
    try:
        cursor = connection.cursor()
        
        # testテーブルの作成クエリ
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            video_id VARCHAR(20) NOT NULL,
            title VARCHAR(255) NOT NULL,
            channel_name VARCHAR(100) NOT NULL,
            view_count INT DEFAULT 0,
            like_count INT DEFAULT 0,
            comment_count INT DEFAULT 0,
            upload_date DATE,
            category VARCHAR(50),
            duration INT,  # 秒単位での動画の長さ
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("testテーブルが作成されました（または既に存在しています）")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"テーブル作成エラー: {err}")

def insert_sample_data(connection):
    """サンプルデータをtestテーブルに挿入する"""
    try:
        cursor = connection.cursor()
        
        # サンプルデータ
        sample_data = [
            ('dQw4w9WgXcQ', 'Rick Astley - Never Gonna Give You Up',   'Rick Astley', 12345678, 9876543,  543210,   '2009-10-25', 'Music', 213),
            ('jNQXAC9IVRw', 'Me at the zoo',                           'jawed',       24814567, 12345678, 7654321,  '2005-04-23', 'People & Blogs', 19),
            ('9bZkp7q19f0', 'PSY - GANGNAM STYLE',                     'officialpsy', 47531567, 24680135, 12345678, '2012-07-15', 'Music', 253),
            ('kJQP7kiw5Fk', 'Luis Fonsi - Despacito ft. Daddy Yankee', 'Luis Fonsi',  78965432, 48651324, 7456123,  '2017-01-12', 'Music', 282),
            ('hGBQZO6wHuM', '初音ミク「マジカルミライ」',                'SEGA',        78945612, 154236,   25463,    '2023-05-20', 'Entertainment', 203)
        ]
        
        # 挿入クエリ
        insert_query = """
        INSERT INTO test 
        (video_id, title, channel_name, view_count, like_count, comment_count, upload_date, category, duration)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # データを挿入
        cursor.executemany(insert_query, sample_data)
        connection.commit()
        print(f"{cursor.rowcount}件のデータが正常に挿入されました")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"データ挿入エラー: {err}")

def fetch_data(connection):
    """挿入したデータを確認するためにデータを取得する"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM test LIMIT 5")
        results = cursor.fetchall()
        
        print("\n挿入されたデータの確認:")
        for row in results:
            print(f"ID: {row['id']}, タイトル: {row['title']}, チャンネル: {row['channel_name']}, 再生回数: {row['view_count']}")
        
        cursor.close()
    except mysql.connector.Error as err:
        print(f"データ取得エラー: {err}")

def main():
    """メイン関数"""
    # データベースに接続
    connection = connect_to_database()
    
    if connection:
        # testテーブルを作成
        create_test_table(connection)
        
        # サンプルデータを挿入
        insert_sample_data(connection)
        
        # 挿入したデータを確認
        fetch_data(connection)
        
        # 接続を閉じる
        connection.close()
        print("\nデータベース接続を閉じました")

if __name__ == "__main__":
    main()
