"""
記事情報ベクトル化エリア
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from library.file_management import save,read,add,add_row,is_contain
import pickle
import os
import re
dir_path = './posts'
documents = []
out_doc = ''
in_doc = ''
for filename in os.listdir(dir_path):
    filepath = os.path.join(f'{dir_path}', filename)
    loader = TextLoader(filepath)
    doc = loader.load()[0]
    url = doc.page_content.split('\n')[0]
    paragraphs = re.sub(r'((?:大|中|小)見出し：(?:[^\n])+?)\n(?=(?:[大|中|小]見出し)：|$)',"", doc.page_content, re.DOTALL)
    paragraphs = re.findall(r'[大|中|小]見出し：(.+?\n.+?)(?=(?:[大|中|小]見出し)：|$)', paragraphs, re.DOTALL)
    for parag in paragraphs:
        # if len(parag)<200 or re.match(r'^.*(?:\n.*){9,}$', parag):
        #     out_doc = out_doc + parag + '\n---\n'
        #     continue
        in_doc = in_doc + parag + '\n---\n'
        documents.append(Document(page_content=parag,metadata={'source':url}))
save(out_doc,f'./liny-manual-chatbot/除外段落.txt')
save(in_doc,f'./liny-manual-chatbot/適用段落.txt')

# Load Data to vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)


# Save vectorstore
with open("./liny-manual-chatbot/vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)