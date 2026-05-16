import pandas as pd

def clean_race_results(df):
    """netkeibaから取得したDataFrameをクレンジング"""
    # 着順が数字以外の行（除外・取消など）を削除
    df = df[pd.to_numeric(df['着順'], errors='coerce').notnull()].copy()
    df['着順'] = df['着順'].astype(int)
    
    # 馬体重の分割処理
    if '馬体重' in df.columns:
        df['馬体重_num'] = df['馬体重'].str.extract(r'^(\d+)').astype(float)
        df['体重増減'] = df['馬体重'].str.extract(r'\(([-+]?\d+)\)').astype(float)
    
    # 単勝オッズと人気の数値化
    df['単勝'] = pd.to_numeric(df['単勝'], errors='coerce')
    df['人気'] = pd.to_numeric(df['人気'], errors='coerce')
    
    return df
