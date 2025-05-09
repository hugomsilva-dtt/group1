import pytest
from src.agents.excel_reader_agent import ExcelReaderAgent
import pandas as pd
import os

@pytest.fixture
def excel_reader_agent():
    return ExcelReaderAgent()

def test_excel_reader_initialization(excel_reader_agent):
    assert excel_reader_agent.state.file_path == ""
    assert excel_reader_agent.state.current_data is None
    assert excel_reader_agent.state.status == "idle"
    assert excel_reader_agent.state.error == ""

def test_excel_reader_tools(excel_reader_agent):
    tools = excel_reader_agent.get_tools()
    assert len(tools) == 4
    tool_names = [tool.name for tool in tools]
    assert "read_excel" in tool_names
    assert "get_columns" in tool_names
    assert "get_data_preview" in tool_names
    assert "get_data_info" in tool_names

def test_excel_reader_no_data(excel_reader_agent):
    result = excel_reader_agent.get_columns()
    assert result["status"] == "error"
    assert "No data loaded" in result["message"]