import spacy

if __name__ == '__main__':
    # 加载中文模型
    nlp_zh = spacy.load("zh_core_web_sm")

    # 处理中文文本
    doc_zh = nlp_zh("苹果公司正在考虑收购一家英国初创公司")

    # 分词
    for token in doc_zh:
        print(token.text)

    # 命名实体识别
    for ent in doc_zh.ents:
        print(f"{ent.text}: {ent.label_}")
