# -*- coding: utf-8 -*-
"""
向量数据库调试工具
用于简易调试ChromaDB向量数据库，包括打印、添加、删除等功能
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import chromadb
from chromadb.config import Settings


class VectorDBDebug:
    """向量数据库调试工具类"""
    
    def __init__(self, persist_dir=None):
        """
        初始化向量数据库调试工具
        
        Args:
            persist_dir: 向量数据库持久化目录，默认为 instance/vector_db
        """
        if persist_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            persist_dir = os.path.join(base_dir, 'instance', 'vector_db')
        
        self.persist_dir = persist_dir
        self.client = None
        self.collection = None
    
    def connect(self, collection_name="patent_knowledge"):
        """连接到向量数据库"""
        try:
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_collection(name=collection_name)
            print(f"✅ 已连接到集合: {collection_name}")
            return True
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            return False
    
    def list_collections(self):
        """列出所有集合"""
        if not self.client:
            self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        collections = self.client.list_collections()
        print("\n📚 集合列表:")
        for i, col in enumerate(collections, 1):
            print(f"  {i}. {col.name}")
        return collections
    
    def print_info(self):
        """打印集合信息"""
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        count = self.collection.count()
        print(f"\n📊 集合信息:")
        print(f"  名称: {self.collection.name}")
        print(f"  文档数: {count}")
        print(f"  持久化目录: {self.persist_dir}")
    
    def print_all(self, limit=10):
        """
        打印所有文档
        
        Args:
            limit: 最大打印数量，默认10
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        count = self.collection.count()
        print(f"\n📖 文档列表 (共{count}条，显示前{min(limit, count)}条):")
        print("-" * 80)
        
        if count == 0:
            print("  (空集合)")
            return
        
        results = self.collection.get(limit=limit)
        
        for i, (doc_id, doc, metadata) in enumerate(zip(
            results['ids'], 
            results['documents'], 
            results['metadatas']
        ), 1):
            print(f"\n[{i}] ID: {doc_id}")
            print(f"    内容: {doc[:100]}{'...' if len(doc) > 100 else ''}")
            print(f"    元数据: {json.dumps(metadata, ensure_ascii=False)}")
    
    def search(self, query, top_k=3):
        """
        搜索相似文档
        
        Args:
            query: 查询文本
            top_k: 返回数量
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        print(f"\n🔍 搜索: \"{query}\"")
        print("-" * 80)
        
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        if not results['documents'] or not results['documents'][0]:
            print("  未找到相关文档")
            return
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ), 1):
            print(f"\n[{i}] 相似度: {1-distance:.4f}")
            print(f"    内容: {doc[:100]}{'...' if len(doc) > 100 else ''}")
            print(f"    元数据: {json.dumps(metadata, ensure_ascii=False)}")
    
    def add_document(self, content, metadata=None, doc_id=None):
        """
        添加单个文档
        
        Args:
            content: 文档内容
            metadata: 元数据字典
            doc_id: 文档ID，不指定则自动生成
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        if metadata is None:
            metadata = {"source": "manual_add", "timestamp": datetime.now().isoformat()}
        
        if doc_id is None:
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            print(f"✅ 文档已添加: {doc_id}")
            return doc_id
        except Exception as e:
            print(f"❌ 添加失败: {str(e)}")
            return None
    
    def add_documents(self, documents, metadatas=None, ids=None):
        """
        批量添加文档
        
        Args:
            documents: 文档内容列表
            metadatas: 元数据列表
            ids: ID列表
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        if ids is None:
            ids = [f"doc_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}" 
                   for i in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{"source": "batch_add"} for _ in documents]
        
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ 已添加 {len(documents)} 个文档")
            return ids
        except Exception as e:
            print(f"❌ 批量添加失败: {str(e)}")
            return None
    
    def delete_by_id(self, doc_id):
        """
        根据ID删除文档
        
        Args:
            doc_id: 文档ID
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        try:
            self.collection.delete(ids=[doc_id])
            print(f"✅ 文档已删除: {doc_id}")
        except Exception as e:
            print(f"❌ 删除失败: {str(e)}")
    
    def delete_by_ids(self, doc_ids):
        """
        批量删除文档
        
        Args:
            doc_ids: 文档ID列表
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        try:
            self.collection.delete(ids=doc_ids)
            print(f"✅ 已删除 {len(doc_ids)} 个文档")
        except Exception as e:
            print(f"❌ 批量删除失败: {str(e)}")
    
    def delete_all(self, confirm=True):
        """
        删除所有文档
        
        Args:
            confirm: 是否需要确认
        """
        if not self.collection:
            print("❌ 请先连接到集合")
            return
        
        count = self.collection.count()
        if count == 0:
            print("集合为空，无需删除")
            return
        
        if confirm:
            ans = input(f"⚠️  确定要删除全部 {count} 个文档吗？(yes/no): ")
            if ans.lower() != 'yes':
                print("已取消")
                return
        
        # 获取所有ID并删除
        results = self.collection.get()
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            print(f"✅ 已删除 {count} 个文档")
    
    def clear_collection(self, collection_name=None):
        """
        清空集合并重新创建
        
        Args:
            collection_name: 集合名称
        """
        if collection_name is None:
            collection_name = self.collection.name if self.collection else "patent_knowledge"
        
        try:
            self.client.delete_collection(name=collection_name)
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "专利知识库向量存储"}
            )
            print(f"✅ 集合已清空并重建: {collection_name}")
        except Exception as e:
            print(f"❌ 清空失败: {str(e)}")


def interactive_mode():
    """交互式调试模式"""
    print("=" * 60)
    print("  向量数据库调试工具 - 交互模式")
    print("=" * 60)
    
    debugger = VectorDBDebug()
    debugger.list_collections()
    
    # 连接默认集合
    debugger.connect()
    
    while True:
        print("\n" + "-" * 40)
        print("命令列表:")
        print("  1. info     - 查看集合信息")
        print("  2. list     - 列出所有文档")
        print("  3. search   - 搜索文档")
        print("  4. add      - 添加文档")
        print("  5. delete   - 删除文档")
        print("  6. clear    - 清空集合")
        print("  7. quit     - 退出")
        print("-" * 40)
        
        cmd = input("\n请输入命令: ").strip().lower()
        
        if cmd in ['quit', 'exit', 'q']:
            print("再见！")
            break
        elif cmd == 'info':
            debugger.print_info()
        elif cmd == 'list':
            limit = input("显示数量 (默认10): ").strip()
            debugger.print_all(limit=int(limit) if limit.isdigit() else 10)
        elif cmd == 'search':
            query = input("输入搜索内容: ").strip()
            if query:
                debugger.search(query)
        elif cmd == 'add':
            content = input("输入文档内容: ").strip()
            if content:
                debugger.add_document(content)
        elif cmd == 'delete':
            doc_id = input("输入文档ID: ").strip()
            if doc_id:
                debugger.delete_by_id(doc_id)
        elif cmd == 'clear':
            debugger.clear_collection()
        else:
            print("未知命令，请重试")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="向量数据库调试工具")
    parser.add_argument('command', nargs='?', default='interactive', 
                       help='命令: interactive/info/list/search/add/delete/clear')
    parser.add_argument('--query', '-q', help='搜索查询')
    parser.add_argument('--content', '-c', help='文档内容')
    parser.add_argument('--id', help='文档ID')
    parser.add_argument('--limit', '-l', type=int, default=10, help='显示数量限制')
    parser.add_argument('--collection', default='patent_knowledge', help='集合名称')
    
    args = parser.parse_args()
    
    debugger = VectorDBDebug()
    
    if args.command == 'interactive':
        interactive_mode()
    else:
        debugger.connect(args.collection)
        
        if args.command == 'info':
            debugger.print_info()
        elif args.command == 'list':
            debugger.print_all(limit=args.limit)
        elif args.command == 'search':
            if args.query:
                debugger.search(args.query)
            else:
                print("请使用 --query 指定搜索内容")
        elif args.command == 'add':
            if args.content:
                debugger.add_document(args.content, doc_id=args.id)
            else:
                print("请使用 --content 指定文档内容")
        elif args.command == 'delete':
            if args.id:
                debugger.delete_by_id(args.id)
            else:
                print("请使用 --id 指定文档ID")
        elif args.command == 'clear':
            debugger.clear_collection()
        else:
            print(f"未知命令: {args.command}")
