import uuid
import os
from decouple import Config, RepositoryEnv

from utils.graph import graph
from utils.utilities import _print_event


# Appoint to enviroment variables
config = Config(RepositoryEnv("/home/nophaieviscente/my-projects/debt-chatbot/.env"))
API_KEY = config("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY

# %%
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": thread_id,
    }
}

count = 0
while True:
    if count == 0:
        print(
            "Olá eu sou o chatbot da Acerto, estou aqui para auxiliar a quitar suas dívidas. Como posso ajudá-lo?"
        )
    # _printed = set()
    question = input("Fale com o bot: ")
    events = graph.invoke(
        {"messages": ("user", question)},
        config,  # stream_mode="values"
    )
    print("Acerto Bot: ", events["messages"][-1].content)
    # for event in events:
    #     _print_event(event, _printed)

    if question.lower() in ["tchau", "sair", "até mais"]:
        break
    count += 1
