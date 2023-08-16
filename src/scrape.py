import requests
from bs4 import BeautifulSoup


def save_problems():
    """
    スクレイピングして英単語とその和訳をファイルに保存
    """
    url = "http://www7b.biglobe.ne.jp/~browneye/english/TOEIC400-1.htm"

    r = requests.get(url)
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text, features="html.parser")

    td_list = soup.find_all("td")
    
    td_values = [x.text for x in td_list]
    # print(td_values)

    splited_list = []
    for index in range(0, len(td_values), 4):
        a = td_values[index: index + 4]

        if a[0] == '\u3000':
            continue
        if " " in a[1]:  # 一単語のもの以外は削除
            continue
        splited_list.append(a)

    with open("words.txt", "w") as f:
        for value in splited_list:
            f.write(f"{value[1]}, {value[2]}\n")


def main():
    save_problems()

    with open("db/words.txt", "r") as f:
        problems = f.readlines()
        problems = [x.strip() for x in problems]
        # print(problems)

    for p in problems:
        x = p.split(",")

        english = x[0]
        japanese = x[1]

        print(x)


if __name__ == "__main__":
    main()