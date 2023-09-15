from django.forms import Form, ChoiceField, FileInput, IntegerField, Select, FileField, FileInput

columns = (
    ('Spending Score (1-100)', 'Spending Score (1-100)'),
    ('Annual Income (k$)', 'Annual Income (k$)'),
    ('Age', 'Age'),
    ('Gender', 'Gender')
)


class ClusteringForm(Form):
    clusters = IntegerField(min_value=2, max_value=100000, label='Anticipated Clusters')
    dataset = FileField(label='Select Dataset', widget=FileInput(attrs={'class': 'form-control', 'type': 'file' }))
    x_axis = ChoiceField(choices=columns, widget=Select)
    y_axis = ChoiceField(choices=columns, widget=Select)


class LogisticForm(Form):
    pass
