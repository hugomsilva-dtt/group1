from typing import Dict, Any
import pandas as pd
from langchain.agents import AgentExecutor
from langchain.agents.tools import Tool
from langchain_core.agents import Agent
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class ExcelReaderState(BaseModel):
    """State for the Excel reader agent."""
    file_path: str = Field(description="Path to the Excel file")
    current_data: pd.DataFrame = Field(default=None, description="Currently loaded data")
    status: str = Field(default="idle", description="Current status of the agent")
    error: str = Field(default="", description="Error message if any")

class ExcelReaderAgent:
    """Agent responsible for reading and processing Excel files."""
    
    def __init__(self):
        self.state = ExcelReaderState(file_path="")
        
    def read_excel(self, file_path: str) -> Dict[str, Any]:
        """Read an Excel file and store it in the agent's state."""
        try:
            self.state.file_path = file_path
            self.state.current_data = pd.read_excel(file_path)
            self.state.status = "success"
            return {
                "status": "success",
                "message": f"Successfully read Excel file: {file_path}",
                "shape": self.state.current_data.shape
            }
        except Exception as e:
            self.state.status = "error"
            self.state.error = str(e)
            return {
                "status": "error",
                "message": f"Error reading Excel file: {str(e)}"
            }

    def get_columns(self) -> Dict[str, Any]:
        """Get the columns of the loaded Excel file."""
        if self.state.current_data is None:
            return {
                "status": "error",
                "message": "No data loaded. Please read an Excel file first."
            }
        return {
            "status": "success",
            "columns": list(self.state.current_data.columns)
        }

    def get_data_preview(self, rows: int = 5) -> Dict[str, Any]:
        """Get a preview of the loaded data."""
        if self.state.current_data is None:
            return {
                "status": "error",
                "message": "No data loaded. Please read an Excel file first."
            }
        return {
            "status": "success",
            "preview": self.state.current_data.head(rows).to_dict()
        }

    def get_data_info(self) -> Dict[str, Any]:
        """Get information about the loaded data."""
        if self.state.current_data is None:
            return {
                "status": "error",
                "message": "No data loaded. Please read an Excel file first."
            }
        return {
            "status": "success",
            "info": {
                "shape": self.state.current_data.shape,
                "columns": list(self.state.current_data.columns),
                "dtypes": self.state.current_data.dtypes.to_dict()
            }
        }

    def get_tools(self) -> list[Tool]:
        """Get the tools available for this agent."""
        return [
            Tool(
                name="read_excel",
                description="Read an Excel file from the given path",
                func=self.read_excel
            ),
            Tool(
                name="get_columns",
                description="Get the columns of the loaded Excel file",
                func=self.get_columns
            ),
            Tool(
                name="get_data_preview",
                description="Get a preview of the loaded data",
                func=self.get_data_preview
            ),
            Tool(
                name="get_data_info",
                description="Get information about the loaded data",
                func=self.get_data_info
            )
        ]