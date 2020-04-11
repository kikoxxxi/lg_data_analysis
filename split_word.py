import re
import csv
import jieba
import jieba.analyse


def read_csv(path, column_name):
    with open('{}.csv'.format(path), 'r') as f:
        reader = csv.DictReader(f)
        column = [row[column_name] for row in reader]
        f.close()
    return column


def create_csv(path, head):
    with open('{}.csv'.format(path), "w+", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(head)
        f.close()


def append_csv(path, data):
    with open('{}.csv'.format(path), 'a+', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)
        f.close()


def main():
    details = read_csv('./lg_position', 'detail')
    position_ids = read_csv('./lg_position', 'positionId')
    create_csv('lg_detail', ['positionId', 'word'])
    data = []
    for i, detail in enumerate(details):
        position_id = position_ids[i]
        detail = re.sub(r"[\\*\\.]", "", detail)
        re_clear = re.compile(r'^(.*?)?[:：](1)?')
        re_clear2 = re.compile('^(.*?)?1')

        if re_clear.match(detail):
            detail = re.sub(re_clear.match(detail).groups()[0], "", detail)
        if re_clear2.match(detail):
            detail = re.sub(re.escape(re_clear2.match(detail).groups()[0]), "", detail)
            words = jieba.analyse.extract_tags(detail)
            for word in words:
                row=[position_id,word]
                print(row)
                data.append(row)
    append_csv('lg_detail', data)


if __name__ == '__main__':
    main()
