from django.views import generic
from leads.models import Agent,User
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
# Create your views here.

class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'
    model=Agent
    context_object_name='agents'

    def get_queryset(self):
       organisation=self.request.user.userprofile
       return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name='agents/agent_create.html'
    form_class=AgentModelForm
    success_url=reverse_lazy('agents:agent-list')

    def form_valid(self, form):
        user=form.save(commit=False)
        user.is_organisor=False
        user.is_agent=True
        user.set_password('testahg')
        user.save()
        Agent.objects.create(user=user,organisation=self.request.user.userprofile)
        send_mail(subject='you are invited as an agent',message='you were added as an agent on DJCRM. Please come and login and start working',
                  recipient_list=[user.email],from_email='DJCRM@adminUser.com')
        return super(AgentCreateView,self).form_valid(form)


class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    model=Agent
    template_name='agents/agent_detail.html'
    
    def get_queryset(self):
       organisation=self.request.user.userprofile
       return Agent.objects.filter(organisation=organisation)
    
class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name='agents/agent_update.html'
    success_url=reverse_lazy('agents:agent-list')
    form_class=AgentModelForm
    model=User

    def get_queryset(self):
    #    organisation=self.request.user.userprofile
    #    return Agent.objects.filter(organisation=organisation)
       return User.objects.all()

class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    model=Agent
    success_url=reverse_lazy('agents:agent-list')
    template_name='agents/agent_delete.html'
    
    def get_queryset(self):
       organisation=self.request.user.userprofile
       return Agent.objects.filter(organisation=organisation)