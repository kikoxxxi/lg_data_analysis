import re
import csv


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
    create_csv('lg_skill', ['positionId', 'skill'])
    data = []
    for i, detail in enumerate(details):
        position_id = position_ids[i]
        detail = re.sub(r"[\\*\\.]", "", detail)
        re_word = re.compile("[a-z]+", re.I)
        words = re_word.findall(detail)
        if words:
            for word in words:
                word=word.lower()
                row = [position_id, word]
                print(row)
                data.append(row)
    append_csv('lg_skill', data)


if __name__ == '__main__':
    main()
