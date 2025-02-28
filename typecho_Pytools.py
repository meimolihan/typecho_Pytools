import json
import re
import datetime
import sys
import os
import shutil
from pytypecho import Typecho, Attachment, Post


# 如果不存在config.json则创建
def create_config():
    # 定义文件路径
    file_path = 'config.json'

    # 判断文件是否存在config.json
    if not os.path.exists(file_path):
        # 若文件不存在，定义要写入的配置信息
        config_data = {
            "url": "http://192.168.188.137",
            "username": "admin",
            "password": "123456"
        }
        try:
            # 以写入模式打开文件
            with open(file_path, 'w', encoding='utf-8') as f:
                # 使用 json.dump 将配置信息以缩进格式写入文件
                json.dump(config_data, f, ensure_ascii=False, indent=4)
            print(f"文件 {file_path} 已创建并写入配置信息。")
        except Exception as e:
            print(f"创建文件 {file_path} 并写入内容时出错: {e}")


# 如果不存在md、hexo_md、ok_md文件夹则创建
def create_directories():
    # 定义要检查的顶级目录列表
    top_level_directories = ['md', 'hexo_md', 'ok_md']

    # 遍历顶级目录列表
    for directory in top_level_directories:
        if not os.path.exists(directory):
            try:
                # 如果目录不存在，则创建它
                os.makedirs(directory)
                print(f"目录 {directory} 已创建。")
            except FileExistsError:
                print(f"目录 {directory} 已经被其他进程创建。")
            except PermissionError:
                print(f"没有权限创建目录 {directory}。")
            except Exception as e:
                print(f"创建目录 {directory} 时发生错误: {e}")

    # 检查 ok_md 目录下的子目录
    ok_md_path = 'ok_md'
    sub_directories = ['md', 'hexo_md']
    for sub_dir in sub_directories:
        sub_dir_path = os.path.join(ok_md_path, sub_dir)
        if not os.path.exists(sub_dir_path):
            try:
                # 如果子目录不存在，则创建它
                os.makedirs(sub_dir_path)
                print(f"目录 {sub_dir_path} 已创建。")
            except FileExistsError:
                print(f"目录 {sub_dir_path} 已经被其他进程创建。")
            except PermissionError:
                print(f"没有权限创建目录 {sub_dir_path}。")
            except Exception as e:
                print(f"创建目录 {sub_dir_path} 时发生错误: {e}")


# 剪切文件到ok_md下
def move_file_with_confirmation(source_file, target_folder="ok_md/md"):
    # 检查目标文件夹是否存在，若不存在则创建
    if not os.path.exists(target_folder):
        try:
            os.makedirs(target_folder)
            print(f"已创建目标文件夹: {target_folder}")
        except PermissionError:
            print(f"没有权限创建文件夹 {target_folder}，请检查权限。")
            return
        except Exception as e:
            print(f"创建文件夹 {target_folder} 时出现错误: {e}")
            return

    # 检查源文件是否存在
    if not os.path.isfile(source_file):
        print(f"源文件 {source_file} 不存在，请检查文件路径。")
        return

    # 获取源文件的文件名
    file_name = os.path.basename(source_file)
    target_file = os.path.join(target_folder, file_name)

    # 检查目标文件是否已存在
    if os.path.exists(target_file):
        while True:
            user_input = input(f"目标文件 {target_file} 已存在，是否替换？(y/n): ").strip().lower()
            if user_input == 'y':
                try:
                    shutil.move(source_file, target_file)
                    print(f"文件 {source_file} 已成功移动并替换 {target_file}。")
                    break
                except PermissionError:
                    print(f"没有权限移动文件 {source_file}，请检查文件和目录的权限。")
                    break
                except Exception as e:
                    print(f"移动文件时出现错误: {e}")
                    break
            elif user_input == 'n':
                print("取消文件移动操作。")
                break
            else:
                print("无效的输入，请输入 'y' 或 'n'。")
    else:
        try:
            shutil.move(source_file, target_file)
            print(f"文件 {source_file} 已成功移动到 {target_file}。")
        except PermissionError:
            print(f"没有权限移动文件 {source_file}，请检查文件和目录的权限。")
        except Exception as e:
            print(f"移动文件时出现错误: {e}")


# 读取本地json文件中的配置
def read_config():
    # 读取 JSON 文件
    with open('config.json', 'r') as file:
        config = json.load(file)
    # 获取 url, username 和 password
    url = config.get('url')
    if url.endswith('/'):
        url = url + "index.php/action/xmlrpc"
    else:
        url = url + "/index.php/action/xmlrpc"
    username = config.get('username')
    password = config.get('password')
    return url, username, password


# 获取一个md文件中hexo的头部信息，并过滤出来作为文章参数
def extract_metadata(file_path):
    """
    从 Markdown 文件中提取 title、date、categories 和 tags 的内容。

    :param file_path: Markdown 文件的路径
    :return: 包含提取信息的字典
    """
    metadata = {
        'title': '',
        'date': '',
        'categories': [],
        'tags': []
    }

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        in_categories = False
        in_tags = False

        for line in lines:
            line = line.strip()

            if line.startswith('title:'):
                metadata['title'] = line.split('title:')[1].strip()
            elif line.startswith('date:'):
                metadata['date'] = line.split('date:')[1].strip()
            elif line.startswith('categories:'):
                in_categories = True
                continue
            elif line.startswith('tags:'):
                in_categories = False
                in_tags = True
                continue
            elif line.startswith('-') and in_categories:
                category = line.replace('-', '').strip()
                metadata['categories'].append(category)
            elif line.startswith('-') and in_tags:
                tag = line.replace('-', '').strip()
                metadata['tags'].append(tag)
            elif line and not line.startswith('-'):
                in_categories = False
                in_tags = False
    return metadata


# 获取一个md文件中的文章内容
def extract_primary(file_path):
    # 打开并读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式删除 '---' 和 '---' 之间的内容
    description = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
    description = re.sub(r"\[toc\]", '', description, flags=re.DOTALL)
    return "<!--markdown-->" + description


# 判断是否存在大小写不一样但是名字一样的分类,直接返回结果(分类名)
def check_string_in_array(input_string):
    # 取出blog中所有的分类
    blog_categories = []
    for x in te.get_categories():
        blog_categories.append(x["categoryName"])

    # 将输入字符串转换为小写
    input_string = input_string.lower()
    # 将数组中的每个元素都转换为小写
    lower_array = [element.lower() for element in blog_categories]
    # 判断转换后的输入字符串是否在转换后的数组中
    if input_string in lower_array:
        return blog_categories[lower_array.index(input_string)]
    else:
        return input_string


# 查找指定目录下所有的.md文件
def find_md_files(directory):
    md_files = []
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # 构建文件的完整路径
                md_files.append(os.path.join(root, file))
    return md_files


# 检查是否存在config.json
create_config()

# 检查是否存在md和hexo_md和ok_md目录
create_directories()

# 读取url账号密码
url, username, password = read_config()

# 创建一个typecho对象
te = Typecho(url, username=username, password=password)


# 处理日期解析的函数
def parse_date(date_str):
    try:
        # 尝试解析 ISO 8601 格式
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        try:
            # 尝试解析 '%Y-%m-%d %H:%M:%S' 格式
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # 如果都解析失败，使用当前时间
            print(f"日期解析失败: {date_str}，使用当前时间。")
            return datetime.datetime.now()


while True:
    print("---------------------typecho_Pytools-----------------------")
    print("1、md导入typecho")
    print("2、查看博客数据")
    print("3、删除博客数据")
    print("4、退出")
    try:
        num = int(input("输入序号:"))
    except:
        input("输入错误重新输入!")
        continue
    if num == 1:  # md导入typecho
        print("-----------------------1、md导入typecho-----------------------")
        print("1、传统md导入typecho")
        print("2、hexo格式md导入typecho")
        try:
            num = int(input("输入序号："))
        except:
            input("输入错误！")
        if num == 1:  # 传统md
            directory = './md'  # 查找.md的目录
            md_directory = find_md_files(directory)
            if len(md_directory) == 0:
                input("md_hexo文件夹没有数据!  回车返回")
                continue

            for x in md_directory:
                print(f"{x}")
            i = 0
            input("检查是否正确，回车开始导入！")
            for md_file in md_directory:
                i = i + 1
                print(f"开始导入第{i}个文件，{md_file}")
                description = extract_primary(md_file)  # 拿到文章内容
                title = input("输入文章标题:")  # 标题
                dateCreated = parse_date(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 发表时间
                categories = input("输入分类：")
                categories = check_string_in_array(categories)  # 检查分类大小写bug
                mt_keywords = input("输入标签(多标签用,隔开)：")  # 标签
                post = Post(title=title, dateCreated=dateCreated, categories=[f'{categories}'], mt_keywords=mt_keywords,
                            description=description)
                te.new_post(post, publish=True)  # 发布
                print(md_file, "发布成功")
                move_file_with_confirmation(md_file, "ok_md/md")
                print("-------------------------------------------------------------")
        elif num == 2:  # hexo格式的md
            directory = './hexo_md'  # 查找.md的目录
            md_directory = find_md_files(directory)
            if len(md_directory) == 0:
                input("md文件夹没有数据!  回车返回")
                continue

            for x in md_directory:
                print(f"{x}")
            input("检查是否正确，回车开始导入！")
            for md_file in md_directory:
                print(f"{md_file}")
                description = extract_primary(md_file)  # 拿到文章内容
                result = extract_metadata(md_file)  # 过滤出hexo参数作为typecho参数
                title = result['title']  # 标题
                dateCreated = parse_date(result['date'])  # 发表时间
                categories = ', '.join(result['categories'])  # 分类
                categories = check_string_in_array(categories)  # 检查分类大小写bug
                mt_keywords = ', '.join(result['tags'])  # 标签
                post = Post(title=title, dateCreated=dateCreated, categories=[f'{categories}'], mt_keywords=mt_keywords,
                            description=description)
                te.new_post(post, publish=True)  # 发布
                print(md_file, "发布成功")
                move_file_with_confirmation(md_file, "ok_md/hexo_md")
                print("-------------------------------------------------------------")
        else:
            print("输入错误！")

    elif num == 2:  # 查看博客数据
        while True:
            print("---------------------2、查看博客数据-----------------------")
            print("1、查看博客分类")
            print("2、查看所有博客")
            print("3、查看帖子信息")
            print("4、查看评论信息")
            print("5、返回")
            try:
                num = int(input("输入序号:"))
            except:
                input("输入错误重新输入!")
                continue
            if num == 1:
                blog_categories = []
                for x in te.get_categories():
                    blog_categories.append(x["categoryName"])
                print(blog_categories)
                input("回车继续")
            elif num == 2:
                for x in te.get_posts():
                    # print(f"标题：{x[0]['title']} 序号:{x[0]['title']}")
                    print(f" 文章id:{x['postid']} 标题：{x['title']} ")
                print("一共有", len(te.get_posts()), "文章")
                input("回车继续")
            elif num == 3:
                id = int(input("输入帖子id："))
                tz = te.get_post(id)
                print(f"url：{tz['link']}")
                print(f"标题：{tz['title']}")
                print(f"分类：{tz['categories']}")
                print(f"标签：{tz['mt_keywords']}")
                print(f"作者：{tz['wp_author']}")
                input("回车继续")
            elif num == 4:
                tz_comment = te.get_comments()
                print(f"本站一共{len(tz_comment)}条评论")
                print('-----------------------------------------------')
                for x in tz_comment:
                    print(f"帖子标题:<<{x['post_title']}>>  评论url:{x['link'] } 评论id:{x['comment_id']}")
                    print(f"评论时间:{x['date_created_gmt']}|名字:{x['author']}|邮件{[ 'author_email']}")
                    print(f"内容:“{x['content']}”")
                    print('-----------------------------------------------')
                input("回车继续")
            elif num == 5:
                break
    elif num == 3:  # 删除博客数据
        while True:
            print("---------------------3、删除博客数据-----------------------")
            print("1、删除帖子")
            print("2、删除评论")
            print("3、返回")
            try:
                num = int(input("输入序号:"))
            except:
                input("输入错误重新输入!")
                continue
            if num == 1:  # 删除帖子
                post_id = int(input("输入要删除的帖子id:"))
                inquire = input("确认删除吗?y/n:")
                if inquire == 'y' or inquire == 'Y':
                    te.del_post(post_id)
                    print(f"id为{post_id}的帖子已删除!")
                    input("回车继续!")
                else:
                    break
            elif num == 2:  # 删除评论
                comment_id = int(input("输入要删除的评论id:"))
                inquire = input("确认删除吗?y/n:")
                if inquire == 'y' or inquire == 'Y':
                    te.del_comment(comment_id=comment_id)
                    print(f"id为{comment_id}的评论已删除!")
                    input("回车继续!")
                else:
                    break
            elif num == 3:
                break
            else:
                print("输入错误，重新输入！")

    elif num == 4:  # 退出
        sys.exit()
    else:
        input("输入不正确，重新输入！")

