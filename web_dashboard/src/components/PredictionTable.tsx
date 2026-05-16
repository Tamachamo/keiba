type Prediction = {
  id: string;
  horse_number: number;
  horse_name: string;
  lgbm_win_prob: number | null;
  gemini_score: number | null;
};

export default function PredictionTable({ predictions }: { predictions: Prediction[] }) {
  if (!predictions || predictions.length === 0) return <p>データがありません。</p>;

  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow mt-4">
      <table className="min-w-full text-left">
        <thead className="bg-slate-800 text-white">
          <tr>
            <th className="px-4 py-3">馬番</th>
            <th className="px-4 py-3">馬名</th>
            <th className="px-4 py-3">LightGBM 勝率</th>
            <th className="px-4 py-3">Gemini スコア</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {predictions.map((p) => (
            <tr key={p.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-bold text-center">{p.horse_number}</td>
              <td className="px-4 py-3 font-semibold">{p.horse_name}</td>
              <td className="px-4 py-3 text-blue-600">
                {p.lgbm_win_prob ? `${(p.lgbm_win_prob * 100).toFixed(1)}%` : '-'}
              </td>
              <td className="px-4 py-3 text-emerald-600">
                {p.gemini_score ? `${p.gemini_score} / 100` : '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
