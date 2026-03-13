# Optional Dashboard

This is an **optional** enhancement for visualizing the MapReduce output.
It reads the exported `alerts_latest.tsv` from the server reports directory.

## Setup
```
cd dashboard
python3 -m pip install -r requirements.txt
```

## Run
```
export REPORT_DIR=../server/reports
python3 app.py
```

Open http://localhost:5001

If you don't want to use a dashboard, you can skip this folder entirely.
