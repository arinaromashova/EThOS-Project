from sentence_transformers import SentenceTransformer, util
import torch
import nlp_search.data_upload as data_upload


def query_response(user_query, number_of_replies=5):
    """Takes the user query and responds with N=number_of_replies
    of semantically close titles and abstracts

    Args:
        user_query (str): user search query
    """
    # number of papers for re-ranking

    RERANKING_RANGE = 150
    TITLE_WEIGHT = 0.4
    ABSTRACT_WEIGHT = 0.6

    # preparation of the data and embedder
    embedder = SentenceTransformer("msmarco-distilbert-base-v4")
    thesis_df = data_upload.thesis_data_upload()
    title_embeddings = data_upload.title_embeddings_upload()
    abstract_embeddings = data_upload.abstract_embeddings_upload()
    # get the query embedding
    query_embedding = embedder.encode(user_query, convert_to_tensor=True)

    # get the indexes of the relevant papers based on titles
    cos_scores = util.cos_sim(query_embedding, title_embeddings)[0]
    top_results_titles = torch.topk(cos_scores, k=RERANKING_RANGE)
    # print("-----BASED ON TITLES-----")
    # for i in top_results_titles[1]:
    #     print(thesis_df["Title"].iloc[int(i)])
    top_indexes = {}
    start = RERANKING_RANGE
    for i in top_results_titles[1]:
        top_indexes[str(int(i))] = start * TITLE_WEIGHT
        start -= 1

    # get the indexes of the relevant papers based on abstracts
    cos_scores = util.cos_sim(query_embedding, abstract_embeddings)[0]
    top_results_abstracts = torch.topk(cos_scores, k=RERANKING_RANGE)
    # print("-----BASED ON ABSTRACTS-----")
    # for i in top_results_abstracts[1]:
    #     print(thesis_df["Title"].iloc[int(i)])
    start = RERANKING_RANGE
    for i in top_results_abstracts[1]:
        key_now = str(int(i))
        if key_now in top_indexes:
            top_indexes[key_now] += start * ABSTRACT_WEIGHT
        else:
            top_indexes[key_now] = start * ABSTRACT_WEIGHT
        start -= 1

    # getting the top indexes
    sorted_result = dict(
        sorted(top_indexes.items(), key=lambda item: item[1], reverse=True)
    )
    best_ids = list(sorted_result.keys())[0:number_of_replies]
    # print(sorted_result)

    # prepare a dictionary with best papers' data
    result = []
    for id in best_ids:
        thesis_data = {
            "Title": thesis_df["Title"].iloc[int(id)],
            "Abstract": thesis_df["Abstract_full"].iloc[int(id)],
            "Url": thesis_df["EThOS URL"].iloc[int(id)],
            "Summary": thesis_df["Abstract_short"].iloc[int(id)],
        }
        result.append(thesis_data)
    # print(result)
    return best_ids, result


if __name__ == "__main__":
    ids, th_data = query_response("propagation of ultrasound in metals")
    print(ids)
    for thesis in th_data:
        print(thesis["Title"])
