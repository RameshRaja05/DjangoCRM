from typing import Any
from django.core.mail import send_mail
from django.db import models
from .models import Lead,Agent,Category
from django.urls import reverse,reverse_lazy
from .forms import LeadForm,CustomUserCreationForm,AssignAgentForm,LeadCategoryUpdateForm,CategoryForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
# Create your views here.

class SignUpView(generic.CreateView):
    form_class=CustomUserCreationForm
    template_name='registration/signup.html'

    def form_valid(self, form):
        response=super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request,user)
        return response
    
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')


class LandingPageView(generic.TemplateView):
    template_name='landing-page.html'


class LeadListView(LoginRequiredMixin,generic.ListView):
    model=Lead
    template_name="leads/lead_list.html"
    context_object_name="leads"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile,agent__isnull=False)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            queryset=queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context=super(LeadListView,self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
            context.update({
                 'unassigned_leads':queryset.filter(agent__isnull=True)
                })
        return context



class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    model=Lead
    template_name="leads/lead_detail.html"

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            queryset=queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    model=Lead
    template_name='leads/lead_create.html'
    success_url=reverse_lazy('leads:lead-list')
    form_class=LeadForm

    def form_valid(self,form) :
        lead=form.save(commit=False)
        lead.organisation=self.request.user.userprofile
        lead.save()
        #send notification to agent mail
        return super(LeadCreateView,self).form_valid(form)
    
class AssignAgentView(OrganisorAndLoginRequiredMixin,generic.FormView):
    template_name='leads/assign_agent.html'
    form_class=AssignAgentForm
    success_url=reverse_lazy('leads:lead-list')

    def get_form_kwargs(self,**kwargs):
        kwargs=super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request':self.request
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        lead=Lead.objects.get(pk=self.kwargs['pk'])
        lead.agent=form.cleaned_data.get('agent')
        lead.save()
        return super(AssignAgentView,self).form_valid(form)

class LeadUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    model=Lead
    template_name='leads/lead_update.html'
    success_url=reverse_lazy('leads:lead-list')
    form_class=LeadForm

    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    


# def lead_update(request,pk):
#     lead=Lead.objects.get(pk=pk)
#     form=LeadForm(instance=lead)
#     if request.method=='POST':
#         #pass a lead data in here otherwise it'd create a new entry
#         form=LeadForm(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect(f'/leads')
#     return render(request,'leads/lead_update.html',{"form":form,"lead":lead})

class LeadDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name='leads/lead_delete.html'
    model=Lead
    success_url=reverse_lazy('leads:lead-list')
    
    def get_queryset(self):
        user=self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name='leads/category_list.html'
    model=Category
    context_object_name='categories'

    def get_context_data(self, **kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
        context.update({
            'unassigned_leads':queryset.filter(category__isnull=True).count(),
        })
        return context

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset
    
class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name='leads/category_detail.html'
    model=Category
    context_object_name='category'

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset
    
class CategoryCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name='leads/category_create.html'
    model=Category
    form_class=CategoryForm

    def get_success_url(self) -> str:
        return reverse('leads:category-list')
    
    def form_valid(self,form) :
        category=form.save(commit=False)
        category.organisation=self.request.user.userprofile
        category.save()
        #send notification to agent mail
        return super(CategoryCreateView,self).form_valid(form)

class CategoryUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name='leads/category_update.html'
    model=Category
    form_class=CategoryForm

    def get_success_url(self) -> str:
        return reverse('leads:category-list')
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name="leads/category_delete.html"
    model=Category
    
    def get_success_url(self) -> str:
        return reverse('leads:category-list')
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else:
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name='leads/lead_category_update.html'
    model=Lead
    form_class=LeadCategoryUpdateForm

    def get_success_url(self) -> str:
        return reverse('leads:lead-detail',kwargs={'pk':self.get_object().id})
    
    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset=Lead.objects.filter(organisation=user.agent.organisation)
            queryset=queryset.filter(agent__user=user)
        return queryset