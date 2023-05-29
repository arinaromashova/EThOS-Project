import pandas as pd
import torch


def thesis_data_upload():
    df_full_data = pd.read_pickle("nlp_search/ethos_data.pkl")
    return df_full_data


def title_embeddings_upload():
    title_embeddings = torch.load(
        "nlp_search/title_embeddings(msmarco-distilbert-base-v4).pt",
        map_location=torch.device("cpu"),
    )
    return title_embeddings


def abstract_embeddings_upload():
    abstract_embeddings = torch.load(
        "nlp_search/abstract_embeddings(msmarco-distilbert-base-v4).pt",
        map_location=torch.device("cpu"),
    )
    return abstract_embeddings


if __name__ == "__main__":
    print(thesis_data_upload().head())
