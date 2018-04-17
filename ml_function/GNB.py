import numpy as np

class GNB():
    def __init__(self):
        pass
    
    def fit(self,tr_d,tr_l):
        """ Fit function
        
        Parameter(input) 
        -------------------------
        tr_d : np array, train data
        tr_l  : np.array, train label 
        
        Returns(out put)
        -------------------------
        self : objrct
        """
        self.tr_d=tr_d
        self.tr_l=tr_l
        self.ns=tr_d.shape[0]
        self.nd=tr_d.shape[1]
        self.nc=len(set(tr_l))   
        self.PC=[tr_d[tr_l==c] for c in sorted(set(tr_l))]
        # calculate propr prob at each class
        self.PY=np.log([len(self.tr_d[self.tr_l==c])/self.ns for c in sorted(set(tr_l))]).reshape(self.nc,1)
        self.means=np.empty((self.nc, 1, self.nd),dtype=float)
        self.sigmas=np.empty((self.nc, 1, self.nd),dtype=float)
        
        # calcluate mean and var at each class and each feature of each class
        for c in range(self.nc):
            self.means[c]=np.mean(self.PC[c],axis=0)
            self.sigmas[c]=np.var(self.PC[c],axis=0)
            
        return self
            
    def predict(self,te_d):
        """ predict function
        
        Parameter(input) 
        -------------------------
        te_d : np array, test data
        te_l  : np.array, test label 
        
        Returns(output)
        -------------------------
        result : 1D np array, predict label
        """
        self.te_d=te_d
        self.result=np.argmax(self.calc_norm(self.te_d), axis=0)
        return self.result

    def calc_norm(self,x):
        """calculated based on norm distribution
        
        Parameter(input) 
        -------------------------
        x : np array, test_data
        
        Returns(output)
        -------------------------
        prob : probability of each class
        """
        p0=1 / (np.sqrt(2*np.pi*self.sigmas) + 1e-7)
        p1=(x-self.means)**2
        p2=2*self.sigmas
        return self.PY+np.sum(np.log((p0 * np.exp(-1 * p1 / (p2 + 1e-7)))+1e-7),axis=2)
    
    def scorering(self,test_label):
        """calculated accuracy
        
        Parameter(input) 
        -------------------------
        test_label : np array, test label
        
        Returns(output)
        -------------------------
        score : accuracy score
        """
        new_label=test_label
        while 0 not in new_label:
            new_label=new_label-1
        return sum(1 for i, j in zip(self.result,new_label) if i==j)/len(new_label)
    
if __name__ == "__main__":
    pass