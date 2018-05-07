import numpy as np
np.random.seed(2018)
class KMeans:
    def init_centers(self, X, k):
        """ Initialize the starting k centers, using the KMeans++ algorithm. 
            Args: 
                X (numpy 2D matrix) : data matrix, each row is an example
                k (float) : number of clusters
            Return: 
                (numpy 2D matrix) : matrix of centers, each row is a center
        """
        result=np.zeros((k,X.shape[1]))
        for j in range(k):
            if j==0:
                result[j]=X[np.random.randint(X.shape[0]),:]
            else:
                p=np.zeros(X.shape[0])
                for i in range(X.shape[0]):
                    diff=(result[0]-X[i])
                    now_min=diff.dot(diff)
                    for jhat in range(1,j):
                        diff=(result[jhat]-X[i])
                        now_min=min(now_min,diff.dot(diff))
                    p[i]=now_min
                p=p/np.sum(p)
                jstar=np.random.choice(X.shape[0],1,p=p)[0]
                result[j]=X[jstar,:]
  
        return result
    
    def assign_clusters(self, X, centers):
        """ Given the data and the centers, assign clusters to all the examples. 
            Args: 
                X (numpy 2D matrix) : data matrix, each row is an example
                centers (numpy 2D matrix) : matrix of centers, each row is a center
            Return: 
                (numpy 2D matrix) : 1 hot encoding of cluster assignments for each example
        """
        y=np.zeros((X.shape[0],centers.shape[0]))
        for i in range(X.shape[0]):
            candidate=np.zeros(centers.shape[0])
            for j in range(centers.shape[0]):
                diff=centers[j]-X[i]
                candidate[j]=diff.dot(diff)
            y[i][np.argmin(candidate)]=1
        
        return y
    
    def compute_means(self, X, y):
        """ Given the data and the cluster labels, compute the new cluster centers. 
            Args: 
                X (numpy 2D matrix) : data matrix, each row is an example
                y (numpy 2D matrix) : 1 hot encoding of cluster assignments for each example
            Return: 
                (numpy 2D matrix) : matrix of centers, each row is a center
        """
        self.k=y.shape[1]
        centers=np.zeros((self.k,X.shape[1]))
        for j in range(self.k):
            agg=np.zeros(X.shape[1])
            count=0
            for i in range(X.shape[0]):
                if np.argmax(y[i])==j:
                    agg+=X[i]
                    count+=1
            centers[j]=agg/count
        
        return centers
    
    def train(self, X, centers, niters=20):
        """ Args: 
                X (numpy 2D matrix) : data matrix, each row is an example
                centers (numpy 2D matrix) : initial matrix of centers, each row is a center
            Return: 
                (y, centers) : tuple of 1 hot encoding of cluster assignments for each example 
                               the resulting cluster centers
        """
        
        for iters in range(niters):
            y=self.assign_clusters(X,centers)
            centers=self.compute_means(X, y)
        
        return (y,centers)
