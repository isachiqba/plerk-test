from uuid import uuid4
from django.db import models

from .. import util
from .transaction import TransactionStatus


class QuerySet(models.QuerySet):

  def with_less_sales(self, fmt_cents_to_basic_unit=True):
    value = self.filter(
      transactions__approved=True,
      transactions__status=TransactionStatus.CLOSED,
    ).annotate(
      total=models.Sum("transactions__price"),
    ).values(
      "id",
      "name",
      "total",
    ).order_by(
      "total",
    ).first()
    if fmt_cents_to_basic_unit and value:
      value["total"] = util.fmt_cents_to_basic_unit(value["total"])
    return value

  def with_more_rejected_sales(self, fmt_cents_to_basic_unit=True):
    value = self.filter(
      transactions__approved=False,
    ).annotate(
      total=models.Count("transactions__id"),
    ).values(
      "id",
      "name",
      "total",
    ).order_by(
      "-total",
    ).first()
    if fmt_cents_to_basic_unit and value:
      value["total"] = util.fmt_cents_to_basic_unit(value["total"])
    return value

  def with_more_sales(self, fmt_cents_to_basic_unit=True):
    value = self.filter(
      transactions__approved=True,
      transactions__status=TransactionStatus.CLOSED,
    ).annotate(
      total=models.Sum("transactions__price"),
    ).values(
      "id",
      "name",
      "total",
    ).order_by(
      "-total",
    ).first()
    if fmt_cents_to_basic_unit and value:
      value["total"] = util.fmt_cents_to_basic_unit(value["total"])
    return value


class Company(models.Model):

  id = models.UUIDField(default=uuid4, primary_key=True)

  name = models.CharField(max_length=100, unique=True)

  slug = models.SlugField(max_length=100)

  active = models.BooleanField(default=True)

  objects = QuerySet.as_manager()

  class Meta:
    constraints = [
      models.CheckConstraint(check=~models.Q(name=""), name="company-name-non-empty"),
      models.CheckConstraint(check=~models.Q(slug=""), name="company-slug-non-empty"),
    ]
    db_table = "company"

  def transactions_charged(self):
    return self.transactions.filter(  # type:ignore
      approved=True,
      status=TransactionStatus.CLOSED,
    ).aggregate(
      count=models.Count("id"),
    )

  def transactions_not_charged(self):
    return self.transactions.exclude(  # type:ignore
      approved=True,
      status=TransactionStatus.CLOSED,
    ).aggregate(
      count=models.Count("id"),
    )

  def day_with_more_transactions(self):
    return self.transactions.annotate(  # type:ignore
      value=models.F("date__date")
    ).values(
      "value",
    ).annotate(
      count=models.Count("id"),
    ).order_by(
      "-count",
    ).values(
      "value",
      "count",
    ).first()
