import pandas as pd, csv, os

path = "data/emotion_journal.csv"

if not os.path.exists(path):
    print("❌ No CSV file found!")
else:
    try:
        df = pd.read_csv(path, on_bad_lines='skip')
        if len(df.columns) < 4:
            df.columns = ['timestamp', 'emotion', 'confidence', 'text'][:len(df.columns)]
        elif len(df.columns) > 4:
            df = df.iloc[:, :4]
            df.columns = ['timestamp', 'emotion', 'confidence', 'text']
        df.to_csv(path, index=False, quoting=csv.QUOTE_ALL)
        print("✅ Fixed CSV successfully!")
    except Exception as e:
        print("❌ Error:", e)

