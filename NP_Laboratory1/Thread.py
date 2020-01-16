import threading
import requests
import json

import Constants


class RequestThread(threading.Thread):
    # constructor that contains route_id - route name, path to the route, token - access token to the server
    def __init__(self, route_id, path, token):
        threading.Thread.__init__(self)
        self.route_id = route_id
        self.path = path
        self.token = token
        # self.response = []
        # list of child threads
        self.threads = []
        # dictionary where final result is saved
        self.current_results = dict()

    def run(self):
        # calling the server to get data from a route
        response = requests.get(self.path, headers={Constants.HEADER_LABEL: self.token}).content.decode("utf8")
        parsing_value = json.loads(response)
        # save the result from first request in current_results dictionary
        self.current_results.update({self.route_id: response})
        # parse the results to extract next routes
        if Constants.LINK in parsing_value:
            route = parsing_value[Constants.LINK]
            for key, value in route.items():
                # a route was found and starting a new thread
                thread = RequestThread(key, Constants.MAIN_URL + value, self.token)
                # saving the thread in the list of threads
                self.threads.append(thread)
                # starting thread with next route
                thread.start()

        for thread in self.threads:
            # waiting for child thread to execute and save the result in current_result dictionary
            self.current_results.update(thread.join())

    def join(self, *args):
        threading.Thread.join(self)
        # returning the results from thread execution
        return self.current_results
