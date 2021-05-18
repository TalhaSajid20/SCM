from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import SCM1, Agent
from .forms import SCMform, SCMModelForm

class LandingPageView(TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render (request, "landing.html")

class SCMListView(ListView):
    template_name = "SCM/SCM_list.html"
    queryset = SCM1.objects.all()
    context_object_name = "SCM"

def SCM_list (request):
    SCM = SCM1.objects.all()
    context = {
        "SCM" : SCM
    }
    return render (request, "SCM/SCM_list.html", context)

class SCMDetailView(DetailView):
    template_name = "SCM/SCM_detail.html"
    queryset = SCM1.objects.all()
    context_object_name = "SCM"

def SCM_detail (request, pk):
    SCM = SCM1.objects.get(id=pk)
    context = {
        "SCM" : SCM
    }
    return render (request, "SCM/SCM_detail.html", context)

class SCMCreateView(CreateView):
    template_name = "SCM/SCM_create.html"
    form_class = SCMModelForm
    
    def get_success_url(self): 
        return reverse("SCM:SCM-list")

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

class SCMUpdateView(UpdateView):
    template_name = "SCM/SCM_update.html"
    queryset = SCM1.objects.all()
    form_class = SCMModelForm
    
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


class SCMDeleteView(DeleteView):
    template_name = "SCM/SCM_delete.html"
    queryset = SCM1.objects.all()
    
    def get_success_url(self): 
        return reverse("SCM:SCM-list")

def SCM_delete(request, pk):
    SCM = SCM1.objects.get(id=pk)
    SCM.delete()
    return redirect('/SCM')




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