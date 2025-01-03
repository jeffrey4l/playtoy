#!/usr/bin/env python3

import argparse
import logging
import os
import time

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import numpy as np
from rich.console import Console
from rich.layout import Layout
from rich.markdown import Markdown
import streamlit as st

from chromadb.config import Settings
from transformers.models.esm.modeling_esmfold import ipa_point_weights_init_

from langchain_huggingface import HuggingFaceEmbeddings


LOG = logging.getLogger(__name__)

api = '50990dd1b3988d6236595620bcba99dd.XXLjxagltgvYuock'


class BaseAction:
    name = ''
    def add_parser(self, parser: argparse.ArgumentParser):
        pass

    def run(self, conf: argparse.Namespace):
        pass


class UIAction(BaseAction):
    name = 'ui'

    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--data', type=str, required=True)
        parser.add_argument('--embedding', type=str, default='hugeface')

    def gen_awnser(self, question, conf):
        db = Chroma(
            persist_directory=conf.data,
            embedding_function=get_embedding(conf.embedding))
        LOG.info(f"database info: {db._collection.count()}")

        chat = ChatZhipuAI(
            api_key=api,
            model="glm-4",
            temperature=0.2,
        )
        template = """你是一个IaaS云系统AI助手，回答使用以下上下文来回答最后的问题;如果你不知道答案，就说你不知道，不要试图编造答案;描写出详细的步骤;使用标准的 markdown 格式进行回答；

上下文内容：{context}

问题: {question}
"""

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template)
        qa_chain = RetrievalQA.from_chain_type(
            chat,
            retriever=db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        result = qa_chain.invoke({"query": question})
        r = result['result']

        r += '\n# 相关资料:\n'
        for d in result['source_documents']:
            r += ' * %s\n' % d.metadata['source']
        return r


    def run(self, conf: argparse.Namespace):
        st.set_page_config(layout="wide")
        st.markdown("<h1 style='margin-top: 0;'>test env</h1>", unsafe_allow_html=True)

        # Add custom CSS for auto height and width
        st.markdown(
            """
            <style>
            .stContainer {
                height: auto !important;
                width: auto !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if 'messages' not in st.session_state:
            st.session_state.messages = []

        messages = st.container()  # Removed height parameter

        for message in st.session_state.messages:
            if message["role"] == "user":
                messages.chat_message("user").write(message["text"])
            elif message["role"] == "assistant":
                messages.chat_message("assistant").write(message["text"])

        if prompt := st.chat_input("say"):
            st.session_state.messages.append({"role": "user", "text": prompt})
            # Display the user's message immediately
            messages.chat_message("user").write(prompt)

            answer = self.gen_awnser(prompt, conf)

            if answer is not None:
                st.session_state.messages.append({"role": "assistant", "text": answer})
                messages.chat_message("assistant").write(answer)



class AskAction(BaseAction):
    name = 'ask'

    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--data', type=str, required=True)
        parser.add_argument('--embedding', type=str, default='zhipu')
        parser.add_argument('question', type=str)

    def run(self, conf):
        db = Chroma(
            persist_directory=conf.data,
            embedding_function=get_embedding(conf.embedding))
        LOG.info(f"database info: {db._collection.count()}")

        chat = ChatZhipuAI(
            api_key=api,
            model="glm-4",
            temperature=0.2,
        )
        template = """你是一个IaaS云系统AI助手，回答使用以下上下文来回答最后的问题;如果你不知道答案，就说你不知道，不要试图编造答案;描写出详细的步骤;使用标准的 markdown 格式进行回答；

上下文内容：{context}

问题: {question}
"""

        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template)
        qa_chain = RetrievalQA.from_chain_type(
            chat,
            retriever=db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        result = qa_chain.invoke({"query": conf.question})

        console = Console()

        r = result['result']

        r += '\n# 相关资料:\n'
        for d in result['source_documents']:
            r += ' * %s\n' % d.metadata['source']

        d = Markdown(r)
        console.print(f'问题: {conf.question}')
        console.print(f'答案如下：')
        console.print(d)

        print("参考文档:")
        for doc in result['source_documents']:
            d = Markdown(doc.page_content)
            print("------------------------------------------")
            console.print(d)

class TestAction(BaseAction):
    name = 'test'
    def run(self, conf):
        layout = Layout()
        c = Console()
        c.print(layout)

class Ask2Action(BaseAction):
    name = 'ask_2'

    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--data', type=str, required=True)
        parser.add_argument('question', type=str)

    def run(self, conf):
        db = Chroma(
            persist_directory=conf.data,
            embedding_function=get_embedding(conf.embedding))
        LOG.info(f"database info: {db._collection.count()}")

        chat = ChatZhipuAI(
            api_key=api,
            model="glm-4",
            temperature=0.5,
        )

        messages = [
            AIMessage(content="Hi."),
            SystemMessage(content="你是一个编程助手"),
            HumanMessage(content="用 python 写一个冒泡排序算法"),
        ]
        response = chat.invoke(messages)
        print(response.content)



class SearchAction(BaseAction):
    name = 'search'

    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--data', type=str, required=True)
        parser.add_argument('--embedding', type=str, default='zhipu')
        parser.add_argument('question', type=str)

    def run(self, conf):
        db = Chroma(
            persist_directory=conf.data,
            embedding_function=get_embedding(conf.embedding))
        LOG.info(f"database info: {db._collection.count()}")

        docs = db.similarity_search(conf.question, k=3)
        for i, doc in enumerate(docs):
            print(f"检索到的第{i+1}个内容: \n{doc.page_content[:200]}", end="\n--------------\n")

        docs = db.max_marginal_relevance_search(conf.question, k=3)
        for i, doc in enumerate(docs):
            print(f"检索到的第{i+1}个内容: \n{doc.page_content[:200]}", end="\n--------------\n")

def get_embedding(type_):
    if type_ == 'zhipu':
        return ZhipuAIEmbeddings(api_key=api)
    elif type_ == 'hugeface':
        return HuggingFaceEmbeddings(
            model_name="jinaai/jina-embeddings-v3",
            model_kwargs={"trust_remote_code": True}
        )
    return ValueError("unknown embedding type: %s" % type_)

class GenIndexAction(BaseAction):
    name = 'gen_index'

    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--data', type=str, required=True)
        parser.add_argument('--knowledge', type=str, required=True)
        parser.add_argument('--skip', type=int, default=0)
        parser.add_argument('--sleep' ,type=float, default=0.5)
        parser.add_argument('--embedding', type=str, default='zhipu')
        parser.add_argument('--max-docs', type=int, default=0)


    def run(self, conf):
        LOG.info(f"gen_index: {conf.data}, {conf.knowledge}")
        docs = list(split_documents(conf.knowledge, max_docs=conf.max_docs))
        split_docs = np.array_split(docs, len(docs)//1 + 1)
        split_count = len(split_docs)
        embedding = get_embedding(conf.embedding)
        for idx, d in enumerate(split_docs):
            if conf.skip and idx < conf.skip:
                continue
            LOG.info("%d/%d Post docs: %d" % (idx, split_count, len(d)))
            try:
                db = Chroma.from_documents(
                    documents=list(d),
                    embedding=embedding,
                    client_settings=Settings(anonymized_telemetry=False),
                    persist_directory=conf.data)
                print(db._collection.count())
            except:
                LOG.exception("Failed to index %d" % idx)
            finally:
                time.sleep(conf.sleep)


def split_documents(parent, max_docs=0):
    total = 0
    for root, _, files in os.walk(parent):
        for file in files:
            if file.find('SUMMARY') != -1:
                continue
            if file.endswith('.md'):
                for doc in UnstructuredMarkdownLoader(os.path.join(root, file)).load():
                    if len(doc.page_content) < 100:
                        continue
                    yield doc
                    total += 1
                    if max_docs and total >= max_docs:
                        return


class SplitAction(BaseAction):
    name = 'split'
    def add_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--knowledge', type=str, required=True)

    def run(self, conf):
        for idx, doc in enumerate(split_documents(conf.knowledge)):
            print("%d %s" % (idx, '='*150))
            print(doc)
            print("=" * 150)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true')
    sub_parser = parser.add_subparsers(dest='subcommand', required=True)
    for action in [z() for z in BaseAction.__subclasses__()]:
        p = sub_parser.add_parser(action.name)
        action.add_parser(p)
        p.set_defaults(subcommand=action.run)

    conf = parser.parse_args()
    level=logging.INFO
    if conf.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    conf.subcommand(conf)

if __name__ == '__main__':
    main()
