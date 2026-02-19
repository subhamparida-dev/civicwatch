from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Issue, Area, Department


def home(request):
    return render(request, "home.html")


def report_issue(request):

    areas = Area.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":
        Issue.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            category=request.POST.get("category"),
            area=Area.objects.get(id=request.POST.get("area")),
            severity=request.POST.get("severity"),
            reported_by=request.user,
            assigned_department=Department.objects.get(id=request.POST.get("department"))
        )

        return redirect("/issues/")

    return render(request, "report.html", {
        "areas": areas,
        "departments": departments
    })


def issue_list(request):
    issues = Issue.objects.all().order_by('-priority_score')

    search = request.GET.get('search')
    area = request.GET.get('area')
    category = request.GET.get('category')
    status = request.GET.get('status')

    if search:
        issues = issues.filter(title__icontains=search)

    if area:
        issues = issues.filter(area_id=area)

    if category:
        issues = issues.filter(category=category)

    if status:
        issues = issues.filter(status=status)

    areas = Area.objects.all()

    return render(request, "issues.html", {
        "issues": issues,
        "areas": areas,
    })


def dashboard(request):

    total_issues = Issue.objects.count()
    open_issues = Issue.objects.filter(status='open').count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    high_priority = Issue.objects.filter(priority_score__gte=15).count()

    area_stats = Area.objects.annotate(issue_count=Count('issue'))
    department_stats = Department.objects.annotate(issue_count=Count('issue'))

    return render(request, "dashboard.html", {
        "total_issues": total_issues,
        "open_issues": open_issues,
        "resolved_issues": resolved_issues,
        "high_priority": high_priority,
        "area_stats": area_stats,
        "department_stats": department_stats,
    })
