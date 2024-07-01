import os
from decouple import Config, RepositoryEnv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig

from utils.state import State
from utils.tools import verify_cpf, verify_date_birth, verify_debt


# Appoint to enviroment variables
config = Config(RepositoryEnv("/home/nophaieviscente/my-projects/debt-chatbot/.env"))
API_KEY = config("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            # Configuration to assistant
            configuration = config.get("configurable", {})
            cpf = configuration.get("", None)
            # Get state from before call
            state = {**state, "user_info": cpf}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [
                    ("user", "Responda com uma saída real.")
                ]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um chatbot da Acerto, uma empresa que renegocia dívidas. "
            " Use as ferramentas para verificar se o CPF do usuário e também a data de nascimento correspondente são válidos no banco."
            " O formato de entrada da data de nascimento deve ser por exemplo DD/MM/AAAA."
            " Se não for peça novamente, não use a próxima ferramenta caso não valide."
            " Nunca passe ao próximo passo caso ambas as ferramentas verify_cpf e verify_date_birth não tenham saída true."
            " Se ambas as informações forem corretas mostre ao usuário as informações sobre as dívidas caso não, peça dados válidos."
            " Se sua busca retornar vazia, informe que não existem dívidas para esses dados."
            " Forneça exemplos de como o CPF é caso o usuário peça, porém sempre cheque esses exemplos antes de passar ao próximo passo."
            " Não forneça informações inventadas, Se estiver com dúvidas pergunte novamente."
            " Não valide informações inventadas, sempre use suas ferramentas para a validação."
            " Caso o CPF não seja válido, peça o de novo. Não passe a pedir data de nascimento de CPF inválido."
            "\n\nUsuário Atual:\n\n{user_info}\n",
        ),
        ("placeholder", "{messages}"),
    ]
)

tools = [verify_cpf, verify_date_birth, verify_debt]
assistant_runnable = primary_assistant_prompt | llm.bind_tools(tools)
