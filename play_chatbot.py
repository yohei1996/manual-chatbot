from langchain.prompts.prompt import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOpenAI
import gradio as gr
import pickle

with open("./liny-manual-chatbot/vectorstore.pkl", "rb") as f:
    vectorstore:FAISS = pickle.load(f)

retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

template = """
You are an adviser for answering questions about the web tool liny.
please answer the following question　based on reference text to answer the question.
output the answer to <answer here> in the output section.
and output the reference source ot <refarence sources here> in the reference text section.
do not change the reference tnsource url.

question: {question}

reference text:
'''
{reference_text}
'''

output:
<answer here>
参考:<refarence sources here>
"""


def chat(message, history=[]):
    try:
        llm = ChatOpenAI()
        prompt = PromptTemplate(
            input_variables=["question","reference_text"],
            template=template,
        )
        docs = retriever.get_relevant_documents(message)
        reference_text = ""
        for doc in docs:
            if len(reference_text) > 500: break
            reference_text += f'text:\n{doc.page_content}\nsource:\n{doc.metadata["source"]}\n\n'
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run({"question":message,"reference_text":reference_text})
    except Exception as e:
        response = f"予期しないエラーが発生しました: {e}"

    history.append((message, response))
    return history, history

chatbot = gr.Chatbot()

demo = gr.Interface(
    chat,
    ['text',  'state'],
    [chatbot, 'state'],
    allow_flagging = 'never',
)

demo.launch()