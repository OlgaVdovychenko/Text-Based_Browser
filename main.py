import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style


def url_ok(string):
    if string.count('.') >= 1:
        return True
    return False


def write_to_files(path, content):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(content)


def print_from_file(path):
    with open(path, 'r') as fh:
        print(fh.read())


def get_request(url):
    user_agent = 'Mozilla/5.0'
    try:
        r = requests.get(url, headers={'User-Agent': user_agent})
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        return None
    else:
        if r.status_code == 200:
            return r
        return None


def parsing_html(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    tags_list = ['p', 'headers', 'a', 'ul', 'ol', 'ol', 'li',
                 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    lst = soup.find_all(tags_list)
    res_lst = []
    for elem in lst:
        line = elem.text.strip()
        if len(line):
            if elem.name == 'a':
                line = Fore.BLUE + line + Fore.RESET
            res_lst.append(line)
    return '\n'.join(res_lst)


if __name__ == '__main__':
    args = sys.argv
    path_new = os.path.join(os.getcwd(), args[1])
    pages_stack = list()
    pages_dict = dict()
    if not os.access(path_new, os.F_OK):
        os.mkdir(path_new)
    while True:
        user_input = input()
        if user_input == 'exit':
            break
        elif user_input == 'back':
            if len(pages_stack) > 1:
                pages_stack.pop()
                print_from_file(pages_stack[-1])
        elif user_input in pages_dict:
            print(pages_dict[user_input])
            print_from_file(pages_dict[user_input])
        elif url_ok(user_input):
            url = user_input
            if not user_input.startswith('http'):
                url = f'http://{user_input}'
            request = get_request(url)
            if request:
                file_name = user_input.split('.')[0]
                path_to_file = os.path.join(path_new, file_name)
                text = parsing_html(request)
                print(text)
                write_to_files(path_to_file, text)
                pages_stack.append(path_to_file)
                pages_dict[file_name] = path_to_file
            else:
                print('Error: Incorrect URL')
        elif user_input in pages_dict:
            print(pages_dict[user_input])
            print_from_file(pages_dict[user_input])
        else:
            print('Error: Incorrect URL')
