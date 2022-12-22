import os  # https://docs.python.org/3/library/os.html
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/


def save_text_from_html(input_path, output_path):
    """
    extracts text from html files in given path and saves results in given path
    """
    for filename in os.listdir(input_path):
        # print(filename)
        with open(os.path.join(input_path, filename), 'r', encoding='utf-8') as f:
            try:
                soup = BeautifulSoup(f, "html.parser")
                f.close()
                with open(output_path + '/' + filename[:-5] + '.txt', "w", encoding='utf-8') as file:
                    file.write(soup.get_text())
                file.close()
            except UnicodeEncodeError:
                print(filename)
                pass


def save_title(input_path, output_path):
    """
    saves title from every html in given path and saves results in given path
    """
    for filename in os.listdir(input_path):
        # print(filename)
        with open(os.path.join(input_path, filename), 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            head_tag = soup.find('head')
            if head_tag is not None:
                title_tag = head_tag.find('title')
                if title_tag is not None:
                    title = title_tag.string
                    with open(output_path + '/' + filename[:-5] + '.txt', "w", encoding='utf-8') as file:
                        file.write(title)
                    file.close()
                else:
                    with open(output_path + '/' + filename[:-5] + '.txt', "w", encoding='utf-8') as file:
                        file.write(' ')
                    file.close()
                    print('No title was found in the <head> section of the HTML file.')
            else:
                with open(output_path + '/' + filename[:-5] + '.txt', "w", encoding='utf-8') as file:
                    file.write(' ')
                file.close()
                print('No <head> section was found in the HTML file.')
            f.close()


def save_df_as_txt(df, output_path):
    df.to_csv(output_path, sep='\t', index=False)
