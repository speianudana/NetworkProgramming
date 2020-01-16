import csv
import json
import requests
import xmltodict
import yaml
import Constants
from Thread import RequestThread


def request_server_result():
    # getting the access token
    response = requests.get(Constants.MAIN_URL + Constants.REGISTER)
    json_str = response.content.decode("utf8")
    json_dict = json.loads(json_str)
    token = json_dict[Constants.ACCESS_TOKEN]
    paths = requests.get(Constants.MAIN_URL + Constants.HOME, headers={Constants.HEADER_LABEL: token})
    # parsing result to extract first routes
    path_links_row_data = json.loads(paths.content.decode("utf8"))
    print(path_links_row_data[Constants.MESSAGE])
    # extracting list of first routes
    link_list = path_links_row_data[Constants.LINK]
    # variable to save final result
    results = dict()
    # list of threads to parse first routes
    threads = []

    # starting threads with first routes
    for key in link_list:
        url = Constants.MAIN_URL + link_list[key]
        # print(url)
        thread = RequestThread(key, url, token)
        threads.append(thread)
        thread.start()
    for thread in threads:
        results.update(thread.join())

    return results


def parse_result(results, query):
    merged_data = []
    for key, result in results.items():
        row_data = json.loads(result)  # converts the string in json format
        if Constants.MIME_TYPE in row_data:
            if row_data[Constants.MIME_TYPE] == Constants.MIME_TYPE_XML:
                xml_data = row_data[Constants.DATA_VALUE]
                loads = json.loads(json.dumps(xmltodict.parse(xml_data, process_namespaces=True)))
                merged_data.append(loads[Constants.DATA_SET_VALUE][Constants.RECORD_VALUE])

            elif row_data[Constants.MIME_TYPE] == Constants.MIME_TYPE_CSV:
                csv_data = row_data[Constants.DATA_VALUE]
                reader = csv.DictReader(csv_data.split('\n'), delimiter=',')
                merged_data.append(json.loads(json.dumps([row for row in reader])))

            elif row_data[Constants.MIME_TYPE] == Constants.MIME_TYPE_YAMLE:
                yamle_data = row_data[Constants.DATA_VALUE]
                merged_data.append(json.loads(json.dumps(yaml.safe_load(yamle_data))))
        else:
            # fixed malformed json format received from server
            if ',]' in row_data[Constants.DATA_VALUE]:
                replace = str(row_data[Constants.DATA_VALUE]).replace(',]', ']')
                merged_data.append(json.loads(replace))
            else:
                merged_data.append(json.loads(row_data[Constants.DATA_VALUE]))

    if Constants.SELECT_COLUMN_VALUE in query:
        query_values = query.replace(Constants.SELECT_COLUMN_VALUE, '').split()
        query_result = []
        for element in merged_data:
            for row in element:
                result_row = dict()
                for query in query_values:
                    if query in row:
                        result_row[query] = row[query]
                if result_row:
                    query_result.append(result_row)
        # transforms from list of dictionaries into json string
        return json.dumps(query_result)
    else:
        # if there is no query all the data is returned
        return json.dumps(merged_data)
