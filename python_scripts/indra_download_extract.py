import requests 
from indra_nxml_extraction import get_xml, extract_text

pmc_id = "PMC6044858"

if pmc_id.upper().startswith('PMC'):
    pmc_id = pmc_id[3:]

pmc_url = 'https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi'

params = {}
params['verb'] = 'GetRecord'
params['identifier'] = 'oai:pubmedcentral.nih.gov:%s' % pmc_id
params['metadataPrefix'] = 'pmc'

# Submit the request
res = requests.get(pmc_url, params)
res.text

xml_string = get_xml(pmc_id)
text = extract_text(xml_string)
with open("results/pmc6044858/output.xml", "w") as file:
    file.write(xml_string)


# xml_string = get_xml_from_file("PMC6070353.xml")
# text = extract_text(xml_string)
# lines = text.splitlines()
