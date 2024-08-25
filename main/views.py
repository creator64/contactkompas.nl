from django.http import HttpResponse
from django.template import loader

from main.models import Bedrijf


def index(request):
    template = loader.get_template("pages/index.html")
    return HttpResponse(template.render())


def search(request):
    search_filter = request.GET.get("company", "")
    companies = Bedrijf.objects.filter(name__contains=search_filter)
    template = loader.get_template("pages/search.html")
    return HttpResponse(template.render({'companies': companies, 'filter': search_filter}))


def most_popular_companies(request):
    # Min is to prevent crashing if the given number is too high
    limit = min(int(request.GET.get('limit')) if request.GET.get('limit', '').isnumeric() else -1, 2 ** 32)
    offset = min(int(request.GET.get('offset')) if request.GET.get('offset', '').isnumeric() else 1, 2 ** 32)
    try:
        # Order the objects by their popularity (!=row_number), then return the range given by the limit and offset
        objects = Bedrijf.objects.raw(
            "SELECT * FROM (SELECT *, ROW_NUMBER() OVER(ORDER BY popularity) poprank FROM main_bedrijf) "
            "WHERE poprank BETWEEN %s AND %s", [offset, 2 ** 32 if limit == -1 else offset + limit - 1])
        status = 206
    except Exception:
        objects = Bedrijf.objects.all().order_by("popularity")
        status = 200

    end_reached = True if Bedrijf.objects.count() < limit + offset else False
    template = loader.get_template("components/shared/business-card.html")
    return HttpResponse("".join(
        [template.render({"company": company}) for company in objects]
    ), status=status, headers={"end-reached": end_reached})
