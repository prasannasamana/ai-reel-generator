from django import forms


class ReelCreateForm(forms.Form):
    """Form for creating a new reel."""
    
    TONE_CHOICES = [
        ('neutral', 'Neutral'),
        ('friendly', 'Friendly'),
        ('formal', 'Formal'),
        ('energetic', 'Energetic'),
        ('dramatic', 'Dramatic'),
    ]
    
    image = forms.ImageField(
        label='Face Image',
        help_text='Upload a clear face image for the talking head'
    )
    script = forms.CharField(
        label='Script',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        help_text='Enter the script text for the reel'
    )
    tone = forms.ChoiceField(
        choices=TONE_CHOICES,
        initial='neutral',
        help_text='Select the tone for script rewriting'
    )
    use_rewrite = forms.BooleanField(
        required=False,
        initial=True,
        help_text='Use AI to rewrite the script in the selected tone'
    )
    max_seconds = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=300,
        help_text='Optional: Target length in seconds (approximate)'
    )

