"""Source-integrity replay of printed Supplementary Table 1 aggregate arithmetic."""
from pathlib import Path
import hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'data/sources/PMC10978600_DataSheet_1.pdf'
text=subprocess.check_output(['pdftotext','-f','15','-l','15','-layout',str(pdf),'-'], text=True)
section=text.split('Supplementary Table 1. Transformation frequency',1)[1].split('Supplementary Table 2.',1)[0]
rows=[]
for line in section.splitlines():
    m=re.match(r'^\s*(1|2|3|4|Total)\s+(\d+)\s+(\d+)\s+(\d+)%\s+(\d+)\s+(.*)$',line)
    if m:
        label,a,b,printed,positive,line_name=m.groups()
        a,b,printed,positive=map(int,(a,b,printed,positive))
        rows.append({'row':label,'screened_calli':a,'gene_positive_calli':b,'printed_ratio_percent':printed,
                     'calculated_ratio_percent':100*b/a,'protein_positive_t1_seeds':positive,'printed_line':line_name.strip(),
                     'rounds_to_printed_integer_percent':round(100*b/a)==printed})
assert [r['row'] for r in rows]==['1','2','3','4','Total']
assert sum(r['screened_calli'] for r in rows[:4])==rows[4]['screened_calli']==192
assert sum(r['gene_positive_calli'] for r in rows[:4])==rows[4]['gene_positive_calli']==59
assert sum(r['protein_positive_t1_seeds'] for r in rows[:4])==rows[4]['protein_positive_t1_seeds']==48
assert all(r['rounds_to_printed_integer_percent'] for r in rows[:4])
assert rows[4]['printed_ratio_percent']==32 and round(rows[4]['calculated_ratio_percent'])==31
result={'source_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10978600/supplementaryFiles',
        'source_file':pdf.name,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'source_pdf_page':15,
        'rows':rows,'finding':'Four individual percentages round correctly, and all three total counts sum correctly; the printed total ratio 32% does not equal 59/192 = 30.729%, which rounds to 31% under integer nearest rounding.',
        'limits':['Printed source arithmetic only, not independent experiments or biological validation','No inference about line performance, vaccine dose, immune outcome, or a causal explanation for the printed discrepancy'],
        'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
