from dataclasses import dataclass
from datetime import datetime
from typing import List

from jinja2 import Environment, FileSystemLoader


@dataclass
class User:
    """用户数据模型"""
    name: str
    age: int
    email: str
    is_active: bool = True

@dataclass
class Product:
    """商品数据模型"""
    id: int
    name: str
    price: float
    category: str
    tags: List[str]

class JinjaDemo:
    """Jinja2 模板引擎演示类"""
    
    def __init__(self, template_dir="templates"):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        # 注册自定义过滤器
        self.env.filters['currency'] = self.currency_filter
    
    @staticmethod
    def currency_filter(value):
        """货币格式化过滤器"""
        return f"¥{value:.2f}"
    
    def demo_basic_rendering(self):
        """基础模板渲染演示"""
        print("=== 基础模板渲染演示 ===")
        template = self.env.get_template("index.html")
        user = User(name="张三", age=25, email="zhang@example.com")
        
        html = template.render(
            user=user,
            year=datetime.now().year,
            title="欢迎页面"
        )
        print(html)
        print()
    
    def demo_list_rendering(self):
        """列表渲染演示"""
        print("=== 列表渲染演示 ===")
        template = self.env.get_template("products.html")
        
        products = [
            Product(1, "笔记本电脑", 5999.99, "电子产品", ["办公", "便携"]),
            Product(2, "智能手机", 3299.00, "电子产品", ["通讯", "娱乐"]),
            Product(3, "咖啡杯", 29.90, "生活用品", ["陶瓷", "保温"])
        ]
        
        html = template.render(
            products=products,
            year=datetime.now().year,
            total_count=len(products)
        )
        print(html)
        print()
    
    def demo_conditional_rendering(self):
        """条件渲染演示"""
        print("=== 条件渲染演示 ===")
        template = self.env.get_template("user_profile.html")
        
        users = [
            User("李四", 30, "li@example.com", True),
            User("王五", 22, "wang@example.com", False),
            User("赵六", 35, "zhao@example.com", True)
        ]
        
        for user in users:
            html = template.render(user=user, year=datetime.now().year)
            print(f"--- {user.name} 的个人资料 ---")
            print(html)
            print()
    
    def demo_macro_usage(self):
        """宏使用演示"""
        print("=== 宏使用演示 ===")
        template = self.env.get_template("forms.html")
        
        html = template.render(year=datetime.now().year)
        print(html)
        print()
    
    def run_all_demos(self):
        """运行所有演示"""
        self.demo_basic_rendering()
        self.demo_list_rendering()
        self.demo_conditional_rendering()
        self.demo_macro_usage()

if __name__ == '__main__':
    demo = JinjaDemo()
    demo.run_all_demos()
