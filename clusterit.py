from utilcluster import *

#plt.figure
label1 = ["#FFFF00", "#008000", "#0000FF", "#800080", "#00FF00", "#333333"]
color = [label1[i] for i in labels]

plt.scatter(datapoint[:,0], datapoint[:,1], c=color)
fxy = zip(filenames, datapoint[:,0], datapoint[:,1])

for file, x, y in fxy:
    plt.text(x,y,file)

centroids = kmeans_model.cluster_centers_
centroidpoint = pca.transform(centroids)
#plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
#plt.savefig('cluster1.png')
#plt.show()

# save it all for future ref:
import pickle
modelos = {'kmeans': (kmeans_model, labels, clusters),
            'pca': (pca, datapoint), 'd2v': d2v_model, 'all': all_content}
#pickle.dump(modelos, open('modelo2.pk','wb'))
#pickle.dump(all_content, open('all_content.pk','wb'))
