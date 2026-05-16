# 🎯 競馬AI予想システム - セットアップガイド

## ✅ 完了事項

以下の作業が自動で完了しています：

- ✅ **Supabaseプロジェクト作成** 
  - プロジェクトID: `ekvjftmcnpbduwydsese`
  - リージョン: `ap-northeast-1` (Tokyo)
  - URL: https://ekvjftmcnpbduwydsese.supabase.co
  
- ✅ **SQLスキーマ実行** (3テーブル作成)
  - `races` - レース情報
  - `race_results` - 競走成績
  - `predictions` - AI予測結果

- ✅ **全ファイル生成**
  - scraper/ (4ファイル)
  - ml_engine/ (6ファイル)
  - web_dashboard/ (15ファイル)
  - supabase/ (1ファイル)
  - その他設定・ドキュメント (3ファイル)

---

## 🔐 次のステップ：認証情報の取得

### 【重要】Supabaseのキーを取得

1. [Supabaseダッシュボード](https://supabase.com/dashboard)にログイン
2. プロジェクト「keiba-ai-system」を選択
3. **Settings** → **API** を開く

以下の2つのキーをコピーしてください：

#### ① Service Role Key（サーバー側用）
- 用途: `scraper/`, `ml_engine/` 用
- **非常に秘密です。絶対に公開しないでください**
- コピーして保管

#### ② Anon Key（クライアント側用）
- 用途: `web_dashboard/` 用
- クライアント側で使用（多少の露出OK）

---

## 🚀 インストール手順

### 1️⃣ ZIPを解凍

```bash
unzip keiba-ai-system.zip
cd keiba-ai-system
```

### 2️⃣ 環境変数を設定

#### scraper/.env
```bash
SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
SUPABASE_KEY=<上記で取得したService Role Key>
```

#### ml_engine/.env
```bash
SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
SUPABASE_KEY=<上記で取得したService Role Key>
GEMINI_API_KEY=<Google AI Studioで取得>
```

#### web_dashboard/.env.local
```bash
NEXT_PUBLIC_SUPABASE_URL=https://ekvjftmcnpbduwydsese.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<上記で取得したAnon Key>
```

### 3️⃣ Python環境構築

```bash
# scraper
cd scraper
pip install -r requirements.txt
cd ..

# ml_engine
cd ml_engine
pip install -r requirements.txt
cd ..
```

### 4️⃣ Node.js環境構築

```bash
cd web_dashboard
npm install
cd ..
```

---

## 🎬 実行フロー

### ステップ1: Gemini API キーの取得

1. [Google AI Studio](https://aistudio.google.com) にアクセス
2. 「Get API Key」をクリック
3. 「Create API key」で新規キーを生成
4. キーをコピーして `ml_engine/.env` に貼り付け

### ステップ2: データ収集

```bash
cd scraper
python main.py
```

データをnetkeiba.comからスクレイピング → Supabaseに保存

**出力例:**
```
Scraping race_id: 202405020111...
✅ Saved 18 horses for race 202405020111
```

### ステップ3: モデル学習

```bash
cd ../ml_engine
python train_lgbm.py
```

保存されたデータでLightGBMモデルを学習 → `models/lightgbm_model.txt`

**出力例:**
```
✅ Model trained and saved.
```

### ステップ4: 推論実行

#### LightGBM推論
```bash
python predict_lgbm.py
```

**出力例:**
```
✅ Race 202405020111 のLightGBM推論結果を保存しました。
```

#### Gemini推論
```bash
python predict_gemini.py
```

**出力例:**
```
✅ Race 202405020111 のGemini推論結果を保存しました。
```

### ステップ5: ダッシュボード起動

```bash
cd ../web_dashboard
npm run dev
```

ブラウザで **http://localhost:3000** を開く

---

## 📊 ダッシュボード機能

### 🔥 AIハイブリッド推奨馬
- LightGBMとGemini両方で上位に挙がった馬を表示
- 最も信頼度が高い推奨

### 📈 全頭評価リスト
- 各馬のスコア一覧
  - **LightGBM勝率**: 機械学習による確率（%表示）
  - **Geminiスコア**: LLMによる評価（1-100）

---

## 🔍 トラブルシューティング

### ❌ エラー: "モデルファイルがありません"
**原因**: `train_lgbm.py` が実行されていない
**解決**: 
```bash
cd ml_engine
python train_lgbm.py
python predict_lgbm.py  # この後
```

### ❌ エラー: "Supabaseへの接続に失敗"
**原因**: `.env` ファイルのキーが間違っている
**解決**: 
1. Supabaseダッシュボードでキーを再確認
2. `.env` ファイルを修正
3. スクリプトを再実行

### ❌ エラー: "Gemini APIの呼び出し失敗"
**原因**: `GEMINI_API_KEY` が設定されていない、または無効
**解決**:
1. [Google AI Studio](https://aistudio.google.com) で新規キーを生成
2. `ml_engine/.env` に貼り付け
3. `python predict_gemini.py` を実行

### ❌ npm install エラー
**原因**: Node.js バージョンが古い
**解決**:
```bash
# Node.js 18.x 以上が必要
node --version

# インストール: https://nodejs.org/
```

---

## 📚 ファイル構成

```
keiba-ai-system/
├── README.md                          # メインドキュメント
├── .gitignore                         # Git除外設定
│
├── supabase/
│   └── schema.sql                     # DB スキーマ（既に実行済み）
│
├── scraper/                           # データ収集層
│   ├── .env                           # 環境変数 ⚙️設定必須
│   ├── requirements.txt
│   ├── main.py                        # メインスクリプト
│   └── data_cleaner.py                # データ前処理
│
├── ml_engine/                         # AI予測層
│   ├── .env                           # 環境変数 ⚙️設定必須
│   ├── requirements.txt
│   ├── train_lgbm.py                  # モデル学習
│   ├── predict_lgbm.py                # LGBM推論
│   ├── predict_gemini.py              # Gemini推論
│   ├── evaluate_models.py             # 評価・シミュレーション
│   └── models/                        # モデル保存先（自動作成）
│
└── web_dashboard/                     # Next.js ダッシュボード
    ├── .env.local                     # 環境変数 ⚙️設定必須
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.ts
    ├── postcss.config.mjs
    ├── src/
    │   ├── lib/
    │   │   └── supabaseClient.ts      # Supabase クライアント
    │   ├── components/
    │   │   ├── PredictionTable.tsx    # 予測結果テーブル
    │   │   └── ModelCompare.tsx       # ハイブリッド推奨馬
    │   └── app/
    │       ├── globals.css            # グローバルスタイル
    │       ├── layout.tsx             # レイアウト
    │       ├── page.tsx               # メインページ
    │       └── api/
    │           └── predictions/
    │               └── route.ts       # API エンドポイント
```

---

## 🎓 各モジュールの役割

| モジュール | 言語 | 役割 |
|-----------|------|------|
| **scraper** | Python | netkeiba.com からデータ取得 |
| **ml_engine** | Python | LightGBM学習＆Gemini推論 |
| **web_dashboard** | TypeScript/React | 結果の可視化 |

---

## 💡 カスタマイズ例

### 📍 別のレースIDで予測

```bash
cd scraper
python -c "from main import scrape_and_save; scrape_and_save('202405030101')"

cd ../ml_engine
python predict_lgbm.py  # グローバル変数を変更
python predict_gemini.py
```

### 🎯 LightGBMの特徴量を変更

`ml_engine/train_lgbm.py` の `features` を編集：

```python
features = ['frame_number', 'horse_number', 'odds', 'popularity']  # カスタマイズ
```

### 🤖 Geminiのプロンプトを変更

`ml_engine/predict_gemini.py` の `prompt` を編集してAIの評価基準を変更可能。

---

## 📞 質問・サポート

- Supabase について: https://supabase.com/docs
- LightGBM について: https://lightgbm.readthedocs.io/
- Gemini API について: https://ai.google.dev/docs
- Next.js について: https://nextjs.org/docs

---

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**🎉 セットアップ完了後、データ競馬の世界へようこそ！**
