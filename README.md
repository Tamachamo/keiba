# 🎯 AI競馬予想システム - LightGBM × Gemini ハイブリッド

競馬データを機械学習（LightGBM）とLLM（Gemini API）を組み合わせて、着順予測するシステムです。

## 📦 システム構成

```
keiba-ai-system/
├── supabase/              # DBスキーマ定義
├── scraper/               # データ収集層 (Python)
├── ml_engine/             # 予測・評価層 (Python)
└── web_dashboard/         # ダッシュボード (Next.js)
```

## 🚀 セットアップガイド

### 1️⃣ 事前準備

- Python 3.9+
- Node.js 18+
- Supabaseアカウント（✅既に作成済み）
- Gemini API キー（[Google AI Studio](https://aistudio.google.com)から取得）

### 2️⃣ Supabase設定

**プロジェクト情報:**
- **URL**: https://ekvjftmcnpbduwydsese.supabase.co
- **Project ID**: ekvjftmcnpbduwydsese
- **Region**: ap-northeast-1 (Tokyo)

**次のキーを取得してください:**
1. Service Role Key（scraper/, ml_engine/ 用）
2. Anon/Public Key（web_dashboard/ 用）

[Supabaseダッシュボード](https://supabase.com/dashboard)の Settings → API より取得できます。

### 3️⃣ 環境変数の設定

#### scraper/.env
```
SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
SUPABASE_KEY=<あなたのService Role Key>
```

#### ml_engine/.env
```
SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
SUPABASE_KEY=<あなたのService Role Key>
GEMINI_API_KEY=<あなたのGemini API Key>
```

#### web_dashboard/.env.local
```
NEXT_PUBLIC_SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<あなたのAnon Key>
```

### 4️⃣ 依存関係インストール

```bash
# scraper
cd scraper
pip install -r requirements.txt

# ml_engine
cd ../ml_engine
pip install -r requirements.txt

# web_dashboard
cd ../web_dashboard
npm install
```

### 5️⃣ 実行フロー

#### ステップ1: データ収集
```bash
cd scraper
python main.py
```

#### ステップ2: モデル学習
```bash
cd ../ml_engine
python train_lgbm.py
```

#### ステップ3: 推論実行
```bash
# LightGBM推論
python predict_lgbm.py

# Gemini推論
python predict_gemini.py
```

#### ステップ4: ダッシュボード起動
```bash
cd ../web_dashboard
npm run dev
```

ブラウザで http://localhost:3000 を開く

## 📊 データベーススキーマ

### races テーブル
| カラム | 型 | 説明 |
|--------|------|------|
| race_id | TEXT (PK) | レースID |
| race_name | TEXT | レース名 |
| course_type | TEXT | コース種別 |
| distance | INTEGER | 距離 |
| weather | TEXT | 天気 |
| track_condition | TEXT | 馬場状態 |
| race_date | DATE | レース日 |

### race_results テーブル
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | ID |
| race_id | TEXT (FK) | レースID |
| rank | INTEGER | 着順 |
| horse_number | INTEGER | 馬番 |
| horse_name | TEXT | 馬名 |
| odds | DECIMAL | 単勝オッズ |
| popularity | INTEGER | 人気 |
| horse_weight | INTEGER | 馬体重 |

### predictions テーブル
| カラム | 型 | 説明 |
|--------|------|------|
| id | UUID (PK) | ID |
| race_id | TEXT (FK) | レースID |
| horse_number | INTEGER | 馬番 |
| lgbm_win_prob | DECIMAL | LightGBM勝率 |
| gemini_score | INTEGER | Geminiスコア (1-100) |

## 🤖 予測モデル

### LightGBM
- **入力特徴**: 枠番、馬番、オッズ、人気、馬体重、体重増減
- **出力**: 勝利確率 (0-1)
- **目的変数**: 3着以内か (二値分類)

### Gemini API
- **入力**: 出走表データ（馬番、馬名、オッズ、人気など）
- **プロンプト**: プロの競馬アナリスト視点での評価
- **出力**: スコア (1-100)

## 🎯 使用例

```python
# データ収集
from scraper.main import scrape_and_save
scrape_and_save("202405020111")

# モデル推論
from ml_engine.predict_lgbm import predict_and_save as predict_lgbm
from ml_engine.predict_gemini import predict_with_gemini
predict_lgbm("202405020111")
predict_with_gemini("202405020111")

# ダッシュボードで可視化
# http://localhost:3000 にアクセス
```

## 📝 ライセンス

MIT

## 🙋 サポート

問題が発生した場合：
1. `.env` ファイルのキーを確認
2. Supabaseのコンソールでテーブル作成を確認
3. エラーメッセージを確認
