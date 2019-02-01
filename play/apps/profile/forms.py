from django import forms


class ProfileForm(forms.Form):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    def save(self, user):
        user.email = self.cleaned_data["email"]
        user.save()
