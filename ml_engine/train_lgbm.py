import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def train_model():
    # 実際の運用ではLIMITやページネーションで全データを取得します
    response = supabase.table('race_results').select('*').execute()
    df = pd.DataFrame(response.data)
    
    if df.empty:
        print("データがありません。先にスクレイピングを実行してください。")
        return
        
    # 目的変数：3着以内か
    df['is_top_3'] = df['rank'].apply(lambda x: 1 if x <= 3 else 0)
    features = ['frame_number', 'horse_number', 'odds', 'popularity', 'horse_weight', 'horse_weight_diff']
    df = df.dropna(subset=features)
    
    X = df[features]
    y = df['is_top_3']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)
    
    params = {'objective': 'binary', 'metric': 'auc', 'verbosity': -1}
    
    os.makedirs('models', exist_ok=True)
    model = lgb.train(params, lgb_train, valid_sets=[lgb_eval], num_boost_round=100)
    model.save_model('models/lightgbm_model.txt')
    print("✅ Model trained and saved.")

if __name__ == "__main__":
    train_model()
