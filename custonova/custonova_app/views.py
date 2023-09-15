from django.shortcuts import render
from django.views.generic import TemplateView, View
from .scripts.clusters import Clusters
from .scripts.logistic_regression import CustomerChurn
from .forms import LogisticForm, ClusteringForm
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from io import BytesIO
import urllib, base64
from pandas import read_csv
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from .models import ClusterImage, RegressionImage
from datetime import datetime

clustering = Clusters()
churn = CustomerChurn()


def get_elbow_diagram(data):
    inertia = []
    cluster_ranges = range(1, 20)
    for k in cluster_ranges:
        model = KMeans(n_clusters=k).fit(data.drop(['Gender'], axis=1))
        inertia.append(model.inertia_)

    plt.figure(figsize=(16,9))
    plt.plot(cluster_ranges, inertia, 'bx-')
    plt.title('Elbow Diagram', fontsize=24)
    plt.xlabel('Clusters')
    plt.ylabel('Inertia')

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    string = base64.b64encode(img_data.read())

    return urllib.parse.quote(string)

def get_data_visualisation(data):
    fig, ax = plt.subplots(2, 3, figsize=(16,9))
    fig.suptitle('Data Visualization', fontsize=24)
    plt.subplots_adjust(hspace = .3)
    ax[0,0].set_title('Spending Score')
    ax[0,0].set_ylabel('Count')
    ax[0,0].set_xlabel('Annual Income')
    ax[0,0].hist(data['Spending Score (1-100)'])

    ax[0,1].set_title('Gender')
    ax[0,1].set_ylabel('Count')
    ax[0,1].set_xlabel('Gender')
    ax[0,1].hist(data['Gender'])

    ax[0,2].set_title('Annual Income')
    ax[0,2].set_ylabel('Count')
    ax[0,2].set_xlabel('Annual Income')
    ax[0,2].plot(data['Annual Income (k$)'], 'tab:orange')

    ax[1,0].set_title('Age Against Gender')
    ax[1,0].set_xlabel('Gender')
    ax[1,0].set_ylabel('Age')
    ax[1,0].bar(data['Gender'],data['Age'])

    ax[1,1].set_title('Annual Income Against Gender')
    ax[1,1].set_ylabel('Annual Income')
    ax[1,1].set_xlabel('Gender')
    ax[1,1].bar(data['Gender'],data['Annual Income (k$)'])

    ax[1,2].set_title('Spending Score Against Gender')
    ax[1,2].set_ylabel('Spending Score')
    ax[1,2].set_xlabel('Gender')
    ax[1,2].bar(data['Gender'],data['Spending Score (1-100)'])

    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    string = base64.b64encode(img_data.read())
    
    return urllib.parse.quote(string)

def get_clusters_diagram(x_axis, y_axis, data, clusters):
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(data.drop(['Gender'], axis=1))
    data['Cluster'] = kmeans.predict(data.drop(['Gender'], axis=1))
    test_la = data['Cluster']
    cluster_mapping = {0: 'Potential Loyalist', 1: 'Loyalist', 2: 'Reasonable', 3: 'Satisfied', 4: 'Need Attention'}
    cluster_labels = []
    for i in test_la:
        cluster_labels.append(cluster_mapping.get(i))
    data['Cluster Labels'] = cluster_labels

    fig1, ax = plt.subplots(figsize=(16,9))
    fig1.suptitle('Cluster Visualization', fontsize=24)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    scatter = ax.scatter(x=data[x_axis], y=data[y_axis], c=data['Cluster'], cmap='rainbow')
    legend1 = ax.legend(*scatter.legend_elements(), loc='best', title='Clusters')
    ax.add_artist(legend1)
    
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    string = base64.b64encode(img_data.read())
    
    return urllib.parse.quote(string), data

class Home(TemplateView):
    template_name = 'app/home.html'

class CustomerClusteringView(View):
    template_name = 'app/clustering.html'
    form_class = ClusteringForm

    def post(self, request, *args, **kwargs):
        # get elbow diagram
        # get clustering images
        form = ClusteringForm(request.POST, request.FILES)
        if form.is_valid():
            data = read_csv(request.FILES.get('dataset'))
            elbow_diagram = get_elbow_diagram(data)
            data_visualization = get_data_visualisation(data)
            clusters_diagram = get_clusters_diagram(y_axis=form.cleaned_data['y_axis'], x_axis=form.cleaned_data['x_axis'], data=data, clusters=form.cleaned_data['clusters'])
            return render(
                request, 
                self.template_name, 
                {
                    'form': self.form_class(request.POST, request.FILES), 
                    'elbow': elbow_diagram,
                    'data_visualisation': data_visualization,
                    'clustering_diagram': clusters_diagram  
                }
            )
        return render(
            request, 
            self.template_name, 
            {
                'form': self.form_class(request.POST, request.FILES)
            }
        )

    def get(self, request, *args, **kwargs):
        # logic here
        return render(
            request, 
            self.template_name, 
            {
                'form': self.form_class()
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomerChurnView(View):
    template_name = 'app/clustering.html'
    form_class = LogisticForm

    def post(self, request, *args, **kwargs):
        # logic here
        return render(request, self.template_name, {'form': self.form_class(), })

    def get(self, request, *args, **kwargs):
        # logic here
        return render(request, self.template_name, {'form': self.form_class(), })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CustomerClusteringApiView(APIView):

    def post(self, request, *args, **kwargs):
        form = ClusteringForm(request.POST, request.FILES)
        if form.is_valid():
            data = read_csv(request.FILES.get('dataset'))
            elbow_diagram = get_elbow_diagram(data)
            data_visualization = get_data_visualisation(data)
            clusters_diagram, data = get_clusters_diagram(y_axis=form.cleaned_data['y_axis'], x_axis=form.cleaned_data['x_axis'], data=data, clusters=form.cleaned_data['clusters'])
            ClusterImage.objects.create(
                title=f'Clustering Elbow Diagram ({datetime.now()})',
                image=elbow_diagram
            )
            ClusterImage.objects.create(
                title=f'Data Visualisation ({datetime.now()})',
                image=data_visualization
            )
            ClusterImage.objects.create(
                title=f'Clustering Diagram ({datetime.now()})',
                image=clusters_diagram
            )
            return Response( 
                data={
                    'elbow': elbow_diagram,
                    'data_visualisation': data_visualization,
                    'clustering_diagram': clusters_diagram, 
                    # 'data': data
                },
                status=200
            )
        return Response(
            data={
                'error': 'Form is invalid'
            },
            status=400
        )


def generate_regression_image(data, title):
    
    # plt.figure(figsize=(16,9))
    # plt.pie(prob_pie['data'], labels=list(prob_pie['labels']), startangle=270)
    # plt.title('Probability Pie Chart', fontsize=24)

    # img_data_1 = BytesIO()
    # plt.savefig(img_data_1, format='png')
    # img_data_1.seek(0)
    # pie_prob = base64.b64encode(img_data_1.read())
    
    plt.figure(figsize=(16,9))
    plt.pie(data, labels=['0', '1'], startangle=270)
    plt.title(title, fontsize=24)

    img_data_2 = BytesIO()
    plt.savefig(img_data_2, format='png')
    img_data_2.seek(0)
    pie_pred = base64.b64encode(img_data_2.read())

    return pie_pred


class CustomerChurnViewApiView(APIView):

    def post(self, request, *args, **kwargs):
        # logic here
        dataset = read_csv(request.FILES.get('dataset'))
        response = churn.predict(dataset)
        # dataset['Churn'] = response
        # probability = response['probs_pie']
        # predictions = response['pred_pie']
        
        # prediction = generate_regression_image(pd.Series(list(response)).value_counts(sort=True), 'Prediction Pie Chart')
        
        # RegressionImage.objects.create(
        #     title= f'Logistic Reg. Probability Prediction ({datetime.now()})',
        #     image= prob_image
        # )
        # RegressionImage.objects.create(
        #     title=f'Logistic Reg. Prediction ({datetime.now()})',
        #     image=prediction
        # )
        return Response(
            data={
                'data': response
            }, 
            status=200
        )

    def get(self, request, *args, **kwargs):
        # logic here
        
        return Response(
            data={
                'form': ''
            },
            status=200
        )

class TrainChurnApiView(APIView):

    def post(self, request, *args, **kwargs):
        return Response(
            data=churn.train(read_csv(request.FILES.get('dataset'))),
            status=200
        )

class TestChurnApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        return Response(
            data=churn.performance(read_csv(request.FILES.get('dataset'))),
            status=200
        )

# serializers
class ClusterImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterImage
        fields = ['id', 'title', 'image', 'date', 'createdBy']


class LogisticImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegressionImage
        fields = ['id', 'title', 'image', 'date', 'createdBy']


class ClusteringImagesViewSets(viewsets.ModelViewSet):
    queryset = ClusterImage.objects.all()
    serializer_class = ClusterImageSerializer
    

class LogisticImagesViewSets(viewsets.ModelViewSet):
    queryset = RegressionImage.objects.all()
    serializer_class = LogisticImageSerializer
    