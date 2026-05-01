# Cricket Player Performance Analysis using Big Data Technologies

A comprehensive big data analytics project for cricket player performance analysis using Hadoop ecosystem tools (Spark, Hive, and Pig), with Docker-based deployment and interactive Flask dashboards.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
- [Dashboards](#dashboards)
- [Scripts](#scripts)
- [Output Files](#output-files)

---

## 📊 Project Overview

This project analyzes cricket player performance data using multiple big data processing frameworks:

- **Apache Pig**: For ETL and data transformation
- **Apache Hive**: For SQL-based data warehousing
- **Apache Spark**: For in-memory data processing
- **Flask**: For interactive web dashboards

The goal is to aggregate and analyze cricket player statistics including runs, wickets, and catches.

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Input Data    │
│ (CSV Files)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌───────┐ ┌───────┐ ┌────────┐
│  Pig  │ │ Spark │ │  Hive  │
└───┬───┘ └───┬───┘ └───┬────┘
    │         │          │
    └────┬────┴──────────┘
         ▼
┌─────────────────┐
│  Output Files   │
│ (CSV Results)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Web      │
│  Dashboards    │
└───────────────┘
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.10 | Programming language |
| Flask | Web framework |
| Pandas | Data manipulation |
| Apache Spark | Big data processing |
| Apache Hive | Data warehousing |
| Apache Pig | ETL scripting |
| Docker | Containerization |

---

## 📁 Project Structure

```
c:/bigdata-project/
├── app.py                     # Flask web application with dashboards
├── generate_pig.py            # Python script to generate Pig output
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container configuration
├── README.md                  # This file
├── derby.log                  # Derby database log
│
├── data/
│   └── final_cricket_data.csv # Input cricket player data
│
├── output/
│   ├── pig_output.csv         # Pig processing output
│   ├── hive_output.csv      # Hive processing output
│   └── spark_output.csv    # Spark processing output
│
├── scripts/
│   ├── pig_script.pig       # Apache Pig script
│   ├── hive_script.sql      # Apache Hive script
│   └── spark_script.py     # Apache Spark script
│
├── metastore_db/            # Hive Metastore database
├── output/hive_output/     # Hive output directory
├── output/spark_output/     # Spark output directory
└── scripts/               # Processing scripts directory
```

---

## 📈 Data Model

### Input Data Format (`data/final_cricket_data.csv`)

| Column | Type | Description |
|--------|------|-------------|
| Player | String | Player name |
| Format | String | Cricket format (Test/ODI/T20) |
| Runs_x | Integer | Runs scored |
| Wkts | Integer | Wickets taken |
| Catches | Integer | Catches fielded |

### Output Data Format

| Column | Type | Description |
|--------|------|-------------|
| Player | String | Player name |
| Runs | Integer | Total runs |
| Wickets | Integer | Total wickets |
| Catches | Integer | Total catches |
| Score | Integer | Performance score (Spark only) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd c:/bigdata-project
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Or use Docker:
```bash
docker build -t cricket-analytics .
docker run -p 5000:5000 cricket-analytics
```

---

## 🖥️ Running the Project

### Running the Flask Dashboard

```bash
python app.py
```

The dashboard will be available at: `http://localhost:5000`

### Running Individual Processing Scripts

#### Using Pig:
```bash
pig scripts/pig_script.pig
```

#### Using Hive:
```bash
hive scripts/hive_script.sql
```

#### Using Spark:
```bash
spark-submit scripts/spark_script.py
```

---

## 📱 Dashboards

The project provides three interactive dashboards:

### 1. Pig Dashboard (`/pig`)
- Search cricket players using Pig-processed data
- View runs, wickets, and catches

### 2. Hive Dashboard (`/hive`)
- Search cricket players using Hive-processed data
- View aggregated statistics

### 3. Spark Dashboard (`/spark`)
- Full-featured dashboard with:
  - Player search
  - Leaderboard (Top 5 players by score)
  - Performance visualization (Chart.js)
  - Player comparison tool

### Comparison Feature (`/compare`)
- Compare two players side-by-side
- Visual bar chart comparison

---

## 📜 Scripts

### Pig Script (`scripts/pig_script.pig`)
```pig
data = LOAD '/app/data/final_cricket_data.csv' USING PigStorage(',')
AS (Player:chararray, Format:chararray, Runs:int, Wkts:int, Catches:int);

filtered = FILTER data BY LOWER(Player) MATCHES '.*$name.*';

STORE filtered INTO '/app/output/pig_output' USING PigStorage(',');
```

### Hive Script (`scripts/hive_script.sql`)
```sql
SELECT Player,
SUM(Runs_x) AS Runs,
SUM(Wkts) AS Wickets,
SUM(Catches) AS Catches
FROM cricket_data
WHERE LOWER(Player) LIKE '%${name}%'
GROUP BY Player;
```

### Spark Script (`scripts/spark_script.py`)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.getOrCreate()

name = input("Enter player name: ").lower()

df = spark.read.csv("/app/data/final_cricket_data.csv", header=True)

result = df.filter(col("Player").rlike(name)) \
    .groupBy("Player") \
    .sum("Runs_x", "Wkts", "Catches")

result.show()
```

---

## 📤 Output Files

| File | Description |
|------|-------------|
| `output/pig_output.csv` | Pig processed player data |
| `output/hive_output.csv` | Hive aggregated player data |
| `output/spark_output.csv` | Spark processed data with scores |

---

## 🔧 Configuration

### Port Configuration
- Flask app runs on port 5000 by default
- Can be changed in `app.py`:
```python
app.run(host="0.0.0.0", port=5000)
```

### Data Paths
- Input data path: `data/final_cricket_data.csv`
- Output directory: `output/`

---

## 📝 License

This project is for educational purposes and demonstrates big data analytics workflows.

---

## 👥 Author

Big Data Analytics Project - Cricket Player Performance Analysis

## 🙏 Acknowledgments

- Apache Hadoop Ecosystem
- Apache Spark
- Apache Hive
- Apache Pig
- Flask Documentation
- Pandas Documentation
