import requests
from bs4 import BeautifulSoup as bs


def get_thesis_data(thesis_id):
    """Takes the thesis ID (as in the Ethos database)
    and returns the thesis title and abstract as a dictionary
    Args:
        thesis_id (str): the Ethos thesis URL
    """
    thesis_link = (
        "https://ethos.bl.uk/OrderDetails.do?did=5&uin=uk.bl.ethos."
        + thesis_id
    )
    with requests.Session() as s:
        page = s.get(
            thesis_link,
            headers={
                "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;"
                + " rv:50.0) Gecko/20100101 Firefox/50.0"
            },
        )
        soup = bs(page.content, "html.parser")
        # print(soup.prettify)
        result = soup.find("td", class_="historytitle")
        title = result.get_text().strip()

        all_trs = list(map(lambda x: x.text.strip(), soup.find_all("tr")))
        # print(all_trs)
        abstract_index = all_trs.index("Abstract:") + 1
        abstract = all_trs[abstract_index]

        paper_data = {"Title": title, "Abstract": abstract}
        return paper_data


if __name__ == "__main__":
    test_id = "232781"
    result = get_thesis_data(test_id)
    print(
        "TITLE:\n",
        result["Title"],
        "\n\n\n",
        "ABSTRACT:\n",
        result["Abstract"],
    )
