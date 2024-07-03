__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# import nltk
# nltk.download('punkt')
import ollama, chromadb, time
from utilities import readtext, getconfig
from mattsollamatools import chunker, chunk_text_by_sentences   


#should keep existing in time
#chroma = chromadb.HttpClient(host='localhost', port=8000)
# chroma = chromadb.PersistentClient(path="test")
# collection = chroma.get_or_create_collection(
#     name="bendercontext", metadata={"hnsw:space": "cosine"}
# )

collectionname="buildragwithpython"

chroma = chromadb.PersistentClient(path="test")
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
  print('deleting collection')
  chroma.delete_collection("buildragwithpython")
collection = chroma.get_or_create_collection(name="buildragwithpython", metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
starttime = time.time()
with open('sourcedocs.txt') as f:
  lines = f.readlines()
  for filename in lines:
    text = readtext(filename)
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 ) #por defecto en 7
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
      print(".", end="", flush=True)
      collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))