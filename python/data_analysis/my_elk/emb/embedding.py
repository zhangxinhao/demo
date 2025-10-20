import hashlib
from typing import List, Union

import numpy as np


class MockEmbeddingModel:
    """
    用于测试的 Embedding 模型替代工具类
    支持文本转向量、相似度计算等基本功能
    """

    def __init__(self, embedding_dim: int = 768, seed: int = 42):
        """
        初始化模型

        Args:
            embedding_dim: 向量维度，默认768（模拟BERT）
            seed: 随机种子，保证可复现性
        """
        self.embedding_dim = embedding_dim
        self.seed = seed
        np.random.seed(seed)

    def encode(self, texts: Union[str, List[str]], normalize: bool = True) -> np.ndarray:
        """
        将文本编码为向量

        Args:
            texts: 单个文本或文本列表
            normalize: 是否归一化向量

        Returns:
            numpy数组，shape为 (n_texts, embedding_dim)
        """
        # 统一处理为列表
        if isinstance(texts, str):
            texts = [texts]
            single_input = True
        else:
            single_input = False

        embeddings = []
        for text in texts:
            # 使用hash保证相同文本得到相同向量
            embedding = self._text_to_vector(text)
            embeddings.append(embedding)

        embeddings = np.array(embeddings)

        # 归一化
        if normalize:
            embeddings = self._normalize(embeddings)

        # 如果输入是单个文本，返回一维数组
        if single_input:
            return embeddings[0]

        return embeddings

    def _text_to_vector(self, text: str) -> np.ndarray:
        """
        将文本转换为向量（基于hash的确定性方法）
        """
        # 使用MD5 hash生成种子
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_int = int(hash_obj.hexdigest(), 16)

        # 使用hash作为种子生成向量
        rng = np.random.RandomState(hash_int % (2 ** 32))
        vector = rng.randn(self.embedding_dim)

        # 添加一些基于文本特征的调整，使相似文本更接近
        # 基于文本长度
        length_factor = len(text) / 100.0
        vector[0] += length_factor

        # 基于字符集
        unique_chars = len(set(text))
        vector[1] += unique_chars / 50.0

        # 基于常见词（简单模拟）
        common_words = ['的', '是', '在', 'the', 'is', 'in', 'a', 'an']
        for i, word in enumerate(common_words[:min(8, len(common_words))]):
            if word in text.lower():
                vector[i + 2] += 0.5

        return vector

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        """L2归一化"""
        norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)  # 避免除零
        return vectors / norms

    def similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的余弦相似度

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度分数 [-1, 1]
        """
        emb1 = self.encode(text1, normalize=True)
        emb2 = self.encode(text2, normalize=True)
        return float(np.dot(emb1, emb2))

    def batch_similarity(self, query: str, candidates: List[str]) -> List[float]:
        """
        计算查询文本与候选文本列表的相似度

        Args:
            query: 查询文本
            candidates: 候选文本列表

        Returns:
            相似度分数列表
        """
        query_emb = self.encode(query, normalize=True)
        candidate_embs = self.encode(candidates, normalize=True)

        # 计算余弦相似度
        similarities = np.dot(candidate_embs, query_emb)
        return similarities.tolist()

    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[tuple]:
        """
        找出最相似的文本

        Args:
            query: 查询文本
            candidates: 候选文本列表
            top_k: 返回前k个最相似的

        Returns:
            [(index, text, similarity_score), ...] 列表
        """
        similarities = self.batch_similarity(query, candidates)

        # 获取top_k个最相似的索引
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append((int(idx), candidates[idx], similarities[idx]))

        return results


def demo_single_text_encoding(emb: MockEmbeddingModel):
    """演示单个文本编码"""
    print("\n1. 单个文本编码:")
    text = "这是一个测试文本"
    embedding = emb.encode(text)
    print(f"文本: {text}")
    print(f"向量维度: {embedding.shape}")
    print(f"向量前10个值: {embedding[:10]}")


def demo_batch_encoding(emb: MockEmbeddingModel):
    """演示批量文本编码"""
    print("\n2. 批量文本编码:")
    texts = ["苹果很好吃", "香蕉也不错", "我喜欢吃水果"]
    embeddings = emb.encode(texts)
    print(f"文本数量: {len(texts)}")
    print(f"向量矩阵形状: {embeddings.shape}")


def demo_similarity_calculation(emb: MockEmbeddingModel):
    """演示相似度计算"""
    print("\n3. 相似度计算:")
    text1 = "我喜欢吃苹果"
    text2 = "我喜欢吃香蕉"
    text3 = "今天天气真好"
    sim1 = emb.similarity(text1, text2)
    sim2 = emb.similarity(text1, text3)
    print(f"'{text1}' vs '{text2}': {sim1:.4f}")
    print(f"'{text1}' vs '{text3}': {sim2:.4f}")


def demo_batch_similarity(emb: MockEmbeddingModel):
    """演示批量相似度计算"""
    print("\n4. 批量相似度计算:")
    query = "Python编程语言"
    candidates = [
        "Python是一种编程语言",
        "Java也是编程语言",
        "我喜欢吃苹果",
        "机器学习很有趣",
        "Python用于数据科学"
    ]
    similarities = emb.batch_similarity(query, candidates)
    print(f"查询: {query}")
    for i, (cand, sim) in enumerate(zip(candidates, similarities)):
        print(f"  {i + 1}. [{sim:.4f}] {cand}")


def demo_find_most_similar(emb: MockEmbeddingModel):
    """演示找出最相似的文本"""
    print("\n5. 找出最相似的文本 (Top 3):")
    query = "Python编程语言"
    candidates = [
        "Python是一种编程语言",
        "Java也是编程语言",
        "我喜欢吃苹果",
        "机器学习很有趣",
        "Python用于数据科学"
    ]
    results = emb.find_most_similar(query, candidates, top_k=3)
    for rank, (idx, text, score) in enumerate(results, 1):
        print(f"  {rank}. [索引:{idx}, 分数:{score:.4f}] {text}")


def demo_consistency_check(emb: MockEmbeddingModel):
    """演示验证相同文本的一致性"""
    print("\n6. 验证相同文本的一致性:")
    emb1 = emb.encode("测试文本")
    emb2 = emb.encode("测试文本")
    print(f"两次编码是否完全相同: {np.allclose(emb1, emb2)}")
    print(f"余弦相似度: {np.dot(emb1, emb2):.6f}")


def main():
    """主函数入口 - 演示MockEmbeddingModel的各项功能"""
    print("=" * 60)
    print("MockEmbeddingModel 测试")
    print("=" * 60)

    # 初始化嵌入模型
    emb = MockEmbeddingModel(embedding_dim=384)

    # 执行各项功能演示
    demo_single_text_encoding(emb)
    demo_batch_encoding(emb)
    demo_similarity_calculation(emb)
    demo_batch_similarity(emb)
    demo_find_most_similar(emb)
    demo_consistency_check(emb)

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
