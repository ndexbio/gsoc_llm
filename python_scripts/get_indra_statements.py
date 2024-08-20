import json
from indra.sources import reach


def main():
    # All the code that you currently have running at the top level
    results = reach.process_pmc('PMC3898398')
    statements = results.statements
    statements_json = [stmt.to_json() for stmt in statements]
    with open("results/pmc3898398/indra_results.json", "w") as file:
        json.dump(statements_json, file, indent=4)

    return statements_json


if __name__ == "__main__":
    statements_json = main()
    print(statements_json)

#perform extraction using indra reach
# indra_reach_results["INDRA_REACH_extractions"] = []
# start_time = time.time()
# for index in selected_keys:
#     sentence = sentences[index]
#     reach_processor = reach.api.process_text(sentence)
#     stmts = reach_processor.statements
#     statements_json = [stmt.to_json() for stmt in stmts]
#     indra_reach_results["INDRA_REACH_extractions"].append({
#         "Index": index,
#         "Sentence": sentence,
#         "Results": statements_json
#     })
# end_time = time.time()
# elapsed_time = end_time - start_time
# elapsed_minutes = elapsed_time / 60
# print(f"Time taken for indra processing: {elapsed_time:.2f} seconds ({elapsed_minutes:.2f} minutes)")

# Save the INDRA REACH results to a JSON file
# with open('indra_results.json', 'w') as indra_file:
#     json.dump(indra_results, indra_file, indent=4)

# indra_combined_results = create_combined_results(indra_reach_results["INDRA_REACH_extractions"])

# with open('results/pmc3898398/indra_combined_results.json', 'w') as indra_file:
#     json.dump(indra_combined_results, indra_file, indent=4)