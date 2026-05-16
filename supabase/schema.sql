-- 1. レース基本情報
CREATE TABLE races (
    race_id TEXT PRIMARY KEY,
    race_name TEXT,
    course_type TEXT,
    distance INTEGER,
    weather TEXT,
    track_condition TEXT,
    race_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. レース結果詳細
CREATE TABLE race_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    race_id TEXT REFERENCES races(race_id) ON DELETE CASCADE,
    rank INTEGER,
    frame_number INTEGER,
    horse_number INTEGER,
    horse_name TEXT NOT NULL,
    horse_id TEXT,
    jockey_name TEXT,
    weight_carried DECIMAL,
    odds DECIMAL,
    popularity INTEGER,
    finish_time_seconds DECIMAL,
    last_3f DECIMAL,
    horse_weight INTEGER,
    horse_weight_diff INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(race_id, horse_number)
);

-- 3. 予測結果保存用
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    race_id TEXT REFERENCES races(race_id) ON DELETE CASCADE,
    horse_number INTEGER,
    horse_name TEXT,
    lgbm_win_prob DECIMAL,
    gemini_score INTEGER,
    expected_value DECIMAL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(race_id, horse_number)
);

-- 検索高速化のためのインデックス
CREATE INDEX idx_race_results_race_id ON race_results(race_id);
CREATE INDEX idx_predictions_race_id ON predictions(race_id);
