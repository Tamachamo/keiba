```react
import { supabase } from '@/lib/supabaseClient';
import PredictionTable from '@/components/PredictionTable';
import ModelCompare from '@/components/ModelCompare';
import Link from 'next/link';

export const dynamic = 'force-dynamic';

export default async function Home({ searchParams }: { searchParams: { race_id?: string } }) {
  // 1. 保存されている予測データからユニークなレースIDを取得
  const { data: allPredictions } = await supabase
    .from('predictions')
    .select('race_id')
    .order('race_id', { ascending: false });

  // 重複を削除してレースIDのリストを作成
  const uniqueRaceIds = Array.from(new Set(allPredictions?.map(p => p.race_id) || []));
  
  // URLパラメータで指定されたレースID、なければ最新のレースIDを使用
  const currentRaceId = searchParams.race_id || uniqueRaceIds[0] || '';

  // 2. 選択されたレースの予測データを取得
  const { data: predictions, error } = await supabase
    .from('predictions')
    .select('*')
    .eq('race_id', currentRaceId)
    .order('lgbm_win_prob', { ascending: false });

  if (error) console.error(error);

  return (
    <main className="max-w-5xl mx-auto p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-800">ハイブリッド AI 競馬予想</h1>
        <p className="text-slate-500 mt-2">LightGBM × Gemini Dashboard</p>
      </header>

      {/* レース切り替え用のセレクター */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow border border-slate-200">
        <label className="block text-sm font-semibold text-slate-600 mb-2">レース切り替え</label>
        <div className="flex flex-wrap gap-2">
          {uniqueRaceIds.length === 0 ? (
            <span className="text-slate-500">データがありません</span>
          ) : (
            uniqueRaceIds.map((id) => (
              <Link 
                key={id} 
                href={`/?race_id=${id}`}
                className={`px-4 py-2 rounded-md text-sm font-bold transition-colors ${
                  currentRaceId === id 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                {/* 11~12文字目がレース番号 */}
                {id.slice(10, 12)}R ({id})
              </Link>
            ))
          )}
        </div>
      </div>

      {currentRaceId ? (
        <section>
          <ModelCompare predictions={predictions || []} />
          <div className="mt-8">
            <h2 className="text-xl font-bold mb-4 border-l-4 border-blue-500 pl-2">
              全頭評価リスト ({currentRaceId.slice(10, 12)}R)
            </h2>
            <PredictionTable predictions={predictions || []} />
          </div>
        </section>
      ) : (
        <p className="text-slate-500 text-center py-10">予測データを取得（スクレイピング）してください。</p>
      )}
    </main>
  );
}

```
