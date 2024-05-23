import warnings
import json
from read_pdf import read_pdf
from get_interactions import extraction_chain
from convert_to_cx2 import convert_to_cx2
warnings.filterwarnings("ignore")


doc = read_pdf("papers/pmc6044858.pdf")
page_content = doc[50:30000]
# print(page_content)

results = extraction_chain.invoke({"input": page_content})
json_output = json.dumps(results, indent=4)
print(json_output)

# Convert extracted data to CX2 format
# cx2_network = convert_to_cx2(results)

# # Convert CX2 data to JSON
# cx2_json = json.dumps(cx2_network, indent=4)
# print(cx2_json)
