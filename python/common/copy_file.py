import os
import shutil


def move_files(source_dir, target_dir):
    # 使用os.listdir来获取源目录中的所有文件和文件夹
    for filename in os.listdir(source_dir):
        # 使用os.path.join来构造完整的文件路径
        full_file_path = os.path.join(source_dir, filename)

        # 使用os.path.isfile来检查这是否是一个文件
        # 使用str.endswith来检查文件名是否以.md结尾
        if os.path.isfile(full_file_path) and filename.endswith('.md'):
            # 使用shutil.move来移动文件到目标目录
            print(filename)
            shutil.copy(full_file_path, target_dir)


def change_file_name(directory):
    # 使用 os.listdir 获取目录中的所有文件
    for filename in os.listdir(directory):
        # 使用 os.path.join 构造完整的文件路径
        full_file_path = os.path.join(directory, filename)

        if os.path.isdir(full_file_path):
            change_file_name(full_file_path)
        # 使用 os.path.isfile 检查这是否是一个文件
        if os.path.isfile(full_file_path):
            new_filename = filename.replace("【海量资源：666java.com】", "")
            print(filename)
            # 使用 os.rename 来修改文件名
            os.rename(full_file_path, os.path.join(directory, new_filename))


if __name__ == '__main__':
    # 调用函数，将当前目录下的txt文件移动到目标目录
    # move_files('/Users/zhangxinhao/Downloads/006-人工智能基础课', '/Users/zhangxinhao/Downloads/人工智能基础课')
    change_file_name('/Users/zhangxinhao/Downloads/人工智能基础课')
