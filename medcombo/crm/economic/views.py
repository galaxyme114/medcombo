from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from medcombo.configuration.usercustom.models import User
from medcombo.product.models import Product
from medcombo.crm.opportunity.models import Opportunity
from medcombo.crm.economic.forms import ProposalForm
from medcombo.crm.economic.models import Proposal_Commercial
from medcombo.crm.economic.models import Proposal_Product
from medcombo.crm.economic.models import Proposal_Opportunity
from django.http import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup
# Create your views here.

class EconomicProposal(PermissionRequiredMixin, ListView):
    permission_required = 'usercustom.sales_user'
    model = Proposal_Commercial
    #context_object_name = 'economic'
    template_name = "crm/economic/list.html"

    def get_context_data(self, **kwargs):
        context = super(EconomicProposal, self).get_context_data(**kwargs)
        #proposal_commercial = Proposal_Commercial.objects.all()
        proposal_commercial = Proposal_Opportunity.objects.select_related('commercial_oppor')
        context['proposal_commercial'] = proposal_commercial
        
        return context
        

class EconomicProposal_create(PermissionRequiredMixin, CreateView):
    permission_required = 'usercustom.sales_user'
    model = Proposal_Commercial
    form_class = ProposalForm
    template_name = "crm/economic/create.html"
    success_url = reverse_lazy('EconomicProposal')

    def get_context_data(self, **kwargs):
        context = super(EconomicProposal_create, self).get_context_data(**kwargs)
        users = User.objects.filter(lead=False,employee=False, is_superuser=False).order_by('-date_joined')
        context['users'] = users
        product = Product.objects.filter(company=1)
        context['products'] = product
        opportunity=Opportunity.objects.filter(responsible=self.request.user.id)
        #opportunity=Opportunity.objects.all()
        context['opportunity'] = opportunity
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            total_len = request.POST.get('total_len')
            total_values = request.POST.get('total_values')
            total_values_temp = total_values.split(",")
            total_len_opp = request.POST.get('total_len_opp')
            total_val_opp = request.POST.get('total_val_opp')
            total_val_opp_temp = total_val_opp.split(",")
            total_len_temp = int(total_len)
            total_len_opp_temp = int(total_len_opp)
            title = request.POST.get('title')
            commercial = request.POST.get('commercial')
            user = request.POST.get('user')
            total = request.POST.get('total')
            edit_date = request.POST.get('edit_date')
            payment_terms = request.POST.get('payment_terms')
            comment = request.POST.get('comments')
            comment_soup = BeautifulSoup(comment, 'html.parser')
            comments = comment_soup.text
            #validata = request.POST.get('validata')

            total_len_pro = []
            for i in range(total_len_temp):
                total_len_pro.append(i)
            total_pro_del = []
            for pro_del in total_values_temp:
                if pro_del != '':
                    total_pro_del.append(int(pro_del))
                else:
                    total_pro_del.append(1000)

            detect_pro = list(set(total_len_pro) - set(total_pro_del))
            total_opport = []
            for i in range(total_len_opp_temp):
                total_opport.append(i)
            total_oppor_del = []
            for opper_del in total_val_opp_temp:
                if opper_del != '':
                    total_oppor_del.append(int(opper_del))
                else:
                    total_oppor_del.append(1000)

            detect_oppor = list(set(total_opport) - set(total_oppor_del))
            flag = 1
            
            newProposal = Proposal_Commercial(
                    commercial= commercial,
                    user_id= user,
                    total= total,
                    edit_date= edit_date,
                    title= title,
                    payment_terms= payment_terms,
                    comments= comments,
                    #validata= validata,
                    flag = 1
                    )
            exist= Proposal_Commercial.objects.filter(user_id= user).count()
            
            if(exist==0):
                newProposal.save()
                neweconomic_data = Proposal_Commercial.objects.filter(flag=1)
                for neweconomic_data_pk in neweconomic_data:
                    pk = neweconomic_data_pk.pk
 
                for i in detect_pro:  
                    value_temp = 'values_'+ str(i)
                    discount_temp = 'discount_'+ str(i)
                    product_temp = 'product_'+ str(i)
                    values = request.POST.get(value_temp)
                    discount = request.POST.get(discount_temp)
                    product = request.POST.get(product_temp)
                    newProdcut = Proposal_Product(
                            commercial_prod_id= pk,
                            product_id= product,
                            value= values,
                            discount= discount
                            )
                    newProdcut.save()
                        
                for j in detect_oppor:
                    opportunity_temp = 'opportunity_'+ str(j)
                    opportunity = request.POST.get(opportunity_temp)
                    newOpportunity = Proposal_Opportunity(
                            commercial_oppor_id= pk,
                            opportunity_id= opportunity,
                            )
                    newOpportunity.save()
                neweconomic_data = Proposal_Commercial.objects.filter(flag=1).update(flag=0)
                
                return HttpResponseRedirect(reverse_lazy('EconomicProposal'))
            
            else:
                Proposal_Commercial.objects.get(user_id=user).delete()
                newProposal.save()
                neweconomic_data = Proposal_Commercial.objects.filter(flag=1)
                for neweconomic_data_pk in neweconomic_data:
                    pk = neweconomic_data_pk.pk

                for i in detect_pro:  
                    value_temp = 'values_'+ str(i)
                    discount_temp = 'discount_'+ str(i)
                    product_temp = 'product_'+ str(i)
                    values = request.POST.get(value_temp)
                    discount = request.POST.get(discount_temp)
                    product = request.POST.get(product_temp)
                    newProdcut = Proposal_Product(
                            commercial_prod_id= pk,
                            product_id= product,
                            value= values,
                            discount= discount
                            )
                    newProdcut.save()
                        
                for j in detect_oppor:
                    opportunity_temp = 'opportunity_'+ str(j)
                    opportunity = request.POST.get(opportunity_temp)
                    newOpportunity = Proposal_Opportunity(
                            commercial_oppor_id= pk,
                            opportunity_id= opportunity,
                            )
                    newOpportunity.save()
                
                neweconomic_data = Proposal_Commercial.objects.filter(flag=1).update(flag=0)
                
                return HttpResponseRedirect(reverse_lazy('EconomicProposal'))
            

class EconomicProposal_update(PermissionRequiredMixin, UpdateView):
    permission_required = 'usercustom.sales_user'
    model = Proposal_Commercial
    form_class = ProposalForm
    template_name = "crm/economic/update.html"
    success_url = reverse_lazy('EconomicProposal')  
    
    
def EconomicProposal_delete(request):
    my_id = request.POST.get('value')
    proposal = Proposal_Opportunity.objects.filter(commercial_oppor_id=my_id)
    for pro in proposal:
        pro.delete()
    product = Proposal_Product.objects.filter(commercial_prod_id=my_id)
    for produc in product:
        produc.delete()
    commercial = Proposal_Commercial.objects.get(id=my_id)
    commercial.delete()
    product.delete()
    return HttpResponse('Ok')

