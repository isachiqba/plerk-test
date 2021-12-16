from django.shortcuts import get_object_or_404
from rest_framework import response
from rest_framework import serializers
from rest_framework import viewsets

from ..models import Company


class ViewSet(viewsets.ViewSet):

  class ListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
      fields = [
        "url",
        "name",
      ]
      model = Company

  class RetrieveSerializer(serializers.ModelSerializer):

    class Meta:
      extra_kwargs = {
        "day-with-more-transactions": {
          "source": "day_with_more_transactions"
        },
        "transactions-charged": {
          "source": "transactions_charged"
        },
        "transactions-not-charged": {
          "source": "transactions_not_charged"
        },
      }
      fields = [
        "id",
        "name",
        "slug",
        "day-with-more-transactions",
        "transactions-charged",
        "transactions-not-charged",
      ]
      model = Company

  def list(self, request):
    queryset = Company.objects.all()
    serializer = self.ListSerializer(queryset, context={"request": request}, many=True)
    return response.Response(serializer.data)

  def retrieve(self, request, pk):
    queryset = Company.objects.all()
    instance = get_object_or_404(queryset, pk=pk)
    serializer = self.RetrieveSerializer(instance)
    return response.Response(serializer.data)
