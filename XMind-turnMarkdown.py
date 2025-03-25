import json
import os
import sys

def process_topic(topic, level=0):
    """处理单个主题节点,返回markdown格式的文本"""
    if not topic:
        return ""
    
    # 获取主题标题
    title = topic.get('title', '')
    if not title:
        return ""
    
    # 计算缩进
    indent = "  " * level
    
    # 构建markdown行
    md_line = f"{indent}- {title}\n"
    
    # 处理子主题
    children = topic.get('children', {}).get('attached', [])
    for child in children:
        md_line += process_topic(child, level + 1)
    
    return md_line

def convert_xmind_to_markdown(json_file, output_file):
    """将XMind JSON文件转换为Markdown格式"""
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 处理每个sheet
        for sheet in data:
            # 写入sheet标题
            f.write(f"# {sheet['title']}\n\n")
            
            # 处理根主题
            root_topic = sheet.get('rootTopic', {})
            if root_topic:
                f.write(process_topic(root_topic))
            
            f.write("\n")

def print_usage():
    print("用法: python xmind_to_markdown.py <输入文件路径> <输出文件路径>")
    print("示例: python xmind_to_markdown.py content.json mindmap.md")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误: 未找到输入文件 {input_file}")
        sys.exit(1)
    
    try:
        convert_xmind_to_markdown(input_file, output_file)
        print(f"转换完成! 输出文件保存在: {output_file}")
    except Exception as e:
        print(f"转换过程中出现错误: {str(e)}")
        sys.exit(1)