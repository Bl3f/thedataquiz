import csv

from django.core.management.base import BaseCommand

from app.models import Question, Tag


class Command(BaseCommand):
    help = 'Load a questions.csv'

    def handle(self, *args, **options):
        with open('app/management/commands/questions.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question, created = Question.objects.update_or_create(
                    pk=row["id"],
                    text=row["text"],
                    a=row["a"],
                    b=row["b"],
                    c=row["c"],
                    d=row["d"],
                    question_type=row["question_type"],
                    answer=row["answer"],
                )
                question.tags.add(Tag.objects.get(slug=row["tags"]))
