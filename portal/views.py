import csv
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecordForm, RegisterForm
from .models import Record

TYPE_NAMES = dict(Record.TYPES)


def reviewer_required(view):
    """Only staff users (HOD / admin) may open the view."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return login_required(wrapper)


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created. Welcome!')
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    mine = Record.objects.filter(faculty=request.user)
    stats = {
        'total': mine.count(),
        'approved': mine.filter(status='approved').count(),
        'pending': mine.filter(status='pending').count(),
        'rejected': mine.filter(status='rejected').count(),
    }
    year = request.GET.get('year', '').strip()
    rtype = request.GET.get('type', '').strip()
    records = mine
    if year.isdigit():
        records = records.filter(year=int(year))
    if rtype:
        records = records.filter(record_type=rtype)
    return render(request, 'dashboard.html', {
        'records': records, 'stats': stats,
        'year': year, 'rtype': rtype, 'types': Record.TYPES,
    })


@login_required
def add_record(request):
    form = RecordForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        rec = form.save(commit=False)
        rec.faculty = request.user
        rec.save()
        messages.success(request, 'Record submitted for approval.')
        return redirect('dashboard')
    return render(request, 'record_form.html', {'form': form, 'heading': 'Add record'})


@login_required
def edit_record(request, pk):
    rec = get_object_or_404(Record, pk=pk, faculty=request.user)
    form = RecordForm(request.POST or None, request.FILES or None, instance=rec)
    if request.method == 'POST' and form.is_valid():
        rec = form.save(commit=False)
        rec.status = 'pending'   # any edit goes back for approval
        rec.remarks = ''
        rec.save()
        messages.success(request, 'Record updated and re-submitted for approval.')
        return redirect('dashboard')
    return render(request, 'record_form.html', {'form': form, 'heading': 'Edit record'})


@login_required
def delete_record(request, pk):
    rec = get_object_or_404(Record, pk=pk, faculty=request.user)
    if request.method == 'POST':
        rec.delete()
        messages.success(request, 'Record deleted.')
    return redirect('dashboard')


@reviewer_required
def review(request):
    status = request.GET.get('status', 'pending')
    if status not in ('pending', 'approved', 'rejected'):
        status = 'pending'
    records = Record.objects.filter(status=status).select_related('faculty__profile')
    return render(request, 'review.html', {'records': records, 'status': status})


@reviewer_required
def decide(request, pk, action):
    if request.method == 'POST' and action in ('approved', 'rejected'):
        rec = get_object_or_404(Record, pk=pk)
        rec.status = action
        rec.remarks = request.POST.get('remarks', '').strip()
        rec.save()
        messages.success(request, f'Record {action}.')
    return redirect('review')


@reviewer_required
def report(request):
    approved = Record.objects.filter(status='approved')
    by_type = [(TYPE_NAMES.get(r['record_type'], r['record_type']), r['n'])
               for r in approved.values('record_type').annotate(n=Count('id')).order_by('-n')]
    by_year = [(r['year'], r['n'])
               for r in approved.values('year').annotate(n=Count('id')).order_by('year')]
    by_dept = [(r['faculty__profile__department'] or 'N/A', r['n'])
               for r in approved.values('faculty__profile__department').annotate(n=Count('id')).order_by('-n')]
    chart = {'labels': [str(y) for y, _ in by_year], 'data': [n for _, n in by_year]}
    return render(request, 'report.html', {
        'by_type': by_type, 'by_year': by_year, 'by_dept': by_dept,
        'chart': chart, 'total': approved.count(),
    })


@reviewer_required
def export_csv(request):
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="faculty_records.csv"'
    w = csv.writer(resp)
    w.writerow(['Faculty', 'Department', 'Type', 'Title', 'Year', 'Details', 'Status', 'Remarks'])
    for r in Record.objects.select_related('faculty__profile'):
        profile = getattr(r.faculty, 'profile', None)
        w.writerow([
            r.faculty.get_full_name() or r.faculty.username,
            profile.department if profile else '',
            r.get_record_type_display(), r.title, r.year,
            r.details, r.get_status_display(), r.remarks,
        ])
    return resp
