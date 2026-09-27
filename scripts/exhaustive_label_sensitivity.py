"""Exhaustive descriptive assignment sensitivity, not an exchangeable permutation test."""
from pathlib import Path
import csv,hashlib,itertools,json,math,statistics
from collections import defaultdict,Counter
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/MTBLS437_maf.tsv'
cols=[f'MR-CTB51A_replicate{i}' for i in range(1,5)]+[f'NPB-HP_replicate{i}' for i in range(1,6)]
groups=defaultdict(list)
for row in csv.DictReader(p.open(newline=''),delimiter='\t'):
 name=row['metabolite_identification'].strip()
 if name.lower() in ('','unknown'):continue
 key=row['database_identifier'].strip().upper() or 'NAME:'+name.lower()
 groups[key].append([float(row[c]) for c in cols])
assert len(groups)==104
arrays=[[statistics.median(r[i] for r in group) for i in range(9)] for group in groups.values()]
assert all(all(math.isfinite(v) and v>0 for v in arr) for arr in arrays)

def effect(values,group):
 a=[values[i] for i in group];b=[values[i] for i in range(9) if i not in group]
 return statistics.mean(a)-statistics.mean(b)

def stable(arr,group):
 logs=[math.log(v) for v in arr]
 e=effect(arr,group);z=effect(logs,group)
 if not e or not z or e*z<=0:return False
 for i in range(9):
  a=[arr[j] for j in range(9) if j!=i and j in group]
  b=[arr[j] for j in range(9) if j!=i and j not in group]
  la=[logs[j] for j in range(9) if j!=i and j in group]
  lb=[logs[j] for j in range(9) if j!=i and j not in group]
  if (statistics.mean(a)-statistics.mean(b))*z<=0 or (statistics.mean(la)-statistics.mean(lb))*z<=0:return False
 return True
counts={','.join(map(str,g)):sum(stable(a,set(g)) for a in arrays) for g in itertools.combinations(range(9),4)}
obs=counts['0,1,2,3']
result={'source':'https://www.ebi.ac.uk/metabolights/MTBLS437','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'distinct_analytes':len(arrays),'all_four_of_nine_assignments':len(counts),'observed_stable_count':obs,
 'assignments_with_count_at_least_observed':sum(v>=obs for v in counts.values()),
 'assignment_counts_summary':{'minimum':min(counts.values()),'median':statistics.median(counts.values()),'maximum':max(counts.values())},
 'assignment_count_histogram':dict(sorted(Counter(counts.values()).items())),
 'counts_by_group':counts,'description':'Enumerate all 126 four-versus-five partitions of nine samples, use identifier-deduped per-sample medians and raw/log direction stability through leave-one-out views.',
 'limits':['This exhaustive enumeration is post-outcome and assignments may be confounded/nonexchangeable. The at-least-observed frequency is not an inferential p-value.','The score can favor many alternative partitions because feature effects and technical conditions are correlated; no independent cohort or cross-study validation.','Counts are analytes, not independently accessioned datasets, and not oral antigen dose.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
