from elasticsearch import Elasticsearch
from emb.embedding import MockEmbeddingModel


def init_elasticsearch_client(host: str = "http://localhost:9017") -> Elasticsearch:
    """初始化 Elasticsearch 客户端"""
    print(f"正在连接 Elasticsearch: {host}")
    es = Elasticsearch([host])
    return es


def create_vector_index(es: Elasticsearch, index_name: str, dims: int = 768):
    """创建向量索引"""
    # 检查索引是否已存在
    if es.indices.exists(index=index_name):
        print(f"索引 '{index_name}' 已存在，正在删除...")
        es.indices.delete(index=index_name)

    index_mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "category": {"type": "keyword"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    es.indices.create(index=index_name, body=index_mapping)
    print(f"成功创建索引 '{index_name}' (维度: {dims})")


def insert_documents(es: Elasticsearch, index_name: str, embedding_model: MockEmbeddingModel):
    """批量插入文档"""
    documents = [
        {"id": 1, "text": "Python是一种高级编程语言", "category": "编程"},
        {"id": 2, "text": "机器学习是人工智能的一个分支", "category": "AI"},
        {"id": 3, "text": "Elasticsearch是一个分布式搜索引擎", "category": "数据库"},
        {"id": 4, "text": "深度学习使用神经网络进行训练", "category": "AI"},
        {"id": 5, "text": "Java是一种面向对象的编程语言", "category": "编程"},
        {"id": 6, "text": "向量数据库用于存储和检索高维向量", "category": "数据库"},
        {"id": 7, "text": "自然语言处理是AI的重要应用领域", "category": "AI"},
        {"id": 8, "text": "JavaScript常用于Web前端开发", "category": "编程"},
        {"id": 9, "text": "NumPy是Python的科学计算库", "category": "编程"},
        {"id": 10, "text": "MongoDB是一个NoSQL数据库", "category": "数据库"},
    ]

    print(f"\n正在插入 {len(documents)} 个文档...")
    for doc_data in documents:
        doc = {
            "text": doc_data["text"],
            "category": doc_data["category"],
            "embedding": embedding_model.encode(doc_data["text"], normalize=True).tolist()
        }
        es.index(index=index_name, id=doc_data["id"], document=doc)
        print(f"  已插入 [ID: {doc_data['id']}] {doc_data['text']}")

    # 刷新索引以确保文档可搜索
    es.indices.refresh(index=index_name)
    print(f"成功插入 {len(documents)} 个文档")


def vector_search(es: Elasticsearch, index_name: str, embedding_model: MockEmbeddingModel,
                  query_text: str, k: int = 5):
    """执行向量搜索"""
    print(f"\n查询: '{query_text}'")
    print("-" * 60)

    query_vector = embedding_model.encode(query_text, normalize=True).tolist()
    response = es.search(
        index=index_name,
        knn={
            "field": "embedding",
            "query_vector": query_vector,
            "k": k,
            "num_candidates": 100
        }
    )

    results = []
    for rank, hit in enumerate(response['hits']['hits'], 1):
        result = {
            "rank": rank,
            "score": hit['_score'],
            "text": hit['_source']['text'],
            "category": hit['_source']['category']
        }
        results.append(result)
        print(f"  {rank}. [分数: {result['score']:.4f}] [{result['category']}] {result['text']}")

    return results


def hybrid_search(es: Elasticsearch, index_name: str, embedding_model: MockEmbeddingModel,
                  query_text: str, category_filter: str = None, k: int = 5):
    """混合搜索：向量搜索 + 关键词过滤"""
    print(f"\n混合查询: '{query_text}'", end="")
    if category_filter:
        print(f" (分类: {category_filter})")
    else:
        print()
    print("-" * 60)

    query_vector = embedding_model.encode(query_text, normalize=True).tolist()

    search_body = {
        "knn": {
            "field": "embedding",
            "query_vector": query_vector,
            "k": k,
            "num_candidates": 100
        }
    }

    # 添加分类过滤
    if category_filter:
        search_body["knn"]["filter"] = {
            "term": {"category": category_filter}
        }

    response = es.search(index=index_name, **search_body)

    results = []
    for rank, hit in enumerate(response['hits']['hits'], 1):
        result = {
            "rank": rank,
            "score": hit['_score'],
            "text": hit['_source']['text'],
            "category": hit['_source']['category']
        }
        results.append(result)
        print(f"  {rank}. [分数: {result['score']:.4f}] [{result['category']}] {result['text']}")

    return results


def main():
    """主函数入口"""
    print("=" * 60)
    print("Elasticsearch 向量搜索演示")
    print("=" * 60)

    # 配置参数
    INDEX_NAME = "my_vectors"
    EMBEDDING_DIM = 768
    ES_HOST = "http://127.0.0.1:9017"

    # 1. 初始化 Embedding 模型
    print("\n1. 初始化 Embedding 模型")
    embedding_model = MockEmbeddingModel(embedding_dim=EMBEDDING_DIM, seed=42)
    print(f"已初始化 MockEmbeddingModel (维度: {EMBEDDING_DIM})")

    # 2. 连接 Elasticsearch
    print("\n2. 连接 Elasticsearch")
    es = init_elasticsearch_client(ES_HOST)

    # 3. 创建索引
    print("\n3. 创建向量索引")
    create_vector_index(es, INDEX_NAME, EMBEDDING_DIM)

    # 4. 插入文档
    print("\n4. 插入示例文档")
    insert_documents(es, INDEX_NAME, embedding_model)

    # 5. 向量搜索示例
    print("\n" + "=" * 60)
    print("5. 向量搜索示例")
    print("=" * 60)

    # 示例查询 1
    vector_search(es, INDEX_NAME, embedding_model, "编程语言相关", k=3)

    # 示例查询 2
    vector_search(es, INDEX_NAME, embedding_model, "人工智能和深度学习", k=3)

    # 示例查询 3
    vector_search(es, INDEX_NAME, embedding_model, "数据存储和检索", k=3)

    # 6. 混合搜索示例
    print("\n" + "=" * 60)
    print("6. 混合搜索示例（向量搜索 + 分类过滤）")
    print("=" * 60)

    hybrid_search(es, INDEX_NAME, embedding_model, "编程", category_filter="编程", k=5)
    hybrid_search(es, INDEX_NAME, embedding_model, "智能算法", category_filter="AI", k=5)

    # 7. 相似度对比
    print("\n" + "=" * 60)
    print("7. 文本相似度对比")
    print("=" * 60)
    texts = [
        "Python编程语言",
        "深度学习算法",
        "数据库系统"
    ]
    print("\n文本间的相似度:")
    for i, text1 in enumerate(texts):
        for j, text2 in enumerate(texts):
            if i < j:
                similarity = embedding_model.similarity(text1, text2)
                print(f"  '{text1}' <-> '{text2}': {similarity:.4f}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
