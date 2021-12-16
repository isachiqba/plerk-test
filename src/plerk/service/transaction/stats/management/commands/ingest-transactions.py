import csv
from typing import Union
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import CommandParser
from django.db import transaction
from django.db.models.functions import Lower
from django.template.defaultfilters import pluralize
from django.utils.text import slugify
from wasabi import msg

from ... import models


def confirmed(msg: str):
  """
  Utility function for asking user confirmation, treating input Exceptions as a negative answer, e.g. KeyboardInterrupt
  """
  try:
    return input(f"{msg}. Continue (y/N)? ") == "y"
  except EOFError:
    return False


class Company(object):
  """
  Utility class for handling Companies, using the `slug` for object identity. To accomplish this, we need to implement
  the following magic methods:

  `__eq__`: Allows to compare:
    1.- `self: Company` with `other: Company` using the `slug` attribute of both objects
    2.- `self: Company` with `other: str` using the `slug` attribute of `self` and `other`

  `__hash__`: It is required that objects that compare equal must have the same hash value
  
  `__str__`: Allows to use directly on django queries
  """

  def __init__(self, name: str):
    self.name = name
    self.slug = slugify(name)

  def __hash__(self):
    return hash(self.slug)

  def __str__(self):
    return self.slug

  def __eq__(self, other: Union["Company", str]):
    return self.slug == (other.slug if isinstance(other, Company) else other)


class Command(BaseCommand):

  help = "Injest Transactions from CSV file(s)"

  def add_arguments(self, parser: CommandParser):
    parser.add_argument("--clear", action="store_true", help="Clear existing Companies|Transactions before ingesting")
    parser.add_argument("--no-input", action="store_false", dest="interactive", help="Do NOT prompt user for anything")
    parser.add_argument("files", nargs="+")

  def do_handle_clear(self):
    if self.options["clear"]:
      if self.options["interactive"] and not confirmed("Remove existing Transactions and Companies"):
        raise CommandError("Interrupted by user request")
      for cls in (models.Transaction, models.Company):
        count, deleted = cls.objects.all().delete()
        if count:
          self.stdout.write(self.style.NOTICE(f"Deleted {deleted}"))

  def do_parse_csvfile(self, file: str):
    self.stdout.write(self.style.SUCCESS(f"=========================== {file} ==========================="))
    known_field_names = ["company", "price", "date", "status_transaction", "status_approved"]
    with open(file, "r") as fp:
      rows = csv.reader(fp)
      field_names = next(rows)
      # do a simple check to confirm the file data is in the format we handle
      if field_names != known_field_names:
        raise CommandError("{} != {}".format(field_names, known_field_names))
      return [(
        Company(row[0]),
        {
          "price": row[1],
          "date": row[2],
          "status": row[3],
          "approved": row[4] == "true",
        },
      ) for row in rows]

  def do_update_companies_map(self, companies_set):
    existing_companies = models.Company.objects.filter(slug__in=companies_set).values_list("id", "slug")
    self.companies_map.update({slug: id for id, slug in existing_companies})
    missing_companies = companies_set - self.companies_map.keys()
    objs_created = models.Company.objects.bulk_create(
      [models.Company(name=company.name, slug=company.slug) for company in missing_companies],
      batch_size=1000,
      ignore_conflicts=False,
    )
    self.companies_map.update({company.slug: company.id for company in objs_created})
    count = len(objs_created)
    self.stdout.write(self.style.SUCCESS(f"✔ Created {count} Compan{pluralize(count, 'y,ies')}"))

  @transaction.atomic
  def handle(self, *args, **options):
    self.companies_map: dict[str, int] = {}
    self.options = options
    self.do_handle_clear()
    for file in self.options["files"]:
      data = self.do_parse_csvfile(file)
      # 1. `sort` using the `name` attribute, for prioritizing names with uppercase letters
      # 2. `convert-to-set` for removing duplicates
      companies_set = set(sorted([company for company, _ in data if company.name], key=lambda company: company.name))
      self.do_update_companies_map(companies_set)
      objs_created = models.Transaction.objects.bulk_create(
        [models.Transaction(**attrs, company_id=self.companies_map.get(company.slug)) for company, attrs in data],
        batch_size=1000,
        ignore_conflicts=False,
      )
      count = len(objs_created)
      self.stdout.write(self.style.SUCCESS(f"✔ Created {count} Transaction{pluralize(count)}"))
