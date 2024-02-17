## Overview

This multiagent chatbot leverages the capabilities of large language models and the LangChain library to showcase the use of multiple agents.

The bot is integrated into a user-friendly interface created with Streamlit, allowing users to interact with the AI in real time.

## Types of Agents

1. The User Proxy Agent acts as the mediator between the customer's inquiries and the specific functions of the Guardrail and Scheduler agents. It interprets user input and decides which agent should handle the request based on the content of the inquiry.

2. The Guardrail Agent is implemented to specifically handle inquiries for "post renovation cleaning" or any service currently outside the company's offerings.

3. The Scheduler Agent is responsible for handling specific inquiries related to scheduling a service and providing pricing information. It achieves this by retrieving data from external sources such as APIs and PDF documents via RAG.

## Features

- **Dynamic Interaction**: Streamlit interface allows for real-time interaction with the bot, making it more engaging and responsive.

- **Conversation Management**: Allows users to create, delete, and switch between different conversation threads. This feature will enable users to separate topics and maintain organised discussions. Each conversation thread could be named or tagged for easy identification.

- **Private Session**: Own your conversations from other users! Create, delete and download any conversations with ease.

## Installation

Try the streamlit [here](https://multiagentchatbot.streamlit.app/).

Access the API endpoint [here](https://multiagent-api-e1c2b87287a3.herokuapp.com/).

Access the API Documentations [here](https://multiagent-api-e1c2b87287a3.herokuapp.com/docs).

If you want to try it out and modify it:

1. Clone the Repository

```bash
git clone https://github.com/timooo-thy/multiagent-chatbot
```

2. Install Dependencies
   Ensure you have Python installed, and then run:

```bash
pip install -r requirements.txt
```

3. Launch the App
   Navigate to the app's directory and run:

```bash
streamlit run cleaningCompanyChat.py
```

## Usage

**Login**: Enter your Huggingface credentials at the sidebar.

**Start Chatting**: Simply type your query or message in the input field and press Enter.

**Manage Sessions**: Start new sessions or review past conversations for reference.

**Download Conversations**: Download the transcript of your current or past conversations for record-keeping.

## Acknowledgements

- Streamlit for providing an intuitive app-building framework.

- Langchain for retrieval augmented generation.

- OpenAI for text embeddings.

- FAISS for vector store and similarity search.

## License

[MIT](https://opensource.org/license/mit/)
