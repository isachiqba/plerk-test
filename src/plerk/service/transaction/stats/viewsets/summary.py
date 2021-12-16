from rest_framework import response
from rest_framework import viewsets

from .. import models


class ViewSet(viewsets.ViewSet):

  def list(self, request):
    data = {
      "company": {
        "with-less-sales": models.Company.objects.with_less_sales(),  # type: ignore
        "with-more-rejected-sales": models.Company.objects.with_more_rejected_sales(),  # type: ignore
        "with-more-sales": models.Company.objects.with_more_sales(),  # type: ignore
      },
      "transaction": {
        "charged": models.Transaction.objects.charged(),  # type: ignore
        "not-charged": models.Transaction.objects.not_charged(),  # type: ignore
      },
    }
    return response.Response(data)
