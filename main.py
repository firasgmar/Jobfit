import streamlit as st
import pages.search as search
import pages.upload as upload

PAGES = {
    "Search CV": search,
    "Upload New CV": upload
}
st.set_page_config(layout="wide")
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()


