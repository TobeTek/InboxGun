from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import random
import json
from collections import defaultdict


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--n", dest="no", default=20, help="Number of articles to create"
        )

    def handle(self, *args, **options):
        N = int(options.get("no"))

        fake = Faker()
        Faker.seed(0)

        DATA = defaultdict(list)

        for _ in range(N):
            DATA["title"].append(fake.catch_phrase())
            DATA["author"].append(fake.first_name())
            DATA["body"].append(fake.text(max_nb_chars=2000))
            DATA["status"].append(random.choice(("draft", "published")))

        data = json.dumps(DATA)

        outfile = os.path.join(os.path.dirname(__file__), r"../fixtures/articles.json")
        with open(outfile, "w") as f:
            f.write(data)
