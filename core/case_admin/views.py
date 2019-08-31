from django.shortcuts import render
from accounts.models import User
# from ..accounts.models import User


schema_user = {
    "endpoint": "/api/v1/user",
    "fields": {
        "first_name": {
            "title": "First Name",
            "key": "first_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 40,
            },
            "write": True,
        }, 
        "last_name": {
            "title": "Last Name",
            "key": "last_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 60,
            },
            "write": True,
        }, 
        "email": {
            "title": "Email",
            "key": "email",
            "widget": {
                "template": "w-email.html",
                "maxchars": 250,
            },
            "write": True,
        }, 
        "university": {
            "title": "University",
            "key": "university",
            "widget": {
                "template": "w-text.html",
                "maxchars": 150,
            },
            "write": True,
        }, 
        "degree_commencement_year": {
            "title": "Degree Start",
            "key": "degree_commencement_year",
            "widget": {
                "template": "w-number.html",
            },
            "write": True,
        }, 
        "is_staff": {
            "title": "Is Staff",
            "key": "is_staff",
            "widget": {
                "template": "w-checkbox.html",
                "maxchars": 40,
            },
            "write": True,
        },
    }
}

schema_case = {
    "endpoint": "/api/v1/case",
    "fields": [],
}

schema_comment = {
    "endpoint": "/api/v1/comment",
    "fields": [],
}

schema_tag = {
    "endpoint": "/api/v1/tag",
    "fields": [],
}


def populate_data(schema, model):
    records = model.objects.all()
    data = {
        "endpoint": schema["endpoint"],
        "entities": [],
    }
    # for all records in the db
    for r in records:
        row_data = []  # this rows data
        # add each field to the data
        for f in schema["fields"]:
            d = schema["fields"][f]
            d["value"] = vars(User)[f]
            d["entity"] = r.id
            row_data.append(d)
        data["entities"].append(row_data)
    return data


def view_admin_user(request):
    data = populate_data(schema_user, User)
    c = {
        "title": "User Admin",
        "data": data,
    }
    return render(request, "case-admin.html", c)


def view_admin_case(request):
    data = populate_data(schema_case, User)
    c = {
        "title": "Case Study Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_admin_comment(request):
    data = populate_data(schema_comment, User)
    c = {
        "title": "Comment Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_admin_tag(request):
    data = populate_data(schema_tag, User)
    c = {
        "title": "Tag Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_default(request):
    return render(request, "admin.html")

