#!/usr/bin/env python3.8
import ollama

#sorta need order 
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import chromadb
from utilities import readtext, getconfig 
from mattsollamatools import chunker, chunk_text_by_sentences

chroma = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma.get_or_create_collection(
    name="bendercontext"
)

embedmodel = getconfig()["embedmodel"]
starttime = time.time()

#error source
with open('context/bendercontext.txt') as f:
  lines = f.readlines()
  for filename in lines:
    text = readtext(filename)
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
      print(".", end="", flush=True)
      collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))





# prompt = input("Ingrese el prompt: ")

# #prompt = "why is the sky blue?"
# output = ollama.generate(model="llama3", prompt=prompt, stream=True)
# # output = ollama.chat(model="llama3", messages=[{
# #     'role': 'user',
# #     'content': 'why is the sky blue?',

# # },])
# # print(response['message']['content'])

# for chunk in output:
#   print(chunk['response'], end='', flush=True)
 