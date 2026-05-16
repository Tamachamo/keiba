import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabaseClient';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const race_id = searchParams.get('race_id');

  let query = supabase.from('predictions').select('*').order('lgbm_win_prob', { ascending: false });
  if (race_id) query = query.eq('race_id', race_id);

  const { data, error } = await query;
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ data });
}
