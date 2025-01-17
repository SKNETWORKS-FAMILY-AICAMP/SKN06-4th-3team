from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableLambda
from operator import itemgetter
from langchain_openai import ChatOpenAI
import os
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_chroma_vector_store():
    """Chroma 벡터 스토어 로드"""
    vector_store_path = os.path.join(BASE_DIR, "api", "data", "vector_store")
    embeddings = OpenAIEmbeddings()  # OpenAI Embeddings 사용
    vector_store = Chroma(persist_directory=vector_store_path, embedding_function=embeddings)
    return vector_store


class Chatting:
    """
    대화형 AI 채팅 클래스.
    
    GPT 모델을 사용하여 사용자와 대화를 수행하고, 대화 기록을 관리한다.
    """

    def __init__(self):
        
        model = ChatOpenAI(model="gpt-4o-mini")

        messages = [
            ("ai", """
            너는 유능한 약사야. 
            context 안에 있는 약 중에 사용자가 입력한 증상에 맞는 약을 3개 선택해서 표 형식으로 추천해줘. 
            
            표에 담기는 내용은 약 별로 '이름, 효능, 복용법, 주의사항'이야.
            
            약은 복용이 간단하고 부작용이 적은 약을 우선적으로 추천해줘. 

            추가적으로
            1. 약을 복용하기 전 반드시 알아야 할 사항을 알려줘.
            2. 증상이 악화될 때 대처방법을 알려줘.
            
            [context]
            {context}"""),
            MessagesPlaceholder("history"), 
            ("human", "{query}")
            ]

        # 그리고 약국에 대한 정보를 물어보면 'recommend_pharmacy'라고만 트리거 줘
        #    context가 없으면 모른다고해
        # 약국 정보는 이후에 삽입. 

        prompt_template = ChatPromptTemplate(messages)
        
        output_parser = StrOutputParser()

        vector_store = load_chroma_vector_store()

        retriever = vector_store.as_retriever(
            search_type='mmr',
            # search_type="similarity_score_threshold",
            search_kwargs = {
                'k':5,
                'fetch_k':10
            }
        )

        def get_context(input_data:dict):
            return retriever.invoke(input_data['query'])

        self.chain = {'context':RunnableLambda(get_context), 
                    'query':itemgetter("query"), 
                    'history':itemgetter('history')
                    } | prompt_template | model | output_parser


    def send_message(self, message:str, history:list):
        """
        사용자 메시지를 처리하고 AI 응답을 반환.
        Parameter:
            message: str 사용자가 입력한 메시지
            history: list - 사용자와 AI간의 이전까지의 대화 기록

        Returns:
            str: AI의 응답 메시지
        """
        response = self.chain.invoke({"history": history, "query": message})
        
        return response
    
def add_message_to_history(history:list[tuple[str, str]], message:tuple[str, str], max_history=20):
    """
    Message를 history에 추가하는 util 메소드.
    파라미터로 받은 history에 message를 추가한다.
    max_history 개수를 넘어가면 오래된 것 부터 지운다.
    Parameter:
        history: list - 대화 기록
        message: tuple - (speaker, message) 형태의 메시지
        max_history: int - 저장할 최대 대화 기록 개수
    """
    while len(history) >= max_history:
        history.pop(0)
    history.append(message)