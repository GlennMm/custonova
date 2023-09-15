from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class Clusters:
    def __init__(self):
        self.kmeans = KMeans(n_clusters=5)
        self.data = None
        self.cluster_mapping = {0: 'Potential Loyalist', 1: 'Loyalist', 2: 'Reasonable', 3: 'Satisfied', 4: 'Need Attention'}

    def train(self, dataset = None):
        data = dataset.drop(['Gender'], axis=1)
        # fitting
        self.kmeans.fit(data)
        
        # predicting clusters
        clustered = dataset.copy()
        clustered['Cluster'] = self.kmeans.predict(dataset.drop(['Gender'], axis=1))
        data_clustres = clustered['Cluster']
        
        cluster_labels = []
        for i in data_clustres:
            cluster_labels.append(self.cluster_mapping.get(i))
        
        clustered['Cluster Labels'] = cluster_labels
        print(clustered)
        return self.generate_visualisation(clustered)

    def predict(self, dataset = None):
        if dataset is None:
            return
        clustered = dataset.copy()
        clustered['Cluster'] = self.kmeans.predict(dataset.drop(['Gender'], axis=1))
        return clustered

    def get_elbow(self, dataset = None):
        inertias = []
        img = BytesIO()
        cluster_range = range(1,15)
        
        for k in cluster_range:
            model = KMeans(n_clusters=k)
            model.fit(dataset.drop(['Gender'], axis=1))
            inertias.append(model.inertia_)

        plt.figure(figsize=(16,8))
        plt.plot(cluster_range, inertias, 'bx-')
        plt.title('Elbow Method', fontsize=24, color='white')
        plt.savefig(img, format='png')
        
        img.seek(0)
        image = img.getvalue()
        img.close()
        
        return image

    def generate_visualisation(self, data):
        data_visualization = BytesIO()
        cluster_visualization = BytesIO()

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

        plt.savefig(data_visualization, format='png')

        fig1, ax1 = plt.subplots(figsize=(16,9))
        fig1.suptitle('Cluster Visualization', fontsize=24)
        scatter = ax1.scatter(x=data['Annual Income (k$)'], y=data['Spending Score (1-100)'], c=data['Cluster'], cmap='rainbow')
        # scatter.xlabel('X LABEL')
        legend1 = ax1.legend(*scatter.legend_elements(), loc='best', title='Clusters')
        ax1.add_artist(legend1)
        plt.savefig(cluster_visualization, format='png')

        data_visualization.seek(0)
        visual = data_visualization.getvalue()
        data_visualization.close()

        cluster_visualization.seek(0)
        cluster = cluster_visualization.getvalue()
        cluster_visualization.close()

        return visual, cluster

    def get_clustered_graph(self, x='Annual Income (k$)', y='Spending Score (1-100)', dataset = None):
        img = BytesIO()
        
        dataset['Cluster'] = self.kmeans.predict(dataset.drop(['Gender'], axis=1))
        plot = sns.scatterplot(x=dataset[x], y=dataset[y], c=dataset['Cluster'], cmap='rainbow')
        plot.figure.savefig(img, format='png')

        img.seek(0)
        image = img.getvalue()
        img.close()
        return image

    
