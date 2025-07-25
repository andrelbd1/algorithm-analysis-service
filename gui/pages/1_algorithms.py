import config
import plotly.express as px
import requests
import streamlit as st

config_app = config.ApplicationConfig()


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

    def __get_executions(self, algorithms, params: dict = {}) -> dict:
        url = r"{endpoint}".format(endpoint=config_app.API_URL["execution"])
        params['amount'] = 1
        params['page'] = 0
        params['execution_status'] = config_app.STATUS_DONE
        params['algorithm_id'] = None
        result = {"total": {}}
        for alg_name, alg_id in algorithms["ids"].items():
            params["algorithm_id"] = alg_id
            request_result = requests.get(url, params=params)
            if request_result.ok:
                result["total"].update({alg_name: request_result.json()['total_items']})
        return result

    def __get_evaluation_report(self, algorithm_id: str, criteria_id: str, input_id: str, params: dict = {}) -> dict:
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

    def __make_report_view(self, report, title):
        if not report:
            return
        unit = report[0].get("unit")
        result = {r['input_value']: r['average'] for r in report}
        fig = px.line(x=result.keys(),
                      y=result.values(),
                      title=title)
        fig.update_traces(hovertemplate='Input: %{x} <br>Average: %{y} '+unit)
        fig.update_layout(xaxis={'title': 'Input'},
                          yaxis={'title': f'Average in {unit}'})
        st.plotly_chart(fig, use_container_width=True)

    def __display(self, algorithms: dict, executions: dict) -> None:
        if "alias" not in st.session_state:
            st.session_state["alias"] = ""
        if "request_date" not in st.session_state:
            st.session_state["request_date"] = ""
        left_col, center_col = st.columns([1, 3], vertical_alignment="top", gap='medium')
        report = []
        with left_col.container(border=True):
            algorithm_selected = st.selectbox("Algorithms", algorithms["ids"].keys())
            lst_inputs = algorithms["inputs"][algorithm_selected].keys()
            input_selected = st.selectbox("Inputs", lst_inputs)
            lst_criteria = algorithms["criteria"][algorithm_selected].keys()
            criteria_selected = st.selectbox("Criteria", lst_criteria)
            filters = {}
            if (alias := st.text_input("Alias", key="alias")):
                filters["alias"] = alias
            if (request_date := st.text_input("Request date", key="request_date")):
                filters["request_date"] = request_date
            _, right_bt = st.columns([2, 1])
            if right_bt.button("Submit", use_container_width=True):
                report = self.__get_evaluation_report(algorithm_id=algorithms['ids'][algorithm_selected],
                                                      criteria_id=algorithms['criteria'][algorithm_selected][criteria_selected],
                                                      input_id=algorithms['inputs'][algorithm_selected][input_selected],
                                                      params=filters)
                executions = self.__get_executions(algorithms, params=filters)

        with center_col.container():
            st.header(f"{algorithm_selected}: {algorithms["description"][algorithm_selected]}")
            left, right = st.columns([1, 3])
            left.write(f"**Total executions:** {executions["total"][algorithm_selected]}")
            right.write(f"Source code: {algorithms["source"][algorithm_selected]}")
            st.divider()
            self.__make_report_view(report, criteria_selected)

    def run(self):
        algorithms: dict = self.__get_algorithms()
        executions: dict = self.__get_executions(algorithms)
        self.__display(algorithms, executions)


ViewAlgorithms().run()
