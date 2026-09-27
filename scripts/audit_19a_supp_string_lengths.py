"""Printed-string length audit of 19A supplementary Tables 2 and 4.

Replays the archived supplementary PDF text layer: for Supplementary Table 4,
joins each wrapped printed string and compares its character count to the
printed bp label; for Supplementary Table 2, counts characters of each printed
primer string (no lengths are printed there) and records descriptive range.
Stores hashes, not the strings themselves. Pure print-layer QC.
"""
from pathlib import Path
import hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'data/sources/PMC10978600_DataSheet_1.pdf'
sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
text=subprocess.check_output(['pdftotext','-f','15','-l','18','-layout',str(pdf),'-'],text=True)

# --- Supplementary Table 4: labeled border strings ------------------------
t4=text.split('Supplementary Table 4.',1)[1]
lines=[x for x in t4.splitlines()]
labels={'LB-1':90,'LB-2':90,'LB-3':89,'RB-1':80,'RB-2':80,'RB-3':80,'RB-4':67}
designed_row=None
for x in lines:
    m=re.search(r'T-DNA vector designed\s+([\d bp]+)$',x)
    if m: designed_row=[int(v) for v in re.findall(r'(\d+)\s*bp',x)]
t4_rows=[]
for i,x in enumerate(lines):
    m=re.match(r'^(LB-[123]|RB-[1234])\s+([ACGT]+)\s*$',x)
    if not m: continue
    lab,chunk1=m.group(1),m.group(2)
    nxt=lines[i+1] if i+1<len(lines) else ''
    m2=re.match(r'^\((\d+) bp\)\s*([ACGT]+)?\s*$',nxt)
    assert m2, f'continuation missing for {lab}'
    printed=int(m2.group(1)); chunk2=m2.group(2) or ''
    s_join=chunk1+chunk2
    t4_rows.append({'label':lab,'printed_bp':printed,'counted_chars':len(s_join),
                    'length_matches_printed':len(s_join)==printed,
                    'string_sha256':hashlib.sha256(s_join.encode()).hexdigest()[:16]})
assert [r['label'] for r in t4_rows]==list(labels)
assert all(r['printed_bp']==labels[r['label']] for r in t4_rows)
designed_matches=all(d==labels[l] for d,l in zip(designed_row,labels))

# --- Supplementary Table 2: primer strings (no printed lengths) -----------
t2=text.split('Supplementary Table 2.',1)[1].split('Supplementary Table 3.',1)[0]
primers=[]
for line in t2.splitlines():
    m=re.match(r"^\s*(.+?)\s+5[^ACGT\s]*\s*([ACGTacgt]{10,})",line)
    if m:
        name,seq=m.group(1).strip(),m.group(2).upper()
        primers.append({'name':name,'counted_chars':len(seq),
                        'string_sha256':hashlib.sha256(seq.encode()).hexdigest()[:16]})
assert len(primers)==19, f'parsed {len(primers)} primers'
lens=[p['counted_chars'] for p in primers]

out={'source_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10978600/supplementaryFiles',
 'source_file':pdf.name,'sha256':sha,'source_pdf_pages':'15-18',
 'checks':{
   'table4_designed_lengths_row':designed_row,
   'table4_designed_row_matches_labels':designed_matches,
   'table4_rows':t4_rows,
   'table4_all_lengths_match_printed':all(r['length_matches_printed'] for r in t4_rows),
   'table4_mismatches':[r['label'] for r in t4_rows if not r['length_matches_printed']],
   'table2_primer_count':len(primers),
   'table2_primer_length_range':[min(lens),max(lens)],
   'table2_primers':primers},
 'limits':['Text-layer character counts of printed strings only; strings themselves are not reproduced in the JSON, only 16-char hash prefixes',
  'A matching character count does not verify the underlying sequence against any genomic record; no accession payload was fetched or aligned',
  'Supplementary Table 2 prints no lengths, so its counts are descriptive, not a pass/fail check',
  'PDF text-layer extraction: a malformed glyph in the layer would surface as a count mismatch and is indistinguishable from a print defect without visual inspection'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
