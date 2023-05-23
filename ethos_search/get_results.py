import ethos_search.thesis_ids_on_request
from ethos_search.thesis_data_extract import get_thesis_data


def main_app(user_query):
    all_thesis_ids = (
        ethos_search.thesis_ids_on_request.process_request_to_get_ids(
            user_query
        )
    )
    MAX_NUMBER_OF_ETHOS_REPLIES = 5
    # print(all_thesis_ids, len(result))
    thesis_data = []
    if len(all_thesis_ids) > MAX_NUMBER_OF_ETHOS_REPLIES:
        print(
            f"There are more than {MAX_NUMBER_OF_ETHOS_REPLIES} responses -"
            + "make your query more specific"
        )
    for thesis_id in all_thesis_ids[0:MAX_NUMBER_OF_ETHOS_REPLIES]:
        thesis_data.append(get_thesis_data(thesis_id))
    return thesis_data, len(all_thesis_ids)


if __name__ == "__main__":
    query = "ultrasound dislocation"
    result = main_app(query)
    print(result)
    # for i, thesis in enumerate(result):
    #     print(
    #         "\n\n\n",
    #         f"Thesis {i}\n",
    #         "TITLE:\n",
    #         thesis["Title"],
    #         "ABSTRACT:\n",
    #         thesis["Abstract"],
    #     )
