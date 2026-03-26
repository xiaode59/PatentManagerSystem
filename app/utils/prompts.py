# -*- coding: utf-8 -*-
"""
RAG服务的提示词和知识库配置
"""

# 系统提示词模板
SYSTEM_PROMPT_TEMPLATE = """你是一个专业的专利与软件著作权咨询助手，专门帮助用户解答关于专利申请、软件著作权登记等相关问题。

## 你的职责
- 回答用户关于专利和软著的问题
- 使用提供的参考信息来回答问题
- 如果参考信息不足，可以结合你的知识进行回答
- 回答要专业、准确、清晰

## 参考信息
以下是知识库中的一些参考信息，你可以根据这些信息来回答问题：
{context}

如果没有相关参考信息，请结合你的知识回答。"""

# 专利知识库数据
PATENT_KNOWLEDGE = [
    {
        'content': '专利申请文件包括：请求书、说明书、权利要求书、摘要。说明书应当对发明作出清楚、完整的说明。',
        'metadata': {'category': 'patent_basics', 'type': 'application'}
    },
    {
        'content': '发明专利保护期限为20年，实用新型专利保护期限为10年，外观设计专利保护期限为15年（2021年修法后）。',
        'metadata': {'category': 'patent_basics', 'type': 'duration'}
    },
    {
        'content': '软件著作权申请需要提供：软件源代码（前、后各3000行）、软件说明书、身份证明文件。',
        'metadata': {'category': 'software_copyright', 'type': 'requirements'}
    },
    {
        'content': '专利新颖性要求：在申请日以前，未在世界范围内公开发表或使用过。创造性要求：具有突出的实质性特点和显著进步。',
        'metadata': {'category': 'patent_basics', 'type': 'criteria'}
    },
    {
        'content': '软著登记流程：在线提交→受理→审查→公示→发证。一般周期为2-3个月。',
        'metadata': {'category': 'software_copyright', 'type': 'process'}
    },
    {
        'content': '专利审查流程：受理→初步审查→实质审查→授权/驳回。发明专利实质审查通常需要1-3年。',
        'metadata': {'category': 'patent_basics', 'type': 'process'}
    },
    {
        'content': '技术交底书应包含：发明名称、技术领域、背景技术、发明内容、技术方案、具体实施方式、优点。',
        'metadata': {'category': 'patent_basics', 'type': 'document'}
    },
    {
        'content': '软件著作权保护的是源代码和文档，不包括软件的思想、算法。保护期限为作者终生及死后50年。',
        'metadata': {'category': 'software_copyright', 'type': 'protection'}
    }
]
