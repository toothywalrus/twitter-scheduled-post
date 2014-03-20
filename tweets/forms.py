from django import forms as django_forms

import floppyforms as forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field

from djangular.forms.angular_model import NgModelFormMixin
from djangular.forms import NgFormValidationMixin

from .models import Tweet, PostTweetSet, PeriodicTweet, TimedTweet,\
    Interval
from .utils import get_model_name, get_form_id, get_resource_name


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateTimePicker(forms.DateTimeInput):
    template_name = 'datetimepicker.html'

    def get_context_data(self):
        del self.attrs['placeholder']
        return super(DateTimePicker, self).get_context_data()


class StatusInput(forms.Textarea):
    rows = 4

    def get_context_data(self):
        self.attrs['style'] = "resize:none"
        return super(StatusInput, self).get_context_data()


class NgSelectInput(forms.Select):
    template_name = 'ngselectinput.html'

    def __init__(self, *args, **kwargs):
        self.items = "".join(["info.", kwargs.pop('items', 'tweets')])
        self.value = kwargs.pop('value', 'id')
        self.text = kwargs.pop('text', 'status')
        self.model_name = kwargs.pop('model_name', 'tweet')
        super(NgSelectInput, self).__init__(*args, **kwargs)

    def get_context_data(self):

        self.attrs['ng-options'] = 'obj.%s as obj.%s for obj in %s' % (
            self.value, self.text, self.items,)
        ctx = super(NgSelectInput, self).get_context_data()
        ctx.update({'model_name': self.model_name})
        return ctx


class TweetHelper(FormHelper):
    form_show_errors = False
    # form_class = 'form-inline'
    disable_csrf = True
    form_tag = True
    form_show_labels = True
    form_action = '#'
    # help_text_as_placeholder = True

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


class TweetForm(FormHelperMixin, NgModelFormMixin, NgFormValidationMixin,
                forms.ModelForm):

    class Meta:
        model = Tweet
        widgets = {
            'status':
            StatusInput
        }


class PostTweetSetForm(
    FormHelperMixin, NgModelFormMixin, NgFormValidationMixin,
        forms.ModelForm):

    description = django_forms.CharField(max_length=200, min_length=1)

    class Meta:
        model = PostTweetSet
        widgets = {
            'interval':
            NgSelectInput(items='intervals',
                          text='period',
                          model_name='interval'),
            'start_time':
            DateTimeLocalInput,
        }
        fields = ('interval', 'description', 'start_time', 'users',)


class PeriodicTweetForm(FormHelperMixin, NgModelFormMixin,
                        NgFormValidationMixin, forms.ModelForm):

    class Meta:
        model = PeriodicTweet
        widgets = {
            'priority': forms.NumberInput,
            'tweet': NgSelectInput,
        }
        fields = ('priority', 'tweet', )


class TimedTweetForm(FormHelperMixin, NgModelFormMixin,
                     NgFormValidationMixin, forms.ModelForm):

    class Meta:
        model = TimedTweet
        widgets = {
            # 'post_time': DateTimePicker,
            'post_time': DateTimeLocalInput
        }
        fields = ('post_time', 'user',)


class IntervalForm(FormHelperMixin, NgModelFormMixin, forms.ModelForm):

    class Meta:
        model = Interval
