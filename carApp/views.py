from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from carApp.forms import RepairForm
from carApp.models import Repair


# Create your views here.

def index(request):
    return render(request, 'index.html')


def repairs(request):
    repair = Repair.objects.all()
    if request.method == 'POST':
        form = RepairForm(request.POST, request.FILES)
        if form.is_valid():
            repair = form.save(commit=False)
            repair.user = request.user
            repair.image = form.cleaned_data['image']
            repair.save()
            return redirect('repairs')
    else:
        form = RepairForm()

    context = {'repairs': repair, 'form': form}
    return render(request, 'repairs.html', context=context)


def deleteRepair(request, repair_id):
    repair = Repair.objects.filter(id=repair_id).get()
    if request.method == 'POST':
        repair.delete()
        return redirect('repairs')
    else:
        return redirect('repairs')


def editRepair(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    if request.method == 'POST':
        form = RepairForm(request.POST, request.FILES, instance=repair)
        if form.is_valid():
            form.save()
            return redirect('repairs')
    else:
        form = RepairForm(instance=repair)

    return render(request, 'edit.html', {'form': form})
