import json

import meilisearch


def load_movies_data(file_path):
    """加载电影数据从JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            movies = json.load(json_file)
        print(f"成功加载 {len(movies)} 部电影数据")
        return movies
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"错误：无法解析JSON文件 {file_path}")
        return None


def main():
    # 使用相对路径读取movies.json文件
    movies_file_path = 'data/movies.json'
    
    # 初始化MeiliSearch客户端
    client = meilisearch.Client('http://127.0.0.1:9009', 'MASTER_KEY')
    
    # 加载电影数据
    movies = load_movies_data(movies_file_path)
    if movies is None:
        return
    
    try:
        # 将文档添加到索引
        print("正在添加文档到MeiliSearch索引...")
        result = client.index('movies').add_documents(movies)
        print(f"添加文档任务ID: {result.task_uid}")
        
        # 搜索示例
        print("\n搜索 'botman':")
        search_results = client.index('movies').search('botman')
        
        # 打印搜索结果
        if search_results['hits']:
            for hit in search_results['hits']:
                print(f"- {hit.get('title', '未知标题')}")
        else:
            print("没有找到匹配的结果")
            
    except Exception as e:
        print(f"MeiliSearch操作出错: {e}")


if __name__ == '__main__':
    main()
