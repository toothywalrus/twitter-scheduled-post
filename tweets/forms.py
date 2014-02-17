import floppyforms as forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field


from djangular.forms.angular_model import NgModelFormMixin
# from djangular.forms import NgFormValidationMixin

from .models import Tweet, PostTweetSet, PeriodicTweet, TimedTweet
from .utils import get_model_name, get_form_id


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class StatusInput(forms.Textarea):
    rows = 4


class TweetHelper(FormHelper):
    form_show_errors = False
    #form_class = 'form-inline'
    disable_csrf = True
    form_tag = True
    form_show_labels = True
    form_action = '#'
    #help_text_as_placeholder = True

    def __init__(self, *args, **kwargs):
        super(TweetHelper, self).__init__(*args, **kwargs)
        for index, name in enumerate(self.form.fields):
            self[index].wrap(Field, placeholder=name.capitalize())


class FormHelperMixin(object):

    def __init__(self, *args, **kwargs):
        scope_prefix = get_model_name(self._meta.model.__name__)
        kwargs.update({'scope_prefix': scope_prefix})
        super(FormHelperMixin, self).__init__(*args, **kwargs)
        self.helper = TweetHelper(form=self)
        self.helper.form_id = get_form_id(self)


class TweetForm(FormHelperMixin, NgModelFormMixin, forms.ModelForm):

    class Meta:
        model = Tweet
        widgets = {
            'status': StatusInput
        }


class PostTweetSetForm(FormHelperMixin, NgModelFormMixin, forms.ModelForm):

    class Meta:
        model = PostTweetSet
        widgets = {
            'start_time': DateTimeLocalInput,
        }


class PeriodicTweetForm(FormHelperMixin, NgModelFormMixin, forms.ModelForm):

    class Meta:
        model = PeriodicTweet
        widgets = {
            'priority': forms.NumberInput,
        }
        fields = ('already_posted', 'priority', 'tweet', )


class TimedTweetForm(FormHelperMixin, NgModelFormMixin, forms.ModelForm):

    class Meta:
        model = TimedTweet
        widgets = {
            'post_time': DateTimeLocalInput,
        }
        fields = ('post_time', 'already_posted',)
