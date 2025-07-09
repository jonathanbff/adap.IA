from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union, Optional, Any, TypedDict, Literal
from openai import OpenAI, OpenAIError
import random
import json
import os
import re
from dotenv import load_dotenv
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)

load_dotenv()

# Define our own type hints for messages
class ChatMessage(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str
    name: Optional[str]

app = FastAPI(
    title="Adap.AI",
    description="Adaptative AI Microservice with FastAPI",
    version="0.1.0"
)

class WordSearchGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def create_agent(self, role_name, initial_message):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": initial_message}],
            temperature=0.5,
            max_tokens=512,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response += content
        return response

    def get_words_from_agent(self, topic, max_attempts=3):
        for attempt in range(max_attempts):
            message = (
                f"Retorne exatamente 10 palavras curtas relacionadas ao tópico '{topic}', "
                "no formato JSON e sem nenhum texto adicional. A resposta deve estar neste formato:\n"
                "[\"palavra1\", \"palavra2\", \"palavra3\", ...]"
            )
            response = self.create_agent("Word Generator", message)
            try:
                words = json.loads(response)
                if isinstance(words, list) and len(words) == 10 and all(isinstance(word, str) for word in words):
                    return [word.strip().upper() for word in words]
            except json.JSONDecodeError:
                continue
        return []

    def place_word_in_grid(self, grid, word):
        max_rows, max_cols = len(grid), len(grid[0])
        word_len = len(word)
        for _ in range(100):
            start_row = random.randint(0, max_rows - 1)
            start_col = random.randint(0, max_cols - 1)
            direction = random.choice([(0, 1), (1, 0), (1, 1)])
            end_row = start_row + (word_len - 1) * direction[0]
            end_col = start_col + (word_len - 1) * direction[1]
            if 0 <= end_row < max_rows and 0 <= end_col < max_cols:
                if all(grid[start_row + i * direction[0]][start_col + i * direction[1]] in ("", word[i]) for i in range(word_len)):
                    for i in range(word_len):
                        grid[start_row + i * direction[0]][start_col + i * direction[1]] = word[i]
                    return {
                        "word": word,
                        "start": [start_row, start_col],
                        "end": [end_row, end_col]
                    }
        return None

    def generate_word_search(self, topic):
        words = self.get_words_from_agent(topic)
        if not words:
            return None
        grid = [["" for _ in range(10)] for _ in range(10)]
        answers = []
        for word in words:
            result = self.place_word_in_grid(grid, word)
            if result:
                answers.append(result)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for row in range(10):
            for col in range(10):
                if grid[row][col] == "":
                    grid[row][col] = random.choice(alphabet)
        return {
            "grid": grid,
            "answers": answers
        }

class MindMapGenerator:
    def __init__(self, api_key: str):
        """
        Inicializa a instância da classe MindMapGenerator.

        Parâmetros:
            api_key (str): A chave de API para autenticação no OpenAI.
        """
        self.client = OpenAI(api_key=api_key)

    def create_agent(self, role_name: str, initial_message: str) -> str:
        """
        Cria um agente no OpenAI e obtém a resposta completa para uma mensagem inicial.

        Parâmetros:
            role_name (str): O nome do papel do agente para o contexto da mensagem.
            initial_message (str): A mensagem inicial enviada ao agente.

        Retorna:
            str: A resposta completa do agente em formato de string.
        """
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": initial_message}],
            temperature=0.5,
            max_tokens=1512,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response += content
        return response

    def generate_mind_map(self, subject: str) -> Optional[Dict[str, Any]]:
        """
        Gera um mapa mental para o assunto fornecido.

        Parâmetros:
            subject (str): O assunto para o qual o mapa mental será gerado.

        Retorna:
            dict: Dicionário representando o mapa mental em formato JSON.
                  Retorna None se não for possível gerar um JSON válido.
        """
        message = (
            f"Create a mind map for the subject '{subject}' in the following JSON format. "
            "It should include nodes and edges. Each node should have fields 'id', 'label', 'type', and 'parent'. "
            "The 'type' should be 'general_subject' for the main topic, 'category' for high-level branches, "
            "and 'sub_category' for subtopics under each category. Each edge should connect a source node to a target node.\n"
            "Example format:\n\n"
            "{\n"
            "  \"general_subject\": \"{subject}\",\n"
            "  \"nodes\": [\n"
            "    {\"id\": \"1\", \"label\": \"{subject}\", \"type\": \"general_subject\"},\n"
            "    {\"id\": \"2\", \"label\": \"Category 1\", \"type\": \"category\", \"parent\": \"1\"},\n"
            "    {\"id\": \"3\", \"label\": \"Subcategory 1\", \"type\": \"sub_category\", \"parent\": \"2\"}\n"
            "  ],\n"
            "  \"edges\": [\n"
            "    {\"source\": \"1\", \"target\": \"2\"},\n"
            "    {\"source\": \"2\", \"target\": \"3\"}\n"
            "  ]\n"
            "}\n"
            "Please use this format and only output valid JSON. Don't write anything after"
        )

        response = self.create_agent("Mind Map Generator", message.replace("{subject}", subject))

        try:
            mind_map_data = json.loads(response)
            return mind_map_data
        except json.JSONDecodeError:
            print("Erro: A resposta da IA não está em formato JSON válido.")
            return None

class FlashcardGenerator:
    """
    Classe para gerar flashcards personalizados para um assunto fornecido,
    utilizando a API do OpenAI para obter os dados dos flashcards.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def clean_response(self, response: str) -> str:
        """
        Limpa a resposta da IA corrigindo problemas comuns, como aspas duplicadas no campo "id".

        Parâmetros:
            response (str): A resposta em formato de string JSON gerada pela IA.

        Retorna:
            str: A resposta limpa e pronta para decodificaço JSON.
        """
        response = re.sub(r'"id": (\d+)",', r'"id": \1,', response)
        return response

    def create_agent(self, role_name: str, initial_message: str) -> str:
        """
        Cria um agente no OpenAI e obtém a resposta completa para uma mensagem inicial.

        Parâmetros:
            role_name (str): O nome do papel do agente para o contexto da mensagem.
            initial_message (str): A mensagem inicial enviada ao agente.

        Retorna:
            str: A resposta completa do agente em formato de string.
        """
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": initial_message}],
            temperature=0.5,
            max_tokens=2000,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response += content
        return response

    def create_flashcards(self, subject: str, num_flashcards: int = 5) -> Optional[Dict[str, Any]]:
        """
        Gera flashcards para o assunto fornecido em formato JSON.

        Parâmetros:
            subject (str): O assunto para o qual os flashcards serão gerados.
            num_flashcards (int): Número de flashcards desejados.

        Retorna:
            dict: Dicionário representando os flashcards em formato JSON.
                  Retorna None se não for possível gerar um JSON válido.
        """
        message = (
            f"Crie {num_flashcards} flashcards para o assunto '{subject}' no formato JSON, sem introduções ou explicações adicionais. "
            "A resposta deve estar neste exato formato, com uma lista de flashcards, cada um contendo: 'id' (número sem aspas), 'front', 'back', 'category', "
            "'difficulty', 'tags', e 'image'. O JSON deve começar diretamente sem qualquer introdução:\n\n"
            "{\n"
            f"  \"general_subject\": \"{subject}\",\n"
            "  \"flashcards\": [\n"
            "    {\n"
            "      \"id\": 1,\n"
            "      \"front\": \"Pergunta do flashcard\",\n"
            "      \"back\": \"Resposta do flashcard\",\n"
            "      \"category\": \"Categoria\",\n"
            "      \"difficulty\": \"Nível de dificuldade\",\n"
            "      \"tags\": [\"tag1\", \"tag2\"],\n"
            "      \"image\": \"[Inserir URL de uma imagem relevante aqui]\"\n"
            "    },\n"
            "    {...}\n"
            "  ]\n"
            "}"
        )

        response = self.create_agent("Flashcard Generator", message.replace("{subject}", subject))

        try:
            response = self.clean_response(response)

            if '"general_subject"' not in response:
                response = f'{{"general_subject": "{subject}", "flashcards": {response}}}'

            flashcard_data = json.loads(response)
            return flashcard_data
        except json.JSONDecodeError as e:
            print("Erro ao decodificar JSON:", e)
            return None

class WordSearchRequest(BaseModel):
    topic: str

class MindMapRequest(BaseModel):
    subject: str

class FlashcardRequest(BaseModel):
    subject: str
    num_flashcards: int = 5

class EducationalAssistant:
    """
    Classe para criar uma interação de assistente educacional com a API OpenAI.
    Permite ao usuário enviar mensagens em texto e receber respostas interativas.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Inicializa a instância da classe EducationalAssistant.
        
        Parâmetros:
            api_key (str): Chave de API para autenticação no OpenAI.
            model (str): O modelo usado para gerar respostas (padrão: gpt-3.5-turbo).
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history: List[ChatMessage] = []
        
        # Add system message to define AI's behavior with multilingual support
        system_message: ChatMessage = {
            "role": "system",
            "content": """You are Adapt AI, an educational assistant focused on helping students learn and understand academic subjects.

Key characteristics:
- Always respond in the same language the user is using
- You are friendly, patient, and encouraging
- You explain concepts in clear, simple terms
- You use examples and analogies to make learning easier
- You stay focused on educational topics
- You politely decline to discuss non-educational topics
- You maintain a professional and supportive tone

Language Guidelines:
1. Detect the language of the user's message and respond in the same language
2. Keep the same language throughout the conversation until the user switches languages
3. For Portuguese users: Use Brazilian Portuguese (pt-BR)
4. For Spanish users: Use Latin American Spanish
5. Maintain formal but friendly tone in all languages

Content Guidelines:
1. If asked about non-educational topics, respond in the user's language with: 
   (EN) "I'm Adapt AI, focused on helping you learn. Could we discuss educational topics instead?"
   (PT) "Sou a Adapt AI, focada em ajudar você a aprender. Podemos discutir tópicos educacionais?"
   (ES) "Soy Adapt AI, enfocada en ayudarte a aprender. ¿Podemos discutir temas educativos?"
2. For educational questions, provide structured, clear explanations
3. When appropriate, suggest related topics to explore
4. Use encouraging language to motivate learning
5. If a concept is complex, break it down into simpler parts
6. Always verify understanding and offer to clarify if needed

Remember: Your primary goal is to facilitate learning and understanding in the user's preferred language.""",
            "name": None
        }
        self.conversation_history.append(system_message)

    def send_message(self, user_message: str, temperature: float = 1.0, max_tokens: int = 1024) -> str:
        """
        Envia uma mensagem do usuário para a API e retorna a resposta.
        
        Parâmetros:
            user_message (str): Mensagem enviada pelo usuário.
            temperature (float): Controle da criatividade da resposta (0 a 1).
            max_tokens (int): Número máximo de tokens na resposta.
        
        Retorna:
            str: A resposta gerada pelo assistente.
        """
        # Create message with correct type
        user_message_param: ChatMessage = {
            "role": "user",
            "content": user_message,
            "name": None
        }
        self.conversation_history.append(user_message_param)

        # Convert messages to the format expected by the API
        api_messages: List[ChatCompletionMessageParam] = []
        for msg in self.conversation_history:
            if msg["role"] == "system":
                api_message: ChatCompletionSystemMessageParam = {
                    "role": "system",
                    "content": msg["content"]
                }
            elif msg["role"] == "user":
                api_message: ChatCompletionUserMessageParam = {
                    "role": "user",
                    "content": msg["content"]
                }
            elif msg["role"] == "assistant":
                api_message: ChatCompletionAssistantMessageParam = {
                    "role": "assistant",
                    "content": msg["content"]
                }
            api_messages.append(api_message)

        # Create completion with properly typed messages
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,  # Use the properly typed messages
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stream=True,
            stop=None,
        )

        assistant_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                assistant_response += content

        # Add assistant response with correct type
        assistant_message_param: ChatMessage = {
            "role": "assistant",
            "content": assistant_response,
            "name": None
        }
        self.conversation_history.append(assistant_message_param)

        return assistant_response

    def clear_history(self):
        """
        Limpa o histórico de conversação, mantendo apenas a mensagem do sistema.
        """
        system_message = self.conversation_history[0]  # Save system message
        self.conversation_history = [system_message]  # Reset history but keep system message

# Configuração da chave da API do OpenAI
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

word_search_generator = WordSearchGenerator(api_key=API_KEY)
mind_map_generator = MindMapGenerator(api_key=API_KEY)
flashcard_generator = FlashcardGenerator(api_key=API_KEY)

# Initialize the educational assistant
assistant = EducationalAssistant(api_key=API_KEY)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate-word-search")
async def generate_word_search(request: WordSearchRequest):
    """
    Gera um caça-palavras com base em um tópico fornecido.

    Parâmetros:
        request (WordSearchRequest): O tópico desejado para a geração do caça-palavras.

    Retorna:
        dict: A grade do caça-palavras e a lista de palavras e suas coordenadas.
    """
    result = word_search_generator.generate_word_search(request.topic)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar o caça-palavras.")
    return result

@app.post("/generate-mind-map")
async def generate_mind_map(request: MindMapRequest):
    """
    Gera um mapa mental com base em um assunto fornecido.

    Parâmetros:
        request (MindMapRequest): O assunto desejado para a geração do mapa mental.

    Retorna:
        dict: O mapa mental gerado em formato JSON.
    """
    result = mind_map_generator.generate_mind_map(request.subject)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar o mapa mental.")
    return result

@app.post("/generate-flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """
    Gera flashcards personalizados com base em um assunto e o número desejado de flashcards.

    Parâmetros:
        request (FlashcardRequest): O assunto e o número de flashcards desejados.

    Retorna:
        dict: Os flashcards gerados em formato JSON.
    """
    result = flashcard_generator.create_flashcards(request.subject, request.num_flashcards)
    if not result:
        raise HTTPException(status_code=400, detail="Não foi possível gerar os flashcards.")
    return result

# Add new request model
class MessageRequest(BaseModel):
    message: str
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024

@app.post("/send-message")
async def send_message(request: MessageRequest):
    """
    Envia uma mensagem do usuário para o assistente educacional e recebe uma resposta.
    
    Parâmetros:
        request (MessageRequest): A mensagem enviada pelo usuário, temperatura e max_tokens.
        
    Retorna:
        str: A resposta gerada pelo assistente.
    """
    # Handle optional parameters with default values
    temperature = request.temperature if request.temperature is not None else 1.0
    max_tokens = request.max_tokens if request.max_tokens is not None else 1024
    
    response = assistant.send_message(
        user_message=request.message,
        temperature=temperature,
        max_tokens=max_tokens
    )
    if not response:
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta do assistente.")
    return {"response": response}

@app.post("/clear-history")
async def clear_history():
    """
    Limpa o histórico de conversação do assistente educacional.
    """
    assistant.clear_history()
    return {"message": "Histórico de conversação limpo com sucesso."}