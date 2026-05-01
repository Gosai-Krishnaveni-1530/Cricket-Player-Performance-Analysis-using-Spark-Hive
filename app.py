from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# ---------- LOAD ----------
def load_csv(path, columns):
    try:
        df = pd.read_csv(path)
        df.columns = columns
        return df
    except:
        return pd.DataFrame(columns=columns)

pig_df = load_csv("output/pig_output.csv",
                  ["Player","Runs","Wickets","Catches"])

hive_df = pd.read_csv("output/hive_output.csv",
                      header=None,
                      names=["Player","Runs","Wickets","Catches"])

spark_df = load_csv("output/spark_output.csv",
                    ["Player","Runs","Wickets","Catches","Score"])


def filter_player(df, name):
    return df[df['Player'].str.lower().str.contains(name.lower(), na=False)]


# ---------- COMMON STYLE ----------
STYLE = """
<style>
body { background:#121212; color:white; font-family:Arial; }
h1 { text-align:center; }
.card {
    background:#1e1e1e;
    padding:20px;
    margin:20px auto;
    width:300px;
    border-radius:10px;
    text-align:center;
    box-shadow:0 0 10px #000;
}
input, button {
    padding:10px;
    margin:5px;
}
a { color:#00ffcc; }
</style>
"""


# ---------- HOME ----------
@app.route('/')
def home():
    return STYLE + """
    <h1>🏏 Big Data Dashboard</h1>
    <div style="text-align:center;">
        <a href="/pig">Pig Dashboard</a><br><br>
        <a href="/hive">Hive Dashboard</a><br><br>
        <a href="/spark">Spark Dashboard</a>
    </div>
    """


# ---------- PIG ----------
@app.route('/pig')
def pig():
    name = request.args.get('name','')

    if name == "":
        return STYLE + """
        <h1>🐷 Pig Dashboard</h1>
        <form style="text-align:center;">
            <input name="name" placeholder="Search player">
            <button>Search</button>
        </form>
        """

    data = filter_player(pig_df, name)

    if data.empty:
        return STYLE + "<h2>No player found</h2>"

    row = data.iloc[0]

    return STYLE + f"""
    <h1>🐷 Pig Dashboard</h1>
    <div class="card">
        <h2>{row['Player']}</h2>
        Runs: {row['Runs']}<br>
        Wickets: {row['Wickets']}<br>
        Catches: {row['Catches']}
    </div>
    """


# ---------- HIVE ----------
@app.route('/hive')
def hive():
    name = request.args.get('name','')

    if name == "":
        return STYLE + """
        <h1>🐝 Hive Dashboard</h1>
        <form style="text-align:center;">
            <input name="name" placeholder="Search player">
            <button>Search</button>
        </form>
        """

    data = filter_player(hive_df, name)

    if data.empty:
        return STYLE + "<h2>No player found</h2>"

    row = data.iloc[0]

    return STYLE + f"""
    <h1>🐝 Hive Dashboard</h1>
    <div class="card">
        <h2>{row['Player']}</h2>
        Runs: {row['Runs']}<br>
        Wickets: {row['Wickets']}<br>
        Catches: {row['Catches']}
    </div>
    """


# ---------- SPARK ----------
@app.route('/spark')
def spark():
    name = request.args.get('name','')

    if name == "":
        return STYLE + """
        <h1>⚡ Spark Dashboard</h1>

        <form style="text-align:center;">
            <input name="name" placeholder="Search player">
            <button>Search</button>
        </form>

        <h2 style="text-align:center;">🏆 Leaderboard</h2>
        """ + spark_df.sort_values("Score", ascending=False).head(5).to_html(index=False)


    data = filter_player(spark_df, name)

    if data.empty:
        return STYLE + "<h2>Player not found</h2>"

    row = data.iloc[0]

    return STYLE + f"""
    <h1>⚡ Spark Dashboard</h1>

    <div class="card">
        <h2>{row['Player']}</h2>
        Runs: {row['Runs']}<br>
        Wickets: {row['Wickets']}<br>
        Catches: {row['Catches']}<br>
        <b>Score: {row['Score']}</b>
    </div>

    <canvas id="chart"></canvas>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{
            labels: ['Runs','Wickets','Catches'],
            datasets: [{{
                label: 'Performance',
                data: [{row['Runs']}, {row['Wickets']}, {row['Catches']}]
            }}]
        }}
    }});
    </script>

    <h2 style="text-align:center;">📊 Compare Players</h2>

    <form action="/compare" style="text-align:center;">
        <input name="p1" placeholder="Player 1">
        <input name="p2" placeholder="Player 2">
        <button>Compare</button>
    </form>
    """


# ---------- COMPARE ----------
@app.route('/compare')
def compare():
    p1 = request.args.get('p1','')
    p2 = request.args.get('p2','')

    d1 = filter_player(spark_df, p1)
    d2 = filter_player(spark_df, p2)

    if d1.empty or d2.empty:
        return STYLE + "<h2>Player not found</h2>"

    r1 = d1.iloc[0]
    r2 = d2.iloc[0]

    return STYLE + f"""
    <h1>Comparison</h1>

    <canvas id="chart"></canvas>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('chart'), {{
        type: 'bar',
        data: {{
            labels: ['Runs','Wickets','Catches'],
            datasets: [
                {{
                    label: '{r1['Player']}',
                    data: [{r1['Runs']}, {r1['Wickets']}, {r1['Catches']}]
                }},
                {{
                    label: '{r2['Player']}',
                    data: [{r2['Runs']}, {r2['Wickets']}, {r2['Catches']}]
                }}
            ]
        }}
    }});
    </script>
    """


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)