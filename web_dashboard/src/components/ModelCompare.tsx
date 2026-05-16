type Prediction = {
  id: string;
  horse_number: number;
  horse_name: string;
  lgbm_win_prob: number | null;
  gemini_score: number | null;
};

export default function ModelCompare({ predictions }: { predictions: Prediction[] }) {
  const validPreds = predictions.filter(p => p.lgbm_win_prob !== null && p.gemini_score !== null);
  
  const sortedByLgbm = [...validPreds].sort((a, b) => (b.lgbm_win_prob!) - (a.lgbm_win_prob!)).slice(0, 3);
  const sortedByGemini = [...validPreds].sort((a, b) => (b.gemini_score!) - (a.gemini_score!)).slice(0, 3);

  const commonPicks = sortedByLgbm.filter(lgbmPick => 
    sortedByGemini.some(geminiPick => geminiPick.horse_number === lgbmPick.horse_number)
  );

  return (
    <div className="bg-white p-6 rounded-lg shadow mt-6 border-t-4 border-amber-400">
      <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center">
        <span className="mr-2">🔥</span> AIハイブリッド推奨馬 (両モデル上位一致)
      </h3>
      
      {commonPicks.length > 0 ? (
        <ul className="space-y-3">
          {commonPicks.map((pick) => (
            <li key={pick.id} className="flex justify-between items-center bg-amber-50 p-3 rounded border border-amber-200">
              <span className="font-bold text-lg">{pick.horse_number}番 {pick.horse_name}</span>
              <div className="text-sm flex space-x-4 font-semibold">
                <span className="text-blue-700">LGBM: {(pick.lgbm_win_prob! * 100).toFixed(1)}%</span>
                <span className="text-emerald-700">Gemini: {pick.gemini_score}pt</span>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-slate-500">現在、両AIの意見が一致する推奨馬はありません。</p>
      )}
    </div>
  );
}
