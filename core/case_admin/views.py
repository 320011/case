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


def populate_schema(schema):
    


def render_schema(request, schema):
    c = {
        "title": "User Admin"
        "schema": schema
    }
    
    return render(request, "case-admin.html", c)
    
    
    
    
    
