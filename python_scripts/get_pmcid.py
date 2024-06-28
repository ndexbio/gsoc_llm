import requests
from indra_nxml_extraction import id_lookup, filter_pmids


def get_pmcid_from_pubmed(pubmed_id):
    """
    Fetches the PMCID for a given PubMed ID.

    :param pubmed_id: The PubMed ID to lookup.
    :return: The corresponding PMCID.
    """
    url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pubmed_id}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()   
    if 'records' in data and len(data['records']) > 0 and 'pmcid' in data['records'][0]:
        return data['records'][0]['pmcid']
    else:
        raise ValueError(f"No PMCID found for PubMed ID: {pubmed_id}")


pmc_id = get_pmcid_from_pubmed(13086)
print(pmc_id)

# # Function to read PMIDs from a file
# def read_pmids(file_path):
#     with open(file_path, 'r') as file:
#         pmids = [line.strip() for line in file.readlines()]
#     return pmids


# # Read PMIDs from the text file
# pmid_file = '/Users/favourjames/Downloads/adrenocortical_carcinoma_v2/adrenocortical_carcinoma_pmids.txt'
# pmids = read_pmids(pmid_file)

# print(pmids)

# # filtered_pmid = filter_pmids(pmids, 'fulltext')
# # print(filtered_pmid)
