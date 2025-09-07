from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json

from u_table.forms import InfoForm
from u_table.models import InfoTable, UpdatedInfoTable


def index(request):
    # Test comment
    info_list = InfoTable.objects.order_by('name')
    updated_info_list = UpdatedInfoTable.objects.order_by('name')
    dict = {'info_list': info_list, 'updated_info_list': updated_info_list}
    return render(request, 'index.html', context=dict)


def info_form(request):
    form = InfoForm()
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
    dict = {'title': "Add User Info", 'form': form}
    return render(request, 'info_form.html', context=dict)


def get_data(request):
    if request.method == 'GET':
        instances = list(InfoTable.objects.values())
        return JsonResponse({'data': instances})


@csrf_exempt
def update_data(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    results = []
    for record in body:
        record_id = record.get('id')
        name = record.get('name')
        amount = record.get('amount')
        remarks = record.get('remarks')
        try:
            record_id = int(record_id)
        except (ValueError, TypeError):
            results.append({'id': record_id, 'status': 'error', 'error': 'Invalid ID format'})
            continue
        if not all([name, amount]):
            results.append({'id': record_id, 'status': 'error', 'error': 'Missing name or amount'})
            continue
        try:
            amount = Decimal(amount)
        except (ValueError, TypeError):
            results.append({'id': record_id, 'status': 'error', 'error': 'Invalid amount format'})
            continue

        if not InfoTable.objects.filter(id=record_id).exists():
            results.append({'id': record_id, 'status': 'error', 'error': f'ID {record_id} not found'})
            continue
        try:
            obj = UpdatedInfoTable.objects.get(id=record_id)
            # Compare values
            if obj.name != name or obj.updated_amount != amount or obj.remarks != remarks:
                obj.name = name
                obj.updated_amount = amount
                obj.remarks = remarks
                obj.save()
                status = 'updated'
            else:
                status = 'unchanged'
        except UpdatedInfoTable.DoesNotExist:
            obj = UpdatedInfoTable.objects.create(
                id=record_id,
                name=name,
                updated_amount=amount,
                remarks=remarks
            )
            status = 'inserted'
        results.append({'id': record_id, 'status': status})
    return JsonResponse({'results': results})

#Bulk Edit
@csrf_exempt
def update_user(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data_list = json.loads(request.body.decode('utf-8'))

            for record in data_list:
                user_id = record.get("id")
                name = record.get("name", "").strip()
                amount = record.get("amount", "").strip()
                remarks = record.get("remarks", "").strip()

                if not name:
                    # Skip rows with empty name
                    continue

                # Update the record
                user = InfoTable.objects.get(id=user_id)
                user.name = name
                user.amount = amount
                user.remarks = remarks
                user.save()

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


#Single Row Edit
def update_single_user(request, user_id):
    single_info = get_object_or_404(InfoTable, id=user_id)

    if request.method == 'POST':
        single_info.name = request.POST.get('name')
        single_info.amount = request.POST.get('amount')
        single_info.remarks = request.POST.get('remarks')
        single_info.save()
        return redirect('u_table:index')

    return render(request, 'update_user.html', {'single_info': single_info})

















#bulk edit
# def update_user(request):
#     if request.method == 'POST':
#         for user in InfoTable.objects.all():
#             name = request.POST.get(f"name_{user.id}")
#             amount = request.POST.get(f"amount_{user.id}")
#             remarks = request.POST.get(f"remarks_{user.id}")
#
#             user.name = name
#             user.amount = amount
#             user.remarks = remarks
#             user.save()
#
#         return redirect('u_table:index')
#
#     instances = InfoTable.objects.all()
#     return render(request, 'update_user.html', {'instances': instances})
# def update_user(request):
#     if request.method == 'POST':
#         for user in InfoTable.objects.all():
#             name = request.POST.get(f"name_{user.id}")
#             amount = request.POST.get(f"amount_{user.id}")
#             remarks = request.POST.get(f"remarks_{user.id}")
#
#             user.name = name
#             user.amount = amount
#             user.remarks = remarks
#             user.save()
#
#         return index(request)
#     instances = InfoTable.objects.all()
#     return render(request, 'update_user.html', {'instances': instances})


# def update_single_user(request, user_id):
#     flag = False
#     user = InfoTable.objects.get(id=user_id)
#     if not user:
#         return redirect('u_table:index')  # if no record found
#
#     if request.method == 'POST':
#         user.name = request.POST.get('name')
#         user.amount = request.POST.get('amount')
#         user.remarks = request.POST.get('remarks')
#         user.save()
#         flag = True
#         return redirect('u_table:index')
#
#     dict = {
#         'user': user,
#         'flag': flag,
#     }
#     return render(request, 'update_user.html', context=dict)

# def update_single_user(request, user_id=None):
#     instances = InfoTable.objects.all()   # for showing bulk list
#     single_info = None
#
#     if user_id:   # fetch single record if id is given
#         single_info = get_object_or_404(InfoTable, id=user_id)
#
#     # ---- Handle POST ----
#     if request.method == 'POST' and single_info:
#         single_info.name = request.POST.get('name')
#         single_info.amount = request.POST.get('amount')
#         single_info.remarks = request.POST.get('remarks')
#         single_info.save()
#         return redirect('u_table:index')
#
#     context = {
#         'instances': instances,      # FIX: match template loop
#         'single_info': single_info
#     }
#     return render(request, 'update_user.html', context=context)
