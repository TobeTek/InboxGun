from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import json
from blog.management.core import utils
import os
from blog import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            dest="file_name",
            default=os.path.join(
                os.path.dirname(__file__), r"../fixtures/articles.json"
            ),
            help="Name of file containing articles",
        )

        parser.add_argument(
            "--format",
            dest="file_format",
            default="json",
            help="Format of the file containing articles",
        )

    def handle(self, *args, **options):
        file_name = options.get("file_name")
        file_format = options.get("file_format")

        if file_name is None:
            raise ValueError("file can not be None.")

        with open(file_name, "r") as f:
            data = f.read()

        # TODO: Switch to OOP dict to handle different data types.
        if file_format.lower() == "json":
            data = json.loads(data)

        if set(data.keys()) != {"title", "author", "body", "status"}:
            raise ValueError(
                "The JSON file specified doesn't contain the necessary fields for Article model"
            )

        COUNTER = 0
        NO_ARTICLES = len(data["title"])
        for counter in range(NO_ARTICLES):
            models.Post.objects.create(
                title=data["title"][counter],
                author=utils.get_user(data["author"][counter]),
                body=data["body"][counter],
                status=data["status"][counter],
            )
