# RAG-GW Project

## Overview
The RAG-GW project is a Python-based application designed to analyze and evaluate documents for compliance with governance, strategy, HR, finance, IT/data, risk & audit, ESG, and stakeholder management frameworks. It uses advanced AI models and vector databases to provide insights and recommendations.

## Features
- **Document Loading**: Load and process text documents for analysis.
- **Text Splitting**: Split documents into manageable chunks for efficient processing.
- **Vector Storage**: Store document embeddings in a Qdrant vector database.
- **AI Analysis**: Use Azure OpenAI and Google Generative AI for document evaluation.
- **Compliance Scoring**: Evaluate documents for compliance with governance frameworks.

## Project Structure
```
rag-gw/
├── connect_db.py          # Handles database connection and collection creation
├── document_loader.py     # Loads and processes documents
├── main_real.py           # Main application logic and agent setup
├── text_chunk.py          # Splits text and interacts with the vector database
├── documents/             # Directory for storing input documents
│   └── Executive_Governance_90.txt
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-gw
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=<your-google-api-key>
AZURE_OPENAI_API_KEY=<your-azure-api-key>
AZURE_OPENAI_ENDPOINT=<your-azure-endpoint>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
AZURE_OPENAI_API_VERSION=<your-api-version>
```

## Usage
1. Load documents into the `documents/` directory.
2. Run the main application:
   ```bash
   python main_real.py
   ```
3. Follow the prompts to analyze documents.

## Dependencies
- `python-dotenv`
- `langchain`
- `langchain-community`
- `langchain-google-genai`
- `langchain-openai`
- `qdrant-client`
- `langchain-qdrant`

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [LangChain](https://github.com/hwchase17/langchain)
- [Qdrant](https://qdrant.tech/)
- [Azure OpenAI](https://azure.microsoft.com/en-us/services/openai/)
