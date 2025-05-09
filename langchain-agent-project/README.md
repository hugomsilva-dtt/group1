# langchain-agent-project/README.md

# LangChain Agent Project

This project implements a multi-agent scenario using LangGraph and LangChain. The primary focus is on reading datasets from Excel files and processing them through various agents.

## Project Structure

```
langchain-agent-project
├── src
│   ├── agents
│   │   ├── excel_reader_agent.py
│   │   └── __init__.py
│   ├── config
│   │   └── settings.py
│   ├── graphs
│   │   └── workflow.py
│   ├── main.py
│   ├── schema
│   │   └── models.py
│   └── utils
│       └── helpers.py
├── tests
│   ├── __init__.py
│   └── test_excel_reader.py
├── requirements.txt
├── .env
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd langchain-agent-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your environment variables in the `.env` file.

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Agents

- **ExcelReaderAgent**: Responsible for reading datasets from Excel files. It includes methods for loading and processing data.

## Workflows

The project defines workflows that manage the interactions between different agents, ensuring a smooth data processing pipeline.

## Testing

Unit tests are provided in the `tests` directory. To run the tests, use:
```
pytest tests
```

## License

This project is licensed under the MIT License.