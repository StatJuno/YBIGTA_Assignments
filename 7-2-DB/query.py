import pymysql

# 데이터베이스 연결 정보
host = 'localhost'
port = 3310
user = 'root'
password = 'test1234'
database = 'ybigta'

# 데이터베이스에 연결
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # INSERT 쿼리 예제
        insert_query = """
        INSERT INTO student (sid, name, academic_warning_count, expected_graduation_date)
        VALUES (%s, %s, %s, %s)
        """
        insert_values = ('2017122054', 'Juno', '0', '2024-02-28')
        
        cursor.execute(insert_query, insert_values)
        connection.commit()
        print("Data inserted successfully")

        # SELECT 쿼리 예제
        select_query = "SELECT * FROM student"
        cursor.execute(select_query)
        result = cursor.fetchall()
        
        for row in result:
            print(row)

finally:
    connection.close()