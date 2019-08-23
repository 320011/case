from django.shortcuts import render


schema_user = {
    "endpoint": "/api/v1/user",
    "fields": [
        {
            "title": "First Name",
            "key": "first_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 40,
            },
            "write": true,
        }, {
            "title": "Last Name",
            "key": "last_name",
            "widget": {
                "template": "w-text.html",
                "maxchars": 60,
            },
            "write": true,
        }, {
            "title": "Email",
            "key": "email",
            "widget": {
                "template": "w-email.html",
                "maxchars": 250,
            },
            "write": true,
        }, {
            "title": "University",
            "key": "university",
            "widget": {
                "template": "w-text.html",
                "maxchars": 150,
            },
            "write": true,
        }, {
            "title": "Degree Start",
            "key": "degree_commencement_year",
            "widget": {
                "template": "w-number.html",
            },
            "write": true,
        }, {
            "title": "Is Staff",
            "key": "is_staff",
            "widget": {
                "template": "w-checkbox.html",
                "maxchars": 40,
            },
            "write": true,
        },
    ]
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
        "endpoint": schema.endpoint,
        "fields": [],
    }
    # for all records in the db
    for r in records:
        d = {}  # data to be filled
        # add each field to the data
        for f in schema.fields:
            r[f.key] = schema[f.key]
            r[f.key]["value"] = u[f.key]
            r["entity"] = u.id
        data.insert()
    return data


def view_admin_user(request):
    data = populate_data(schema_user, User)
    c = {
        "title": "User Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_admin_case(request):
    data = populate_data(schema_case, CaseStudy)
    c = {
        "title": "Case Study Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_admin_case_comment(request):
    data = populate_data(schema_comment, CaseComment)
    c = {
        "title": "Comment Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_admin_tag(request):
    data = populate_data(schema_tag, Tag)
    c = {
        "title": "Tag Admin",
        "data": data
    }
    return render(request, "case-admin.html", c)


def view_default(request):
    return render(request, "default.html")

