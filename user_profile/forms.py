from django.forms import ModelForm, Textarea, TextInput

from user_profile.models import Profile


class ProfileAdd(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "occupation",
            "bio",
            "age",
            "sex",
            "pic",
            "bio",
        ]
        widgets = {
            "occupation": TextInput(
                attrs={"placeholder": " e.g Student at University of Lagos"}
            ),
            "bio": Textarea(attrs={"cols": 80, "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for fieldname in ["sex"]:
            self.fields[fieldname].help_text = None


class ProfileUpdate(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "occupation",
            "age",
            "sex",
            "pic",
            "bio",
        ]
        widgets = {
            "occupation": TextInput(
                attrs={"placeholder": " e.g Student at University of Lagos"}
            ),
            "bio": Textarea(attrs={"cols": 80, "rows": 5}),
        }
