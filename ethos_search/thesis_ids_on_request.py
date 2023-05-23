from bs4 import BeautifulSoup as bs
import mechanize
import ssl
import re


def get_thesis_ids(page_to_process):
    """Receives a Beatifulsoup object
    and returns a list of thesis ids as a list
    Args:
        page_to_process (BS object): Ethos page a BS object
    """
    links = page_to_process.find_all("a", class_="title ui-button-text")
    list_of_ids = []
    for j in links:
        list_of_ids.append(re.findall(r"\d+", j.get("href"))[1])
    return list_of_ids


def process_request_to_get_ids(user_request):
    """Recieves a user query and returns a list of the thesis
    ids from Ethos

    Args:
        user_request (string): a user query to Ethos
    """
    ethos_url = "https://ethos.bl.uk/"
    ssl._create_default_https_context = ssl._create_unverified_context

    # preparation and sending the request
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_header(
        "User-agent",
        value="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0)"
        + " Gecko/20100101 Firefox/50.0",
    )
    br.open(ethos_url)
    br.select_form(name="searchForm")
    br["query"] = user_request
    response = br.submit()

    # get the first page of the response
    soup = bs(response.read(), "html.parser")

    # get the total number of records
    records_number = soup.find_all("h1")
    records_number = int(re.findall(r"\d+", records_number[1].text)[0])
    print(f"The total number of records found is {records_number}")

    # gets the total number of pages
    pages_number = soup.find_all("span", class_="no-link")
    pages_number = int((re.findall(r"\d+", pages_number[2].text)[0]))
    print(f"There {pages_number} pages overall")

    # get the ids from the 1st page
    thesis_ids = get_thesis_ids(soup)
    # print(f"The thesis ids from the first page are {thesis_ids}")

    # first we prepare a base link
    if pages_number > 1:
        links = soup.find_all("a")
        for i in links:
            test = i.get("href")
            if test[1:4] == "Pro":
                base_link = test
                break

        first_part_of_the_link = (
            "https://ethos.bl.uk/ProcessSearchUpdate.do?page="
        )
        second_part_of_the_link = base_link.split("time=")[1]
        # print(first_part_of_the_link, second_part_of_the_link)
    else:
        base_link = None
    if not base_link:
        return thesis_ids

    for i in range(2, pages_number + 1):
        rolling_link = (
            first_part_of_the_link
            + str(i)
            + "&time="
            + second_part_of_the_link
        )
        br.open(rolling_link)
        soup = bs(br.response(), "html.parser")
        thesis_ids += get_thesis_ids(soup)
    return thesis_ids


if __name__ == "__main__":
    query = "non-linear ultrasound test"
    result = process_request_to_get_ids(query)
    print(result, len(result))
