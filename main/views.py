from django.http import HttpResponse
from django.template import loader
from .utils import remove_multiple_characters, sql_nested_replace

from main.models import Bedrijf


def index(request):
    template = loader.get_template("pages/index.html")
    return HttpResponse(template.render())


def search(request):
    search_query = request.GET.get("company", "")

    chars_to_remove = [" ", "&", "-"]
    reduced_filter = remove_multiple_characters(search_query, *chars_to_remove)
    sql_replace_string = sql_nested_replace("name", *chars_to_remove)
    companies = Bedrijf.objects.raw(
        f"select name from main_bedrijf where {sql_replace_string} like %s",
        # No danger of sql injection as sql_replace_string cannot be changed by a user in any way
        [f"%{reduced_filter}%"]
    )

    template = loader.get_template("pages/search.html")
    return HttpResponse(template.render({'companies': companies, 'query': search_query}))


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
