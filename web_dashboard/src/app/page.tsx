import { supabase } from '@/lib/supabaseClient';
import PredictionTable from '@/components/PredictionTable';
import ModelCompare from '@/components/ModelCompare';

export const dynamic = 'force-dynamic';

export default async function Home() {
  const { data: predictions, error } = await supabase
    .from('predictions')
    .select('*')
    .order('lgbm_win_prob', { ascending: false });

  if (error) console.error(error);

  return (
    <main className="max-w-5xl mx-auto p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-extrabold text-slate-800">ハイブリッド AI 競馬予想</h1>
        <p className="text-slate-500 mt-2">LightGBM × Gemini 1.5 Pro Dashboard</p>
      </header>

      <section>
        <ModelCompare predictions={predictions || []} />
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4 border-l-4 border-blue-500 pl-2">全頭評価リスト</h2>
          <PredictionTable predictions={predictions || []} />
        </div>
      </section>
    </main>
  );
}
