import streamlit as st


def _set_page_title(page_title: str):
    """
    Set the page title and layout for the Streamlit app.
    """
    st.set_page_config(
        page_title=page_title,
        layout="wide",
    )

    st.title(page_title)
    st.markdown("---")


def _set_navigation():
    with st.sidebar:
        st.header("Navigation")
        st.page_link("app.py", label="Video Subtitle Translator", icon="🏠")
        st.page_link("pages/1_⬆️_Upload.py", label="Upload Video", icon="⬆️")
        st.page_link("pages/2_🎬_Library.py", label="Library", icon="🎬")


def set_page_layout(page_title: str):
    """
    Set the layout for the Streamlit app, including sidebar navigation and page title."""
    _set_page_title(page_title)
    _set_navigation()

    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            This Streamlit frontend demonstrates the capabilities of our PyPI translation package installable via
            ```pip install easy-nlp-translate```."""
        )
        st.markdown(
            """
            Further description of the app. This is a placeholder for the further description of the app that will be displayed in the sidebar.
            """
        )
        st.caption(
            """
            Developed by *Philipp Meyer, Ole Schildt & Kevin Schäfer* as part of the **Natural Language Processing** course, taught by *Raffael Veser*.
            """
        )
