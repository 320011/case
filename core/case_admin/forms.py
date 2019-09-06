from django import forms


class TagImportForm(forms.Form):
    FILE_FORMAT_CHOICES = [
        ("auto", "Auto Detect"),
        ("csv", "Comma-separated Values (.csv)"),
        ("json", "JSON (.json)"),
        ("xlsx", "Microsoft Excel (.xlsx)"),
        ("txt", "Plain Text (.txt)"),
    ]
    file = forms.FileField(label="File")
    file_format = forms.ChoiceField(label="File Format", choices=FILE_FORMAT_CHOICES)
