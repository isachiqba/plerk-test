from uuid import uuid4
from django.db import models

from .. import util


class QuerySet(models.QuerySet):

  def charged(self, fmt_cents_to_basic_unit=True):
    value = self.filter(
      approved=True,
      status=TransactionStatus.CLOSED,
    ).aggregate(
      total=models.Sum("price"),
    )
    if fmt_cents_to_basic_unit:
      if value["total"] is not None:
        value["total"] = util.fmt_cents_to_basic_unit(value["total"])
    return value

  def not_charged(self, fmt_cents_to_basic_unit=True):
    value = self.exclude(
      approved=True,
      status=TransactionStatus.CLOSED,
    ).aggregate(
      total=models.Sum("price"),
    )
    if fmt_cents_to_basic_unit:
      if value["total"] is not None:
        value["total"] = util.fmt_cents_to_basic_unit(value["total"])
    return value


class TransactionStatus(models.TextChoices):
  CLOSED = "closed"
  PENDING = "pending"
  REVERSED = "reversed"


class Transaction(models.Model):

  id = models.UUIDField(default=uuid4, primary_key=True)

  date = models.DateTimeField()

  price = models.PositiveBigIntegerField()

  Status = TransactionStatus
  status = models.CharField(choices=TransactionStatus.choices, max_length=20)

  approved = models.BooleanField()

  company = models.ForeignKey(
    to="Company",
    null=True,
    on_delete=models.PROTECT,
    related_name="transactions",
  )

  objects = QuerySet.as_manager()

  class Meta:
    constraints = []
    db_table = "transaction"

  @property
  def charged(self):
    return self.approved and self.status == TransactionStatus.CLOSED
