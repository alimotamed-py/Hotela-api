# ==================== ADD LIBRARY AND PACKAGE ====================
import django_filters
from .models import Hotel

# ==================== HOTEL FILTER ====================
class HotelFilter(django_filters.FilterSet):

    min_star = django_filters.NumberFilter(field_name="star", lookup_expr="gte")

    max_star = django_filters.NumberFilter(field_name="star", lookup_expr="lte")

    city = django_filters.CharFilter(field_name="city__name", lookup_expr="icontains")

    class Meta:
        model = Hotel
        fields = ["city", "status"]