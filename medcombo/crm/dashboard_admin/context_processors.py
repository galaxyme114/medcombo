from .models import CompanyLogo


def get_company_logos(request):

    company_logos = CompanyLogo.objects.all()

    return {
        'company_logos': company_logos
    }


    