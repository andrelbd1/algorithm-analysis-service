import config
import requests
import streamlit as st


config_app = config.ApplicationConfig()
# st.title(":computer: Algorithms")


class ViewAlgorithms:

    def __get_algorithms(self) -> dict:
        url = r"{endpoint}".format(endpoint=config_app.API_URL["algorithm"])
        params = {
            "amount": 100,
            "page": 0
        }
        request_result = requests.get(url, params=params)
        if request_result.ok:
            lst_algorithm = request_result.json()['algorithms']
            result = {"ids": {}, "inputs": {}, "source": {}, "description": {}, "criteria": {}}
            for a in lst_algorithm:
                result_ids, result_inputs, result_criteria = {}, {}, {}
                result_source, result_description = {}, {}
                input_dct = {i["name"]: i['input_id'] for i in a['input']}
                criteria_dct = {c["name"]: c['criteria_id'] for c in a['criteria']}
                result_ids[a['name']] = a['algorithm_id']
                result_inputs[a['name']] = input_dct
                result_criteria[a['name']] = criteria_dct
                result_source[a['name']] = a['source']
                result_description[a['name']] = a['description']
                result["ids"].update(result_ids)
                result["inputs"].update(result_inputs)
                result["criteria"].update(result_criteria)
                result["source"].update(result_source)
                result["description"].update(result_description)
            return result
        st.error("Failed to fetch algorithms")

    def __get_executions(self, algorithms) -> dict:
        url = r"{endpoint}".format(endpoint=config_app.API_URL["execution"])
        params = {
            "amount": 1,
            "page": 0,
            "execution_status": config_app.STATUS_DONE,
            "algorithm_id": None,
        }
        result = {"total": {}}
        for alg_name, alg_id in algorithms["ids"].items():
            params["algorithm_id"] = alg_id
            request_result = requests.get(url, params=params)
            if request_result.ok:
                result["total"].update({alg_name: request_result.json()['total_items']})
        return result

    def __get_evaluation_report(self, algorithm_id: str, criteria_id: str, input_id: str, params: str) -> dict:
        url = r"{endpoint}/evaluation-report/algorithm/{algorithm_id}/criteria/{criteria_id}/input/{input_id}".format(
                    endpoint=config_app.API_URL["result"],
                    algorithm_id=algorithm_id,
                    criteria_id=criteria_id,
                    input_id=input_id
                )
        params['amount'] = 100
        params['page'] = 0
        result = []
        while True:
            request_result = requests.get(url, params=params)
            if request_result.ok and request_result.json()['report']:
                result.extend(request_result.json()['report'])
                params['page'] += 1
                continue
            break
        return result

    def __display(self, algorithms: dict, executions: dict) -> None:
        left, center = st.columns([1, 3], vertical_alignment="top", gap='medium')
        report = []
        with left.container(border=True):
            algorithm_selected = st.selectbox("Algorithms", algorithms["ids"].keys())
            lst_inputs = algorithms["inputs"][algorithm_selected].keys()
            input_selected = st.selectbox("Inputs", lst_inputs)
            lst_criteria = algorithms["criteria"][algorithm_selected].keys()
            criteria_selected = st.selectbox("Criteria", lst_criteria)
            filters = {}
            if (alias := st.text_input("Alias")):
                filters["alias"] = alias
            if (request_date := st.text_input("Request date")):
                filters["request_date"] = request_date
            _, right = st.columns([2, 1])
            if right.button("Submit", use_container_width=True):
                report = self.__get_evaluation_report(algorithm_id=algorithms['ids'][algorithm_selected],
                                                      criteria_id=algorithms['criteria'][algorithm_selected][criteria_selected],
                                                      input_id=algorithms['inputs'][algorithm_selected][input_selected],
                                                      params=filters)
        with center.container():
            st.header(f"{algorithm_selected}: {algorithms["description"][algorithm_selected]}")
            left, right = st.columns([1, 3])
            left.write(f"**Total executions:** {executions["total"][algorithm_selected]}")
            right.write(f"Source code: {algorithms["source"][algorithm_selected]}", use_container_width=True)
            st.divider()
            print(f"{report=}")
            print(f"{len(report)=}")

    def run(self):
        algorithms: dict = self.__get_algorithms()
        executions: dict = self.__get_executions(algorithms)
        # print(algorithms)
        self.__display(algorithms, executions)


ViewAlgorithms().run()
