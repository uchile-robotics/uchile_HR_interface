__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import ollama
import chromadb
from utilities import getconfig

class NLPProcessor:
    def __init__(self):
        config = getconfig()
        self.embedmodel = config["embedmodel"]
        self.mainmodel = config["mainmodel"]
        self.chroma = chromadb.PersistentClient(path="/home/bender/catkin_ws/src/uchile_hr_interface/src/conversation_smach/test")
        self.collection = self.chroma.get_or_create_collection("buildragwithpython")

    def process_query(self, query):
        queryembed = ollama.embeddings(model=self.embedmodel, prompt=query)['embedding']
        relevantdocs = self.collection.query(query_embeddings=[queryembed], n_results=5)["documents"][0]
        docs = "\n\n".join(relevantdocs)

        modelquery = f"{query} - Responde en español usando el siguiente documento como fuente: {docs}"
        stream = ollama.generate(model=self.mainmodel, prompt=modelquery, stream=True)

        response = ""
        for chunk in stream:
            if chunk["response"]:
                response += chunk['response']
        
        return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        nlp_processor = NLPProcessor()
        response = nlp_processor.process_query(query)
        print(response)
    else:
        print("Por favor, proporcione un argumento para el prompt.")