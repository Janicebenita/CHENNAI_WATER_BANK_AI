"""Chennai Water Bank Streamlit entry point."""

import streamlit as st

from src.ui.command_center import render_command_center
from src.ui.theme import configure_page, render_sidebar_context


configure_page("Command Center")
render_sidebar_context()
st.markdown(
    "### [🌍 PROBLEM 2.3 — WATER CONSERVATION PRIORITY MAP](./water_conservation_priority_map)"
)
render_command_center()
