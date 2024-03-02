import requests
import responses

import components.datacollector as cd

url_good = 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28human+sk3%29&size=1'
url_bad = 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28human+sk3%29&size=-5'

example_sequence = 'MDTSGHFHDSGVGDLDEDPKCPCPSSGDEQQQQQQQQQQQQPPPPAPPAAPQQPLGPSLQ'
example_fasta = '''>sp|Q9UGI6|KCNN3_HUMAN Small conductance OS=Homo sapiens OX=9606 GN=KCNN3 PE=1 SV=2\nMDTSGHFHDSGVGDLDEDPKCPCPSSGDEQQQQQQQQQQQQPPPPAPPAAPQQPLGPSLQ'''

@responses.activate
def test_get_single_batch():
    session = requests.Session()
    responses.get(url_bad, body="No response", status=400, content_type="text/plain")
    responses.get(url_good, body=example_fasta, status=200, content_type="text/plain")

    assert not list(cd.get_single_batch(session, url_bad)) 
    assert not list(cd.get_single_batch(session, url_good)) == [ "fake sequence" ] 
    assert list(cd.get_single_batch(session, url_good)) == [ example_sequence ]
