import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(
    page_title="This is a demopage for the PyPi package ```easy-nlp-translate``` to be found at https://easy-nlp-translate.de/",
)

st.write(
    "Further information and docs about the package can be found under the following link: [easy-nlp-translate](https://easy-nlp-translate.de/)"
)
st.image("src/images/pypi_package.png")
