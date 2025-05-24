import os
from datetime import datetime, date
from dataclasses import fields, is_dataclass
from typing import Any, Dict, List, Optional, TypeVar, Type, Union

import mysql.connector

from video_entity import VideoEntity
from viewcount_entity import ViewcountEntity


# MySQLデータベース接続設定
db_config = {
    'host': os.getenv("MYSQL_HOST"), # ホスト名
    'user': os.getenv("MYSQL_USER"), # ユーザー名
    'password': os.getenv("MYSQL_PASSWORD"), # パスワード
    'database': os.getenv("MYSQL_DB") # データベース名
}

T = TypeVar('T')  # dataclassのジェネリック型

def connect_to_database():
    """データベースへの接続を確立する"""
    try:
        connection = mysql.connector.connect(**db_config)
        print("MySQLデータベースに接続しました")
        return connection
    except mysql.connector.Error as err:
        print(f"エラー: {err}")
        return None

class MySQLDataclassInserter:
  """
  dataclassのインスタンスをMySQLに挿入するための汎用クラス
  """  
  def __init__(self, connection: mysql.connector.MySQLConnection=None):
    """
    MySQL接続を使用して初期化
    
    Args:
        connection: MySQL接続オブジェクト
    """
    if connection:
      self.connection = connection
    else:
      self.connection = connect_to_database()
  
  def _format_value_for_sql(self, value: Any) -> Any:
    """
    値をSQL用に適切なフォーマットに変換
    
    Args:
        value: フォーマットする値
    
    Returns:
        SQL用にフォーマットされた値
    """
    if value is None:
        return None
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, bool):
        return int(value)
    return value
  
  def _get_table_name(self, dataclass_type: Type[T]) -> str:
    """
    dataclassからテーブル名を取得（デフォルトではクラス名をスネークケースに変換）
    
    Args:
        dataclass_type: dataclassの型
    
    Returns:
        テーブル名
    """
    # クラス名をスネークケースに変換（例: VideoEntity -> video_entity）
    class_name = dataclass_type.__name__
    table_name = ''.join(['_' + c.lower() if c.isupper() else c for c in class_name]).lstrip('_')
    
    # dataclassに__table_name__属性が定義されている場合はそれを使用
    return getattr(dataclass_type, '__table_name__', table_name)
  
  def _extract_values(self, instance: T) -> Dict[str, Any]:
    """
    dataclassインスタンスからフィールド名と値のマッピングを抽出
    
    Args:
        instance: dataclassインスタンス
    
    Returns:
        フィールド名と値のマッピング
    """
    result = {}
    for field in fields(instance):
        value = getattr(instance, field.name)
        result[field.name] = self._format_value_for_sql(value)
    return result
  
  def insert(self, instance: T, table_name: Optional[str] = None) -> int:
    """
    dataclassインスタンスをMySQLテーブルに挿入
    
    Args:
        instance: 挿入するdataclassインスタンス
        table_name: 使用するテーブル名（指定がなければクラス名から自動生成）
    
    Returns:
        挿入された行のID（auto_incrementの場合）またはaffected rowsの数
        
    Raises:
        ValueError: 引数がdataclassインスタンスでない場合
    """
    if not is_dataclass(instance):
        raise ValueError("引数はdataclassのインスタンスである必要があります")
    
    # テーブル名を取得
    if table_name is None:
        table_name = self._get_table_name(type(instance))
    
    # フィールド値を抽出
    values_dict = self._extract_values(instance)
    
    # SQLクエリ構築
    columns = list(values_dict.keys())
    placeholders = ["%s"] * len(columns)
    
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
    
    # クエリ実行
    cursor = self.connection.cursor()
    try:
        cursor.execute(query, list(values_dict.values()))
        self.connection.commit()
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        self.connection.rollback()
        raise e
    finally:
        cursor.close()
  
  def insert_many(self, instances: List[T], table_name: Optional[str] = None) -> int:
    """
    複数のdataclassインスタンスをMySQLテーブルに一括挿入
    
    Args:
        instances: 挿入するdataclassインスタンスのリスト
        table_name: 使用するテーブル名（指定がなければ最初のインスタンスのクラス名から自動生成）
        
    Returns:
        挿入された行数
        
    Raises:
        ValueError: リストが空または要素がdataclassインスタンスでない場合
    """
    if not instances:
        raise ValueError("インスタンスのリストが空です")
    
    # すべての要素が同じdataclass型かチェック
    first_instance = instances[0]
    if not is_dataclass(first_instance):
        raise ValueError("リストの要素はdataclassのインスタンスである必要があります")
    
    instance_type = type(first_instance)
    for instance in instances:
        if not isinstance(instance, instance_type):
            raise ValueError("すべてのインスタンスは同じdataclass型である必要があります")
    
    # テーブル名を取得
    if table_name is None:
        table_name = self._get_table_name(instance_type)
    
    # 最初のインスタンスからカラム情報を取得
    first_values = self._extract_values(first_instance)
    columns = list(first_values.keys())
    
    # SQLクエリ構築
    placeholders = ["%s"] * len(columns)
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
    
    # すべてのインスタンスから値を抽出
    values_list = []
    for instance in instances:
        values_dict = self._extract_values(instance)
        values_list.append([values_dict[col] for col in columns])
    
    # クエリ実行
    cursor = self.connection.cursor()
    try:
        cursor.executemany(query, values_list)
        self.connection.commit()
        return cursor.rowcount
    except Exception as e:
        self.connection.rollback()
        raise e
    finally:
        cursor.close()

  def filter_videos(self, instances: List[T]) -> List[T]:
    """
    hidden テーブルに存在しない video_id のみを返すフィルタ関数

    Args:
        instances: dataclass インスタンスのリスト（例: Videoのリスト）

    Returns:
        hidden テーブルに存在しない video_id を持つインスタンスのリスト
    """
    if not instances:
        return []

    # video_id を収集
    video_ids = [getattr(instance, "video_id", None) for instance in instances]
    video_ids = [vid for vid in video_ids if vid is not None]

    if not video_ids:
        return instances

    # SQL で hidden テーブルに存在する video_id を取得
    format_strings = ','.join(['%s'] * len(video_ids))
    query = f"SELECT video_id FROM hidden WHERE video_id IN ({format_strings})"

    cursor = self.connection.cursor()
    try:
        cursor.execute(query, video_ids)
        hidden_ids = set(row[0] for row in cursor.fetchall())
    finally:
        cursor.close()

    # hidden に存在しない video_id を持つインスタンスのみ返す
    return [instance for instance in instances if getattr(instance, "video_id", None) not in hidden_ids]
     


def insert_video_entity(video: VideoEntity, connection: mysql.connector.MySQLConnection = None, table_name = None) -> int:
  """
  VideoEntityをMySQLに挿入する関数例
  
  Args:
      video: 挿入するVideoEntityインスタンス
      connection: MySQL接続オブジェクト
  """
  if connection is None:
    connection = connect_to_database()
  inserter = MySQLDataclassInserter(connection)
  videos_should_be_inserted = inserter.filter_videos([video])
  if videos_should_be_inserted:
    try:
      res = inserter.insert(video, table_name=table_name)
      return res
    except Exception as e:
      print("データ挿入エラー:", e)
  else:
    print(f"非表示リストにあるため挿入は行われませんでした: id={video.video_id}, title={video.title}")

def insert_video_entity_many(videos: list[VideoEntity], connection: mysql.connector.MySQLConnection = None, table_name = None) -> int:
  """
  VideoEntityをMySQLに挿入する(リスト)
  
  Args:
      videos: 挿入するVideoEntityインスタンスリスト
      connection: MySQL接続オブジェクト
      
  Returns:
      挿入された行数
  """
  if connection is None:
    connection = connect_to_database()
  inserter = MySQLDataclassInserter(connection)
  videos_should_be_inserted = inserter.filter_videos(videos)
  try:
    inserter.insert_many(videos_should_be_inserted, table_name=table_name)
  except Exception:
    for video in videos_should_be_inserted:
       insert_video_entity(video, connection, table_name=table_name)

def insert_viewcount_entity(viewcount: ViewcountEntity, connection: mysql.connector.MySQLConnection = None, table_name = None) -> int:
  """
  ViewcountEntityをMySQLに挿入する関数
  """
  if connection is None:
    connection = connect_to_database()
  inserter = MySQLDataclassInserter(connection)
  try:
    res = inserter.insert(viewcount, table_name=table_name)
    return res
  except Exception as e:
    print("データ挿入エラー:", e)

def insert_viewcount_entity_many(viewcounts: list[ViewcountEntity], connection: mysql.connector.MySQLConnection = None, table_name = None) -> int:
  """
  ViewcountEntityをMySQLに挿入する(リスト)
  """
  if connection is None:
    connection = connect_to_database()
  inserter = MySQLDataclassInserter(connection)
  try:
    inserter.insert_many(viewcounts, table_name=table_name)
  except Exception as e:
    print("データリスト挿入エラー:", e)
    for viewcount in viewcounts:
       insert_viewcount_entity(viewcount, connection, table_name=table_name)
