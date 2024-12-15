import re
import sys
import os
import json
from collections import defaultdict
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_regex_patterns(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"配置文件 '{config_file}' 未找到。")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"配置文件 '{config_file}' 格式错误: {e}")
        sys.exit(1)

def extract_info(directory_path, regex_patterns):
    extracted_info = defaultdict(set)
    for dirpath, _, filenames in os.walk(directory_path):
        for file in filenames:
            if file.endswith('.js'):
                file_path = os.path.join(dirpath, file)
                try:
                    with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for key, info in regex_patterns.items():
                            pattern = re.compile(info['pattern'], re.IGNORECASE | re.MULTILINE)
                            matches = pattern.findall(content)
                            for match in matches:
                                if isinstance(match, tuple):
                                    match = ''.join(match)
                                extracted_info[key].add(f"{file}---{match.strip()}")
                except Exception as e:
                    logging.error(f"处理文件 {file_path} 时出错: {e}")
    return extracted_info

def print_menu(regex_patterns):
    categories = defaultdict(list)
    for key, info in regex_patterns.items():
        categories[info['category']].append(key)

    print("\n请选择一个类别：")
    for i, category in enumerate(categories.keys(), 1):
        print(f"{i}. {category}")
    print("0. 退出")

    return categories

def handle_category_choice(category, regex_patterns):
    print(f"\n请选择 {category} 中的项目：")
    items = [key for key, info in regex_patterns.items() if info['category'] == category]
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")
    print(f"{len(items) + 1}. 全部")

    choice = input("请输入选项编号：")
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        return [items[int(choice) - 1]]
    elif choice == str(len(items) + 1):
        return items
    else:
        print("无效的选择")
        return []

def print_results(extracted_info, keys):
    results_found = False
    for key in keys:
        if extracted_info[key]:
            results_found = True
            print(f"\n=== {key} ===")
            for value in sorted(extracted_info[key]):
                print(value)
    
    if not results_found:
        print("未找到匹配的结果。")

def save_results(extracted_info, keys, output_file):
    with open(output_file, "w", encoding='utf-8') as f:
        results_found = False
        for key in keys:
            if extracted_info[key]:
                results_found = True
                f.write(f"=== {key} ===\n")
                for value in sorted(extracted_info[key]):
                    f.write(value + '\n')
                f.write('\n')
    
    if results_found:
        print(f"结果已保存到：{output_file}")
    else:
        print("未找到匹配的结果，未创建文件。")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 extractor.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"目录 '{directory_path}' 不存在。")
        sys.exit(1)

    regex_patterns = load_regex_patterns('regex_patterns.json')
    extracted_info = extract_info(directory_path, regex_patterns)

    while True:
        categories = print_menu(regex_patterns)
        choice = input("请输入类别编号：")

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = list(categories.keys())[int(choice) - 1]
            keys = handle_category_choice(category, regex_patterns)
        else:
            print("无效的选择")
            continue

        if keys:
            output_choice = input("请选择输出方式（1: 终端输出, 2: 保存到文件）：")
            if output_choice == "1":
                print_results(extracted_info, keys)
            elif output_choice == "2":
                output_file = input("请输入保存文件的路径：")
                save_results(extracted_info, keys, output_file)
            else:
                print("无效的选择")

if __name__ == "__main__":
    main()
