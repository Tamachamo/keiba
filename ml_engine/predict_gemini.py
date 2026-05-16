import google.generativeai as genai
import os
import json
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
model = genai.GenerativeModel('gemini-3.1-flash-lite')

def predict_with_gemini(race_id: str):
    # レースデータの取得
    response = supabase.table('race_results').select('horse_number, horse_name, odds, popularity, horse_weight').eq('race_id', race_id).execute()
    df = pd.DataFrame(response.data)
    if df.empty: return

    race_data_json = df.to_json(orient="records", force_ascii=False)
    
    prompt = f"""
    あなたはプロの競馬アナリストです。以下の出走表データを分析し、各馬が3着以内に入るポテンシャル（期待値スコア）を1〜100の整数で評価してください。
    以下のJSONフォーマットのみで出力してください。Markdownのコードブロック(```json)などは一切含めず、純粋なJSON配列のみを出力してください。
    [ {{"horse_number": 1, "gemini_score": 85}}, {{"horse_number": 2, "gemini_score": 40}} ]
    
    【出走データ】
    {race_data_json}
    """
    
    try:
        res = model.generate_content(prompt)
        result_text = res.text.strip()
        # Markdownのゴミを削除
        if result_text.startswith("```json"):
            result_text = result_text[7:-3]
            
        scores = json.loads(result_text)
        
        # predictionsテーブルを更新
        for score in scores:
            supabase.table('predictions').update({"gemini_score": score["gemini_score"]})\
                .eq("race_id", race_id).eq("horse_number", score["horse_number"]).execute()
                
        print(f"✅ Race {race_id} のGemini推論結果を保存しました。")
    except Exception as e:
        print(f"❌ Gemini予測エラー: {e}")

if __name__ == "__main__":
    predict_with_gemini("202405020111")
