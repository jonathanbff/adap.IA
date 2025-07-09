### Documentation for `Adap.AI` API -- back-end

This API offers adaptive educational tools and resources, including word search generation, mind map creation, flashcard creation, and interactive assistant messaging. It’s built with FastAPI and now integrates the OpenAI API for AI-powered responses.

---

#### **Classes and Endpoints Overview**

---

#### **1. WordSearchGenerator**

Generates a word search puzzle with words related to a provided topic.

- **Methods**:
  - `create_agent`: Initializes an OpenAI client to create responses based on initial messages.
  - `get_words_from_agent`: Fetches 10 words related to a specified topic.
  - `place_word_in_grid`: Randomly places words in a 10x10 grid.
  - `generate_word_search`: Generates the puzzle and populates the grid with random letters.

#### **2. MindMapGenerator**

Generates a mind map structure for a given subject.

- **Methods**:
  - `create_agent`: Initializes an OpenAI client with a role to facilitate structured responses.
  - `generate_mind_map`: Generates a JSON-format mind map for a given subject.

#### **3. FlashcardGenerator**

Creates custom flashcards on a specified topic.

- **Methods**:
  - `create_agent`: Generates structured flashcard responses through an OpenAI client.
  - `create_flashcards`: Produces flashcards with key fields in JSON.

#### **4. EducationalAssistant**

Simulates an interactive educational assistant, responding in the user's preferred language.

- **Methods**:
  - `send_message`: Sends a user’s message to the assistant and returns a structured response.
  - `clear_history`: Clears conversation history, retaining only the initial system message.

---

#### **API Endpoints**

---

- **GET `/`**
  - **Description**: Root endpoint; returns a greeting.
  - **Response**: `{"message": "Hello World"}`

- **GET `/health`**
  - **Description**: Health check endpoint.
  - **Response**: `{"status": "healthy"}`

---

#### **POST `/generate-word-search`**

- **Description**: Generates a word search puzzle based on a topic.
- **Request Body**: JSON with the field:
  - `topic` (str): Topic for generating word search words.
- **Response**: A JSON object with the grid and answers.
- **Error**: 400 if generation fails.

---

#### **POST `/generate-mind-map`**

- **Description**: Generates a mind map for a subject.
- **Request Body**: JSON with the field:
  - `subject` (str): Topic for the mind map.
- **Response**: JSON-formatted mind map.
- **Error**: 400 if generation fails.

---

#### **POST `/generate-flashcards`**

- **Description**: Generates flashcards based on a subject and specified quantity.
- **Request Body**: JSON with fields:
  - `subject` (str): Subject of the flashcards.
  - `num_flashcards` (int, optional): Number of flashcards, default is 5.
- **Response**: JSON with generated flashcards.
- **Error**: 400 if generation fails.

---

#### **POST `/send-message`**

- **Description**: Sends a user message to the educational assistant and receives a response.
- **Request Body**: JSON with fields:
  - `message` (str): User message to the assistant.
  - `temperature` (float, optional): Controls response creativity, default 1.0.
  - `max_tokens` (int, optional): Maximum tokens in response, default 1024.
- **Response**: JSON with the assistant’s response.
- **Error**: 500 if response generation fails.

---

#### **POST `/clear-history`**

- **Description**: Clears the assistant's conversation history.
- **Response**: `{"message": "Histórico de conversação limpo com sucesso."}`

---

This documentation serves as a comprehensive guide for developers and users interacting with the `Adap.AI` API to manage various educational resources.
