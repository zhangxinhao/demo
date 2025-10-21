"""
Milvus VectorDatabase 基础操作示例

本示例演示了如何使用 VectorDatabase 进行基础的向量数据库操作：
- 插入单条记录 (insert)
- 批量插入 (batch_insert)
- 向量搜索 (search)
- 删除记录 (delete)
- 清空数据库 (clear)
- 使用 Knowledge 和 Experience 对象
"""

import uuid
from typing import List

from ahvn.ukf.templates.basic import Knowledge, Experience
from ahvn.utils.basic.hash_utils import md5hash
from ahvn.utils.basic.rnd_utils import stable_rnd_vector
from ahvn.utils.vdb.base import VectorDatabase


# ============================================================================
# Mock Encoder 和 Embedder 实现
# ============================================================================

def mock_encoder(obj) -> str:
    """
    Mock encoder，将任意对象转换为字符串表示。

    Args:
        obj: 任意对象 (BaseUKF, string 等)

    Returns:
        对象的字符串表示
    """
    if hasattr(obj, "content"):
        # 对于 BaseUKF 对象
        return f"{obj.name}: {obj.content}"
    else:
        # 对于普通字符串
        return str(obj)


def mock_embedder(text: str, dim: int = 128) -> List[float]:
    """
    Mock embedder，从文本生成稳定的、确定性的向量。

    使用 stable_rnd_vector 创建可复现的嵌入向量：
    - 相同文本总是生成相同向量
    - 不同文本生成不同向量
    - 向量模拟真实嵌入向量的行为

    Args:
        text: 待嵌入的文本
        dim: 嵌入维度 (默认 128)

    Returns:
        归一化的嵌入向量
    """
    # 对文本进行哈希得到整数种子
    seed = md5hash(text)
    return stable_rnd_vector(seed, dim=dim)


def create_mock_encoder_embedder(dim: int = 128):
    """
    创建用于测试的 (encoder, embedder) 元组。

    Args:
        dim: 嵌入维度

    Returns:
        (encoder_func, embedder_func) 元组
    """
    encoder = mock_encoder

    def embedder(text: str) -> List[float]:
        return mock_embedder(text, dim=dim)

    return encoder, embedder


# ============================================================================
# VectorDatabase 基础操作示例
# ============================================================================

def demo_basic_insert_search(vdb: VectorDatabase):
    """演示基础的插入和搜索操作"""
    print("\n" + "=" * 60)
    print("演示 1: 基础插入和搜索")
    print("=" * 60)

    # 创建简单的测试记录
    record1 = {
        "id": "doc_1",
        "text": "这是一篇关于机器学习的文档",
        "vector": [0.1] * 128,
        "category": "ml"
    }

    record2 = {
        "id": "doc_2",
        "text": "另一篇关于深度学习的文档",
        "vector": [0.2] * 128,
        "category": "dl"
    }

    # 插入记录
    print("\n插入记录...")
    vdb.insert(record1)
    print(f"  ✓ 已插入: {record1['id']}")
    vdb.insert(record2)
    print(f"  ✓ 已插入: {record2['id']}")

    # 使用嵌入向量搜索
    print("\n执行向量搜索...")
    query_embedding = [0.15] * 128
    query = vdb.search(embedding=query_embedding, topk=2)

    print(f"  搜索结果:")
    print(f"    - similarity_top_k : {query.similarity_top_k}")
    print(f"    - query_embedding 维度: {len(query.query_embedding)}")


def demo_batch_insert(vdb: VectorDatabase):
    """演示批量插入操作"""
    print("\n" + "=" * 60)
    print("演示 2: 批量插入")
    print("=" * 60)

    # 创建多条记录
    records = [
        {
            "id": f"batch_{i}",
            "text": f"批量文档 {i}",
            "vector": [float(i) * 0.1] * 128,
            "index": i
        }
        for i in range(10)
    ]

    # 批量插入
    print(f"\n批量插入 {len(records)} 条记录...")
    vdb.batch_insert(records)
    print(f"  ✓ 已插入 {len(records)} 条记录")

    # 搜索验证
    print("\n执行搜索验证...")
    query_embedding = [0.5] * 128
    query = vdb.search(embedding=query_embedding, topk=5)
    print(f"  ✓ 搜索成功，topk={query.similarity_top_k}")


def demo_ukf_knowledge_storage(vdb: VectorDatabase):
    """演示存储和检索 Knowledge 对象"""
    print("\n" + "=" * 60)
    print("演示 3: 存储 Knowledge 对象")
    print("=" * 60)

    # 创建 Knowledge 对象
    k1 = Knowledge(
        name="向量数据库知识",
        content="向量数据库支持语义搜索",
        tags={"[topic:vdb]", "[type:definition]"},
        priority=8
    )

    k2 = Knowledge(
        name="嵌入向量知识",
        content="嵌入向量将文本表示为稠密向量",
        tags={"[topic:embeddings]", "[type:definition]"},
        priority=7
    )

    print(f"\n创建 Knowledge 对象:")
    print(f"  - {k1.name} (priority={k1.priority})")
    print(f"  - {k2.name} (priority={k2.priority})")

    # 编码和嵌入 Knowledge 对象
    print("\n编码和嵌入 Knowledge 对象...")
    text1, vec1 = vdb.k_encode_embed(k1)
    text2, vec2 = vdb.k_encode_embed(k2)
    print(f"  ✓ 编码完成，向量维度: {len(vec1)}")

    # 存储为记录
    record1 = {
        "id": str(k1.id),
        "text": text1,
        "vector": vec1,
        "name": k1.name,
        "priority": k1.priority,
    }

    record2 = {
        "id": str(k2.id),
        "text": text2,
        "vector": vec2,
        "name": k2.name,
        "priority": k2.priority,
    }

    # 插入记录
    print("\n插入 Knowledge 记录...")
    vdb.insert(record1)
    vdb.insert(record2)
    print("  ✓ 已插入 2 条 Knowledge 记录")

    # 使用查询嵌入搜索
    print("\n搜索: '什么是向量数据库?'")
    query_text, query_vec = vdb.q_encode_embed("什么是向量数据库?")
    query = vdb.search(embedding=query_vec, topk=2)
    print(f"  ✓ 搜索成功，返回 {query.similarity_top_k} 条结果")


def demo_ukf_experience_storage(vdb: VectorDatabase):
    """演示存储和检索 Experience 对象"""
    print("\n" + "=" * 60)
    print("演示 4: 存储 Experience 对象")
    print("=" * 60)

    # 创建 Experience 对象
    exp1 = Experience(
        name="向量搜索操作",
        content="成功执行了相似度搜索",
        priority=6,
        metadata={"duration_ms": 120, "results": 5}
    )

    exp2 = Experience(
        name="嵌入向量生成",
        content="为用户查询生成了嵌入向量",
        priority=5,
        metadata={"model": "mock-embedder"}
    )

    print(f"\n创建 Experience 对象:")
    print(f"  - {exp1.name} (priority={exp1.priority})")
    print(f"  - {exp2.name} (priority={exp2.priority})")

    # 编码和嵌入
    print("\n编码和嵌入 Experience 对象...")
    text1, vec1 = vdb.k_encode_embed(exp1)
    text2, vec2 = vdb.k_encode_embed(exp2)

    # 存储为记录
    records = [
        {
            "id": str(exp1.id),
            "text": text1,
            "vector": vec1,
            "name": exp1.name,
            "priority": exp1.priority,
        },
        {
            "id": str(exp2.id),
            "text": text2,
            "vector": vec2,
            "name": exp2.name,
            "priority": exp2.priority,
        },
    ]

    # 批量插入
    print("\n批量插入 Experience 记录...")
    vdb.batch_insert(records)
    print("  ✓ 已插入 2 条 Experience 记录")

    # 搜索
    print("\n搜索: '搜索操作'")
    query_text, query_vec = vdb.q_encode_embed("搜索操作")
    query = vdb.search(embedding=query_vec, topk=2)
    print(f"  ✓ 搜索成功")


def demo_search_with_query_text(vdb: VectorDatabase):
    """演示使用查询文本进行搜索"""
    print("\n" + "=" * 60)
    print("演示 5: 使用查询文本搜索")
    print("=" * 60)

    # 插入一些文档
    records = [
        {
            "id": "ml_doc",
            "text": "机器学习算法",
            "vector": [0.1] * 128,
        },
        {
            "id": "dl_doc",
            "text": "深度神经网络",
            "vector": [0.2] * 128,
        },
    ]

    print(f"\n插入 {len(records)} 条文档...")
    vdb.batch_insert(records)
    print("  ✓ 插入完成")

    # 使用查询文本搜索（会被自动编码和嵌入）
    print("\n搜索: '机器学习'")
    query = vdb.search(query="机器学习", topk=1)
    print(f"  ✓ 搜索成功，topk={query.similarity_top_k}")


def demo_clear(vdb: VectorDatabase):
    """演示清空数据库操作"""
    print("\n" + "=" * 60)
    print("演示 6: 清空数据库")
    print("=" * 60)

    # 插入一些记录
    records = [
        {
            "id": f"clear_{i}",
            "text": f"文档 {i}",
            "vector": [float(i) * 0.1] * 128,
        }
        for i in range(5)
    ]

    print(f"\n插入 {len(records)} 条记录...")
    vdb.batch_insert(records)
    print("  ✓ 插入完成")

    # 清空数据库
    print("\n清空数据库...")
    try:
        vdb.clear()
        print("  ✓ 数据库已清空")
    except Exception as e:
        print(f"  ⚠ 清空操作失败 (某些后端可能不支持): {e}")


def main():
    """主函数：演示 Milvus VectorDatabase 的基础操作"""
    print("=" * 60)
    print("Milvus VectorDatabase 基础操作演示")
    print("=" * 60)

    # 创建 mock encoder 和 embedder
    encoder, embedder = create_mock_encoder_embedder(dim=128)
    print("✓ Mock encoder 和 embedder 已创建")

    # 配置参数
    collection_name = "demo_collection"
    connection_alias = f"demo_{uuid.uuid4().hex[:8]}"

    print(f"✓ Collection: {collection_name}")
    print(f"✓ Connection alias: {connection_alias}")

    # 创建 VectorDatabase 实例
    print("\n创建 VectorDatabase 实例...")
    try:
        vdb = VectorDatabase(
            provider="milvus",
            uri="http://127.0.0.1:9013",
            collection=collection_name,
            encoder=encoder,
            embedder=embedder,
            connection_alias=connection_alias,
            connect=True,
        )
        print("✓ VectorDatabase 已创建并连接")

        # 执行各种演示
        demo_basic_insert_search(vdb)
        demo_batch_insert(vdb)
        demo_ukf_knowledge_storage(vdb)
        demo_ukf_experience_storage(vdb)
        demo_search_with_query_text(vdb)
        demo_clear(vdb)

        print("\n" + "=" * 60)
        print("所有演示完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
