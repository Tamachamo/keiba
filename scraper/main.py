import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from data_cleaner import clean_race_results

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def scrape_and_save(race_id: str):
    print(f"Scraping race_id: {race_id}...")
    url = f"https://db.netkeiba.com/race/{race_id}"
    res = requests.get(url)
    res.encoding = "EUC-JP"
    
    try:
        dfs = pd.read_html(res.text)
        if not dfs: return
        
        df = clean_race_results(dfs[0])
        records = []
        
        # racesテーブルへのダミーインサート
        supabase.table('races').upsert({"race_id": race_id}).execute()

        for _, row in df.iterrows():
            record = {
                "race_id": race_id,
                "rank": row.get('着順'),
                "frame_number": row.get('枠番'),
                "horse_number": row.get('馬番'),
                "horse_name": row.get('馬名'),
                "jockey_name": row.get('騎手'),
                "odds": row.get('単勝'),
                "popularity": row.get('人気'),
                "horse_weight": row.get('馬体重_num'),
                "horse_weight_diff": row.get('体重増減')
            }
            records.append({k: v for k, v in record.items() if pd.notna(v)})
            
        if records:
            supabase.table('race_results').upsert(records, on_conflict='race_id,horse_number').execute()
            print(f"✅ Saved {len(records)} horses for race {race_id}")
            
    except Exception as e:
        print(f"❌ Error scraping {race_id}: {e}")

if __name__ == "__main__":
    # テスト用（2024年の適当なレースID）
    test_races = ["202405020111", "202405020112"]
    for rid in test_races:
        scrape_and_save(rid)
        time.sleep(2) # サーバー負荷軽減のため必ずスリープ
