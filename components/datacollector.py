import io

from Bio import SeqIO

def get_single_batch(session, url):
    response = session.get(url)
    if response.status_code == 200:
        for record in SeqIO.parse(io.StringIO(response.text), "fasta"):
            yield str(record.seq)
    else:
        return []