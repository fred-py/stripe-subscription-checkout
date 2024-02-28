# flat_counts.py
from collections import defaultdict
import csv

authors = defaultdict(int)
publishers = defaultdict(int)

with open('./data/author_book_publisher.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = f"{row['first_name']} {row['last_name']}"

        authors[name] += 1
        publishers[row["publisher"]] += 1

print("Authors:")
for name, count in authors.items():
    print(f"   {name}:{count}")

print("Publishers:")
for publisher, count in publishers.items():
    print(f"   {publisher}:{count}")
