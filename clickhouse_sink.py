import time
import redis
from clickhouse_connect import Client

# ---------- Redis Connection ----------
r = redis.Redis(host='redis', port=6379, decode_responses=True)

# ---------- ClickHouse Connection ----------
# تعديل بيانات الاتصال حسب الإعدادات الخاصة بك
client = Client(
    host='clickhouse',       # Docker service name
    port=8123,               # HTTP port
    username='default',
    password='',
    database='streaming_analytics'
)

# إنشاء جدول في ClickHouse إذا لم يكن موجوداً
client.command("""
CREATE TABLE IF NOT EXISTS engagement_aggregation (
    content_id String,
    play UInt32,
    pause UInt32,
    finish UInt32,
    click UInt32,
    updated_at DateTime
) ENGINE = MergeTree()
ORDER BY content_id
""")

print("ClickHouse sink started (updates every 5 seconds)...")

while True:
    try:
        # قراءة البيانات المجمعة من Redis
        metrics = r.hgetall("aggregated_metrics")  # content_id -> JSON string
        rows = []
        
        for content_id, json_data in metrics.items():
            data = eval(json_data)  # تحويل من str إلى dict
            row = {
                'content_id': content_id,
                'play': data.get('PLAY', 0),
                'pause': data.get('PAUSE', 0),
                'finish': data.get('FINISH', 0),
                'click': data.get('CLICK', 0),
                'updated_at': int(time.time())
            }
            rows.append(row)
        
        if rows:
            client.insert('engagement_aggregation', rows)
            print(f"Inserted {len(rows)} rows into ClickHouse")
        else:
            print("No new data to insert")

    except Exception as e:
        print("Error:", e)
    
    time.sleep(5)
