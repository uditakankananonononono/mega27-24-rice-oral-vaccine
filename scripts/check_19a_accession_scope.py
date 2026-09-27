"""Reconcile published 19A genome accession to live archived ENA run metadata."""
from pathlib import Path
from bs4 import BeautifulSoup
import csv,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
XML=ROOT/'data/sources/pmc10978600.xml'
TSV=ROOT/'data/sources/DRX362635_ena_run.tsv'
URL='https://www.ebi.ac.uk/ena/portal/api/filereport?accession=DRX362635&result=read_run&fields=run_accession%2Cexperiment_accession%2Csample_accession%2Cstudy_accession%2Clibrary_strategy%2Clibrary_source%2Cfastq_bytes&format=tsv'

def replay():
 xml=XML.read_bytes();tsv=TSV.read_bytes()
 soup=BeautifulSoup(xml,'xml');paras=[p.get_text(' ',strip=True) for p in soup.find_all('p')]
 matches=[p for p in paras if 'DRX362635' in p and 'SAMD00491847' in p and ('whole genome' in p or 'whole-genome' in p)]
 if not matches: raise ValueError('Primary published WGS accession passage missing')
 rows=list(csv.DictReader(tsv.decode().splitlines(),delimiter='\t'))
 assert len(rows)==1 and rows[0]['experiment_accession']=='DRX362635' and rows[0]['sample_accession']=='SAMD00491847'
 row=rows[0]
 assert row['library_strategy']=='WGS' and row['library_source']=='GENOMIC'
 sizes=[int(x) for x in row['fastq_bytes'].split(';')]
 assert len(sizes)==2
 return {'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/', 'article_sha256':hashlib.sha256(xml).hexdigest(), 'source_passage':matches[0], 'ena_report_url':URL,'ena_report_sha256':hashlib.sha256(tsv).hexdigest(),'metadata':{'experiment':row['experiment_accession'],'run':row['run_accession'],'sample':row['sample_accession'],'study':row['study_accession'],'library_strategy':row['library_strategy'],'library_source':row['library_source'],'advertised_fastq_bytes':sizes,'total_advertised_fastq_bytes':sum(sizes)},'scope':'A single 19A leaf/seedling WGS assay used to locate the genomic integration; it is not a seed-protein or oral-dose measurement.','limits':['ENA metadata were fetched, not either of the two advertised compressed FASTQ payloads; zero individually fetched-and-used accession payload credit.','The published 19A CTB n=3 lot SDS-PAGE numbers are a different measurement, and this run must not be treated as three independently accessioned protein samples.','This is a provenance clarification, not an antigen design, expression model, efficacy result, discovery or fair benchmark.'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}

if __name__=='__main__': print(json.dumps(replay(),sort_keys=True,indent=2))
