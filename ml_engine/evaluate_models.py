import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def evaluate_predictions():
    pred_res = supabase.table('predictions').select('*').execute()
    actual_res = supabase.table('race_results').select('race_id, horse_number, rank, odds').execute()
    
    df_pred = pd.DataFrame(pred_res.data)
    df_actual = pd.DataFrame(actual_res.data)
    
    if df_pred.empty or df_actual.empty:
        print("評価するデータがありません。")
        return
        
    df = pd.merge(df_pred, df_actual, on=['race_id', 'horse_number'])
    
    # LGBM勝率1位を買い続けた場合
    print("--- LightGBM シミュレーション ---")
    top_lgbm_picks = df.loc[df.groupby('race_id')['lgbm_win_prob'].idxmax()]
    lgbm_hits = top_lgbm_picks[top_lgbm_picks['rank'] == 1]
    
    total_bets = len(top_lgbm_picks) * 100
    total_return = (lgbm_hits['odds'] * 100).sum()
    
    print(f"対象レース数: {len(top_lgbm_picks)}")
    print(f"的中率: {len(lgbm_hits) / len(top_lgbm_picks) * 100:.1f}%")
    print(f"回収率: {(total_return / total_bets * 100) if total_bets > 0 else 0:.1f}%\n")

if __name__ == "__main__":
    evaluate_predictions()
