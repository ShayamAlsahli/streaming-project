# Streaming Analytics Project

## 📖 Project Description
This project is a **real-time engagement analytics system** for content interactions, using **PostgreSQL, Kafka, Debezium, Redis, Python, ClickHouse, and Dashboard tools (Streamlit/Grafana)**.  

The project goals are:
- Stream events from PostgreSQL to Kafka using Debezium.
- Store the latest events in Redis as a cache for fast access.
- Perform data aggregation (e.g., counts per event type per content) every few seconds.
- Send aggregated data to a columnar database like ClickHouse for advanced analytics and reporting.
- Display real-time dashboards using Streamlit or Grafana.

---

## 🗂️ Project Structure

streaming-project/
│
├── docker-compose.yml # Defines all services: Postgres, Kafka, Zookeeper, Redis, ClickHouse
├── connector.json # Debezium Connector configuration for PostgreSQL → Kafka
├── main_streamer.py # Python script: reads events from Postgres → Redis
├── aggregation.py # Python script: reads from Redis → performs Aggregation
├── clickhouse_sink.py # Python script: sends aggregated data from Redis → ClickHouse
├── api.py # FastAPI: API to expose aggregated metrics
├── dashboard.py # Streamlit: Dashboard to visualize content interactions
└── README.md # This file

yaml
Copy code

---

## ⚙️ Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop)
- Python libraries:

```bash
pip install psycopg2 redis clickhouse-connect fastapi uvicorn streamlit
🐳 Running the Project with Docker
Start all services:

bash
Copy code
docker compose up -d
Check running containers:

bash
Copy code
docker compose ps
Main services:

Postgres (main database)

Kafka + Zookeeper (streaming system)

Kafka Connect (Debezium Connector)

Redis (cache for latest events)

ClickHouse (columnar database for analytics)

📝 Setting up PostgreSQL & Debezium
Create the database and table:

sql
Copy code
-- Connect to PostgreSQL
CREATE DATABASE streaming_db;

\c streaming_db

CREATE TABLE engagement_events (
    id SERIAL PRIMARY KEY,
    content_id UUID,
    user_id UUID,
    event_type VARCHAR(10),
    event_ts TIMESTAMP,
    device VARCHAR(50)
);
Configure Debezium Connector (connector.json):

json
Copy code
{
  "name": "postgres-engagement-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "admin",
    "database.password": "admin",
    "database.dbname": "streaming_db",
    "database.server.name": "streaming",
    "topic.prefix": "streaming",
    "table.include.list": "public.engagement_events",
    "plugin.name": "pgoutput",
    "slot.name": "engagement_slot",
    "publication.autocreate.mode": "filtered"
  }
}
Enable the connector:

bash
Copy code
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @connector.json
🔄 Python Streamer (Postgres → Redis)
File: main_streamer.py

Reads new events from Postgres every 5 seconds.

Pushes them to Redis as latest_events.

Run:

bash
Copy code
python main_streamer.py
📊 Aggregation
File: aggregation.py

Computes count per event type per content from Redis every 5 seconds.

Aggregated results can be stored in Redis or later sent to ClickHouse.

Run:

bash
Copy code
python aggregation.py
🏢 ClickHouse Sink
File: clickhouse_sink.py

Sends aggregated data from Redis to ClickHouse every 5 seconds.

Allows large-scale analytics and reporting.

Run:

bash
Copy code
python clickhouse_sink.py
🖥️ Dashboard
1. Streamlit
File: dashboard.py

Reads data from ClickHouse and displays tables & charts.

Run:

bash
Copy code
streamlit run dashboard.py
2. Grafana
Add ClickHouse Data Source

URL: http://localhost:8123

Database: streaming_analytics

Create dashboards according to your requirements.

🔧 FastAPI API
File: api.py

Exposes aggregated metrics via HTTP from Redis.

Run:

bash
Copy code
uvicorn api:app --reload
Access metrics:

bash
Copy code
http://localhost:8000/metrics
⏱️ Tips for Running
Start Docker first.

Run main_streamer.py → then aggregation.py.

Finally, run clickhouse_sink.py and the Dashboard.

Make sure all services are using the correct host (localhost or Docker service name).

📈 Project Output
Real-time streaming from Postgres → Kafka → Redis

Automatic aggregation on the fly

Data stored in ClickHouse for analytics

Real-time Dashboard with Streamlit or Grafana

Useful Links
Kafka

Debezium

Redis

ClickHouse

Streamlit

Grafana

