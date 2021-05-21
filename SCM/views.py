from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import SCM1, Agent, User, Category
from agents.mixins import OrganisorandLoginRequiredMixin
from .forms import SCMform, SCMModelForm, CustomUserCreationForm, AssignAgentForm, SCMCategoryUpdateForm



class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self): 
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render (request, "landing.html")

class SCMListView(LoginRequiredMixin, ListView):
    template_name = "SCM/SCM_list.html"
    context_object_name = "SCM"

    def get_queryset(self):
        user = self.request.user

        #initial filter for all the leads that lies under one organisation
        if user.is_organisor:
            queryset = SCM1.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False)
        else:
            queryset = SCM1.objects.filter(organisation=user.agent.organisation,agent__isnull=False)
            #filtering leads for our current agent who is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SCMListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = SCM1.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
                )
        context.update({
            "unassigned_leads": queryset
        })
        return context

def SCM_list (request):
    SCM = SCM1.objects.all()
    context = {
        "SCM" : SCM
    }
    return render (request, "SCM/SCM_list.html", context)

class SCMDetailView(LoginRequiredMixin, DetailView):
    template_name = "SCM/SCM_detail.html"
    context_object_name = "SCM"

    def get_queryset(self):
        user = self.request.user

        #initial filter for all the leads that lies under one organisation
        if user.is_organisor:
            queryset = SCM1.objects.filter(organisation=user.userprofile)
        else:
            queryset = SCM1.objects.filter(organisation=user.agent.organisation)
            #filtering leads for our current agent who is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset

def SCM_detail (request, pk):
    SCM = SCM1.objects.get(id=pk)
    context = {
        "SCM" : SCM
    }
    return render (request, "SCM/SCM_detail.html", context)

class SCMCreateView(OrganisorandLoginRequiredMixin, CreateView):
    template_name = "SCM/SCM_create.html"
    form_class = SCMModelForm
    
    def get_success_url(self): 
        return reverse("SCM:SCM-list")

    def form_valid(self, form):
        SCM = form.save(commit=False)
        SCM.organisation = self.request.user.userprofile
        SCM.save()
        #to send mails
        send_mail(
            subject="A new entry has been added",
            message="Go to site to see the recently added entry",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(SCMCreateView,self).form_valid(form)

def SCM_create (request):
    form = SCMModelForm()
    if request.method == "POST":
        form = SCMModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/SCM')
    context = {
        "form" : form
    }
    return render (request, "SCM/SCM_create.html",context)

class SCMUpdateView(OrganisorandLoginRequiredMixin, UpdateView):
    template_name = "SCM/SCM_update.html"
    form_class = SCMModelForm

    def get_queryset(self):
        user = self.request.user
        return SCM1.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self): 
        return reverse("SCM:SCM-list")

def SCM_update(request, pk):
    SCM = SCM1.objects.get(id=pk)
    form = SCMModelForm(instance=SCM)
    if request.method == "POST":
        form = SCMModelForm(request.POST, instance=SCM)
        if form.is_valid():
            form.save()
            return redirect('/SCM')
    context = {
        "form" : form,
        "SCM" : SCM
    }

    return render (request, "SCM/SCM_update.html",context)


class SCMDeleteView(OrganisorandLoginRequiredMixin, DeleteView):
    template_name = "SCM/SCM_delete.html"
    
    def get_success_url(self): 
        return reverse("SCM:SCM-list")

    def get_queryset(self):
        user = self.request.user
        return SCM1.objects.filter(organisation=user.userprofile)

def SCM_delete(request, pk):
    SCM = SCM1.objects.get(id=pk)
    SCM.delete()
    return redirect('/SCM')

class AssignAgentView(OrganisorandLoginRequiredMixin, generic.FormView):
    template_name = "SCM/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self): 
        return reverse("SCM:SCM-list")

    def form_valid(self,form):
        agent= form.cleaned_data["agent"]
        lead = SCM1.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):


    template_name = "SCM/category_list.html"
    context_object_name = "category_list"
    

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = SCM1.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = SCM1.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context 

    def get_queryset(self):
        user = self.request.user

        #initial filter for all the leads that lies under one organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "SCM/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class SCMCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "SCM/SCM_category_update.html"
    form_class = SCMCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user

        #initial filter for all the leads that lies under one organisation
        if user.is_organisor:
            queryset = SCM1.objects.filter(organisation=user.userprofile)
        else:
            queryset = SCM1.objects.filter(organisation=user.agent.organisation)
            #filtering leads for our current agent who is logged in 
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_success_url(self):
        return reverse("SCM:SCM-detail", kwargs={"pk":self.get_object().id})




# def SCM_update(request, pk):
#     SCM = SCM1.objects.get(id=pk)
#     form = SCMForm()
#     if request.method == "POST":
#         form = SCMForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             SCM.first_name = first_name
#             SCM.last_name = last_name
#             SCM.age = age
#             SCM.save()
#             return redirect('/SCM')
    # context = {
    #     "form" : form,
    #     "SCM" : SCM
    # }
#     return render (request, "SCM/SCM_update.html",context)



# def SCM_create (request):
    # form = SCMForm()
    # if request.method == "POST":
    #     form = SCMForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         SCM1.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age= age,
    #             agent= agent
    #         )
    #         return redirect('/SCM')
    # context = {
    #     "form" : form
    # }
#     return render (request, "SCM/SCM_create.html",context)
