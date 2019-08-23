import json



schema = {
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
            "widget": 
                "template": "w-email.html",
                "maxchars": 250,
            },,
            "write": true,
        }, {
            "title": "University",
            "key": "university",
            "widget": 
                "template": "w-text.html",
                "maxchars": 150,
            },,
            "write": true,
        }, {
            "title": "Degree Start",
            "key": "degree_commencement_year",
            "widget": 
                "template": "w-number.html",
            },
            "write": true,
        }, {
            "title": "Is Staff",
            "key": "is_staff",
            "widget": 
                "template": "w-checkbox.html",
                "maxchars": 40,
            },
            "write": true,
        },
    ]
}


def populate_data(schema):
    users = User.objects.all()
    data = {
        "fields": [],
    }
    # add all users in the db
    for u in users:
        du = {}  # data user to be filled
        # add each field to the data user
        for f in schema.fields:
            du[f.key] = schema[f.key]
            du[f.key]["value"] = u[f.key]
            du["rowId"] = u.id
        data.insert()


def render_schema(request, schema):
    c = {
        "title": "User Admin"
        "schema": schema
    }
    
    return render(request, "case-admin.html", c)
    
    
    
    
    
