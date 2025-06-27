import os
import streamlit as st
from dotenv import load_dotenv


# st.set_page_config(layout="wide", initial_sidebar_state="expanded")
class ApplicationConfig:

    load_dotenv(override=True)

    st.set_page_config(
        page_title="Algorithm Analysis Service",
        page_icon=":computer:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    API_HOST = os.environ.get("API_HOST", "127.0.0.1")
    API_PORT = os.environ.get("PORT_API", 8000)
    API_URL = {
        "algorithm": f"http://{API_HOST}:{API_PORT}/v1/algorithm",
        "execution": f"http://{API_HOST}:{API_PORT}/v1/execution",
        "result": f"http://{API_HOST}:{API_PORT}/v1/result",
    }

    STATUS_DONE = 'DONE'
    STATUS_ERROR = 'ERROR'
    STATUS_PROCESSING = 'PROCESSING'
    STATUS_QUEUE = "QUEUE"
    STATUS_WARNING = 'WARNING'
