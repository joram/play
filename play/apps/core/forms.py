from django import forms

from apps.core.models import Profile, Snake


class ProfileForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    class Meta:
        model = Profile
        fields = ["optin_marketing"]
        labels = {
            "optin_marketing": "Opt in to occasional updates and marketing communication"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)
        profile.user.email = self.cleaned_data["email"]
        profile.user.save()
        return profile


class SnakeForm(forms.ModelForm):
    class Meta:
        model = Snake
        fields = ["name", "url"]
