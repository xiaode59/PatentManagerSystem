# -*- coding: utf-8 -*-
"""
向量数据库调试工具 - 使用示例

用法:
  python debug_vector.py interactive    # 交互模式
  python debug_vector.py info           # 查看集合信息
  python debug_vector.py list           # 列出所有文档
  python debug_vector.py search "专利" # 搜索
  python debug_vector.py add "内容"     # 添加文档
  python debug_vector.py delete xxx    # 删除文档
  python debug_vector.py clear          # 清空集合
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.vector_debug import VectorDBDebug


def example_info():
    """示例：查看向量数据库信息"""
    print("=" * 50)
    print("示例1: 查看向量数据库信息")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    debugger.print_info()


def example_list():
    """示例：列出所有文档"""
    print("=" * 50)
    print("示例2: 列出所有文档")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    debugger.print_all(limit=5)


def example_search(query):
    """示例：搜索文档"""
    print("=" * 50)
    print("示例3: 搜索文档")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    debugger.search(query, top_k=3)


def example_add(content):
    """示例：添加文档"""
    print("=" * 50)
    print("示例4: 添加文档")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    
    # 添加单个文档
    doc_id = debugger.add_document(
        content=content,
        metadata={"category": "test", "source": "debug_example"}
    )
    print(f"添加的文档ID: {doc_id}")


def example_batch_add():
    """示例：批量添加文档"""
    print("=" * 50)
    print("示例5: 批量添加文档")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    
    documents = [
        "测试文档1：软件著作权保护期限为作者终生及死后50年",
        "测试文档2：发明专利保护期限为20年",
        "测试文档3：实用新型专利保护期限为10年"
    ]
    
    metadatas = [
        {"category": "software_copyright", "type": "duration"},
        {"category": "patent_basics", "type": "duration"},
        {"category": "patent_basics", "type": "duration"}
    ]
    
    debugger.add_documents(documents, metadatas)


def example_delete(doc_id):
    """示例：删除文档"""
    print("=" * 50)
    print("示例6: 删除文档")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    
    # 删除
    debugger.delete_by_id(doc_id)


def example_clear():
    """示例：清空集合"""
    print("=" * 50)
    print("示例7: 清空集合")
    print("=" * 50)
    
    debugger = VectorDBDebug()
    debugger.connect()
    debugger.clear_collection()


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  向量数据库调试工具 - 使用示例")
    print("=" * 60 + "\n")
    
    # 初始化
    example_info()
    
    # 列出现有文档
    example_list()
    
    # 搜索
    example_search("专利申请")
    
    # 添加单个文档
    example_add("测试文档内容")
    
    # 批量添加
    example_batch_add()
    
    print("\n" + "=" * 60)
    print("  所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="向量数据库调试工具使用示例")
    parser.add_argument('command', nargs='?', default='interactive', 
                       help='命令: interactive, info, list, search, add, delete, clear')
    parser.add_argument('params', nargs='*', help='命令参数')
    
    args = parser.parse_args()
    
    debugger = VectorDBDebug()
    
    if args.command == 'interactive':
        # 导入并运行交互模式
        from app.utils.vector_debug import interactive_mode
        interactive_mode()
    elif args.command == 'info':
        debugger.connect()
        debugger.print_info()
    elif args.command == 'list':
        debugger.connect()
        debugger.print_all(limit=10)
    elif args.command == 'search':
        if args.params:
            debugger.connect()
            debugger.search(' '.join(args.params))
        else:
            print("用法: python debug_vector.py search \"搜索内容\"")
    elif args.command == 'add':
        if args.params:
            debugger.connect()
            debugger.add_document(' '.join(args.params))
        else:
            print("用法: python debug_vector.py add \"文档内容\"")
    elif args.command == 'delete':
        if args.params:
            debugger.connect()
            debugger.delete_by_id(args.params[0])
        else:
            print("用法: python debug_vector.py delete <文档ID>")
    elif args.command == 'clear':
        debugger.connect()
        debugger.clear_collection()
    else:
        print(f"未知命令: {args.command}")
        print("\n用法:")
        print("  python debug_vector.py interactive       # 交互模式")
        print("  python debug_vector.py info             # 查看集合信息")
        print("  python debug_vector.py list             # 列出所有文档")
        print("  python debug_vector.py search \"专利\"   # 搜索文档")
        print("  python debug_vector.py add \"内容\"      # 添加文档")
        print("  python debug_vector.py delete <ID>      # 删除文档")
        print("  python debug_vector.py clear            # 清空集合")
