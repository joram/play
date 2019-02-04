from django import forms
from apps.platform.models import Player


class PlayerForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.EmailInput)

    class Meta:
        model = Player
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        player = super().save(*args, **kwargs)
        player.user.email = self.cleaned_data["email"]
        player.user.save()
        return player
