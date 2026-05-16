import pandas as pd
import lightgbm as lgb
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def predict_and_save(race_id: str):
    response = supabase.table('race_results').select('*').eq('race_id', race_id).execute()
    df = pd.DataFrame(response.data)
    
    if df.empty: return

    features = ['frame_number', 'horse_number', 'odds', 'popularity', 'horse_weight', 'horse_weight_diff']
    df[features] = df[features].fillna(0)
    X_pred = df[features]
    
    if not os.path.exists('models/lightgbm_model.txt'):
        print("モデルファイルがありません。先に学習を実行してください。")
        return

    model = lgb.Booster(model_file='models/lightgbm_model.txt')
    predictions = model.predict(X_pred)
    df['lgbm_win_prob'] = predictions
    
    records = []
    for _, row in df.iterrows():
        records.append({
            "race_id": row['race_id'],
            "horse_number": int(row['horse_number']),
            "horse_name": row['horse_name'],
            "lgbm_win_prob": float(row['lgbm_win_prob']),
        })
        
    supabase.table('predictions').upsert(records, on_conflict='race_id,horse_number').execute()
    print(f"✅ Race {race_id} のLightGBM推論結果を保存しました。")

if __name__ == "__main__":
    predict_and_save("202405020111")
