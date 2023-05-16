"""
記事情報ベクトル化エリア
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from library.file_management import save,read,add,add_row,is_contain
import pickle
import os
import re
dir_path = './posts'
documents = []
for filename in os.listdir(dir_path):
    filepath = os.path.join(f'{dir_path}', filename)
    loader = TextLoader(filepath)
    doc = loader.load()[0]
    url = doc.page_content.split('\n')[0]
    paragraphs = re.sub(r'((?:大|中|小)見出し：(?:[^\n])+?)\n(?=(?:[大|中|小]見出し)：|$)',"", doc.page_content, re.DOTALL)
    paragraphs = re.findall(r'[大|中|小]見出し：(.+?\n.+?)(?=(?:[大|中|小]見出し)：|$)', paragraphs, re.DOTALL)
    for parag in paragraphs:
        if len(parag)<200 or re.match(r'^.*(?:\n.*){9,}$', parag):
            out_doc = out_doc + parag + '\n---\n'
            continue
        in_doc_str = in_doc_str + parag + '\n---\n'
        documents.append(Document(page_content=parag,metadata={'source':url}))
save(out_doc,f'{kw.path_bench_source}/除外段落.txt')
save(in_doc_str,f'{kw.path_bench_source}/適用段落.txt')

# Load Data to vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)


# Save vectorstore
with open("vectorstore.pkl", "wb") as f:
    pickle.dump(vectorstore, f)


# こちらの内容をもとに作成 https://github.com/hwchase17/chat-your-data/blob/master/ingest_data.py

####################
# play_chatbot.py #
####################
# こちらの内容をもとに作成 https://github.com/hwchase17/chat-your-data/blob/master/app.py#L20