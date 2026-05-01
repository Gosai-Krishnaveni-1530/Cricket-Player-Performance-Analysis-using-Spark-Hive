data = LOAD '/app/data/final_cricket_data.csv' USING PigStorage(',')
AS (Player:chararray, Format:chararray, Runs:int, Wkts:int, Catches:int);

filtered = FILTER data BY LOWER(Player) MATCHES '.*$name.*';

STORE filtered INTO '/app/output/pig_output' USING PigStorage(',');