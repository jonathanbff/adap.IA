# Adap.AI API

Adap.AI is an adaptive educational microservice API built with FastAPI. It provides interactive tools for learning, including word search generation, mind map creation, flashcard generation, and conversational assistant responses. Additionally, Adap.AI integrates a video creation API, enabling users to create customized educational videos.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Available Endpoints](#available-endpoints)
  - [Root](#get-)
  - [Health Check](#get-health)
  - [Generate Word Search](#post-generate-word-search)
  - [Generate Mind Map](#post-generate-mind-map)
  - [Generate Flashcards](#post-generate-flashcards)
  - [Send Message to Assistant](#post-send-message)
  - [Clear Conversation History](#post-clear-history)
  - [Video Creation API Integration](#video-creation-api-integration)
- [Video Creation API Documentation](#video-creation-api-documentation)
- [License](#license)

---

## Overview

Adap.AI offers a suite of adaptive educational tools, helping users engage in structured, interactive learning. This API now leverages OpenAI's ChatGPT models to deliver intelligent responses and customized educational resources.

## Installation

To install and run this API:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/adap-ai
   cd adap-ai
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

## Environment Setup

Ensure you set up the `OPENAI_API_KEY` environment variable in a `.env` file:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

## Available Endpoints

---

### **GET `/`**

- **Description**: Root endpoint that returns a welcome message.
- **Response**: `{"message": "Hello World"}`

---

### **GET `/health`**

- **Description**: Health check endpoint.
- **Response**: `{"status": "healthy"}`

---

### **POST `/generate-word-search`**

- **Description**: Generates a word search puzzle based on a topic.
- **Request Body**:
  - `topic` (str): The topic for generating word search words.
- **Response**: JSON with the word search grid and word coordinates.
- **Error**: 400 if generation fails.

---

### **POST `/generate-mind-map`**

- **Description**: Generates a mind map for a subject.
- **Request Body**:
  - `subject` (str): The topic for the mind map.
- **Response**: JSON-format mind map.
- **Error**: 400 if generation fails.

---

### **POST `/generate-flashcards`**

- **Description**: Generates flashcards based on a subject and specified quantity.
- **Request Body**:
  - `subject` (str): Subject of the flashcards.
  - `num_flashcards` (int, optional): Number of flashcards, default is 5.
- **Response**: JSON with generated flashcards.
- **Error**: 400 if generation fails.

---

### **POST `/send-message`**

- **Description**: Sends a user message to the educational assistant and receives a response.
- **Request Body**:
  - `message` (str): The message from the user.
  - `temperature` (float, optional): Controls response creativity, default is 1.0.
  - `max_tokens` (int, optional): Maximum tokens in response, default is 1024.
- **Response**: JSON with the assistant’s response.
- **Error**: 500 if response generation fails.

---

### **POST `/clear-history`**

- **Description**: Clears the assistant's conversation history.
- **Response**: `{"message": "Histórico de conversação limpo com sucesso."}`

---

### **Video Creation API Integration**

The Adap.AI API integrates with a video creation API, allowing users to generate custom educational videos. The API for video creation can be found [here](https://github.com/well2632/hackmetabacknode). Refer to the documentation in this GitHub repository for setup instructions and endpoint specifications.

---

## Video Creation API Documentation

Please refer to the official documentation for the video creation API in the [GitHub repository](https://github.com/well2632/hackmetabacknode) to understand the parameters, setup, and detailed endpoint descriptions for video generation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
