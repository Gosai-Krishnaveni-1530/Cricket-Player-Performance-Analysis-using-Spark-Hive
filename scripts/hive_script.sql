SELECT Player,
SUM(Runs_x) AS Runs,
SUM(Wkts) AS Wickets,
SUM(Catches) AS Catches
FROM cricket_data
WHERE LOWER(Player) LIKE '%${name}%'
GROUP BY Player;