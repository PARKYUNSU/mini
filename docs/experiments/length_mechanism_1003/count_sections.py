"""RAG 응답의 템플릿 섹션/고정 슬롯을 세어 (A)/(B) 를 가른다. 사용: python3 count_sections.py"""
import json, re, statistics as st, collections, pathlib

HERE = pathlib.Path(__file__).parent
rows = [json.loads(l) for l in open(HERE / 'data' / 'ragdump.jsonl')]

# 마크업과 무관하게 '이름'으로 섹션을 찾는다 (## / ### / **굵게** 모두 포함)
SECTIONS = {'선별': '선별 논문', '부족': '부족 논문', 'gap': 'Research Gap'}
PAPER = re.compile(r'📄|^\s*\d+\.\s*\*{0,2}\[?\d{4}\.', re.M)
# 고정 3슬롯: 값만 떼어낸다
SLOTS = {
    '무엇을': re.compile(r'무엇을 개선했는지\s*[:：]\s*(.+)'),
    '어떻게': re.compile(r'어떻게 해결했는지\s*[:：]\s*(.+)'),
    '차별점': re.compile(r'기존 대비 차별점\s*[:：]\s*(.+)'),
}
GAPBUL = re.compile(r'^\s*[-•]\s+(.*\S)\s*$', re.M)

def feats(t):
    f = {'chars': len(t)}
    f['secs'] = sum(1 for key in SECTIONS.values() if key in t)
    f['papers'] = len(re.findall(r'📄', t))
    # 고정 슬롯: 채워진 개수와 값 길이
    filled, lens = 0, []
    for name, rx in SLOTS.items():
        vals = [v.strip() for v in rx.findall(t)]
        filled += len(vals)
        lens += [len(v) for v in vals]
    f['slot_n'] = filled                                  # 채워진 고정 슬롯 수
    f['slot_len'] = st.mean(lens) if lens else 0          # 고정 슬롯당 값 길이
    # Research Gap 구간의 불릿
    i = t.find('Research Gap')
    gap = t[i:] if i >= 0 else ''
    gb = GAPBUL.findall(gap)
    f['gap_n'] = len(gb)
    f['gap_len'] = st.mean(len(x) for x in gb) if gb else 0
    return f

by = collections.defaultdict(list)
for r in rows:
    if r['status'] == 'ok':
        by[r['model']].append(feats(r['text']))

ORDER = ['qwen3.5:9b', 'yunsur_v9', 'yunsur_v10']
KEYS = [('chars','전체 길이'),
        ('secs','섹션 수 (3)'), ('papers','논문 수 (2)'),
        ('slot_n','고정슬롯 채움 (6)'), ('slot_len','★고정슬롯당 길이'),
        ('gap_n','Gap 불릿 수 (2)'), ('gap_len','Gap 불릿 길이')]

print(f"{'지표':<18}", ''.join(f'{m:>13}' for m in ORDER), '   base→v10')
print('-' * 78)
for k, label in KEYS:
    v = {m: st.mean(f[k] for f in by[m]) for m in ORDER}
    b, t10 = v['qwen3.5:9b'], v['yunsur_v10']
    d = f'{(t10/b-1)*100:+6.1f}%' if b else '      -'
    print(f'{label:<18}', ''.join(f'{v[m]:>13.2f}' for m in ORDER), f'  {d}')

# 템플릿을 아예 따랐는가 (섹션 이름이 하나도 없으면 이탈)
print()
for m in ORDER:
    off = sum(1 for f in by[m] if f['secs'] == 0)
    print(f'  {m:<12} 템플릿 이탈 {off}/{len(by[m])} 시행')

# ── 문항별 짝지은 비교 (base vs v10), 시행 3회 평균 ──
print('\n문항별 (base → v10)   고정슬롯당 길이      고정슬롯 채움 수')
print('-' * 62)
per = collections.defaultdict(dict)
for r in rows:
    if r['status'] != 'ok':
        continue
    per[r['id']].setdefault(r['model'], []).append(feats(r['text']))

up_len = up_n = n = 0
for iid in sorted(per):
    d = per[iid]
    if 'qwen3.5:9b' not in d or 'yunsur_v10' not in d:
        continue
    bl = st.mean(f['slot_len'] for f in d['qwen3.5:9b'])
    vl = st.mean(f['slot_len'] for f in d['yunsur_v10'])
    bn = st.mean(f['slot_n'] for f in d['qwen3.5:9b'])
    vn = st.mean(f['slot_n'] for f in d['yunsur_v10'])
    n += 1
    up_len += vl > bl
    up_n += vn > bn
    print(f'  {iid}   {bl:6.1f} → {vl:6.1f}  {"길어짐" if vl>bl else "짧아짐":<6}'
          f'     {bn:4.1f} → {vn:4.1f}  {"늘어남" if vn>bn else ("같음" if vn==bn else "줄어듦")}')
print(f'\n  길이 증가 {up_len}/{n} 문항 · 슬롯 수 증가 {up_n}/{n} 문항')

from math import comb
p = sum(comb(n, k) for k in range(up_len, n + 1)) / 2**n * 2
print(f'  길이 증가 부호검정 양측 p = {min(p,1.0):.4f}')
