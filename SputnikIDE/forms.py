from django import forms

attrs = {'class': 'form-control', 'autocomplete': 'off'}


class Project_Form(forms.Form):
    valid_css_class = 'is-valid'
    invalid_css_class = 'is-invalid'
    name = forms.CharField(label='Название', max_length=50, widget=forms.TextInput(attrs=attrs))

    def is_valid(self):
        res = forms.Form.is_valid(self)

        for name, field in self.fields.items():
            class_attr = field.widget.attrs.get('class', '')
            if name in self.errors:
                field.widget.attrs.update({
                    'class': class_attr + ' ' + self.invalid_css_class
                })
            else:
                field.widget.attrs.update({
                    'class': class_attr + ' ' + self.valid_css_class
                })
        return res


class Version_Loading(forms.Form):
    code = forms.CharField()
    new_version = forms.BooleanField(required=False)
    build = forms.BooleanField(required=False)
    run = forms.BooleanField(required=False)


class Project_Delete(forms.Form):
    to_delete = forms.IntegerField(initial=1, widget=forms.HiddenInput())
