from Data import *
class DecisionNode:
    """
        This Node Stores the attribute on which decision needs to be taken
        and further Sub-DecisionNodes
        data : dataframe of data on which this node was trained
        attr : decison attribute
        child : sub-decision Nodes 
    """
    def __init__(self,data,attr,child):
        self.data= data
        self.attr = attr
        self.childs = child

class Leaf:
    """
        Stores the prediction to return when its instance is encountered
    """
    def __init__(self,prediction):
        self.prediction  = prediction

class DecisionTree:

    """
        Decision Tree is the classifier class implementing ID3 Algorithm
        for decison making 
                                  
    """

    def __init__(self,data,lcol):
        """
            data :  pandas dataframe on which it will be trained
            lcol :  column in which labels are stored 
        """
        self.data=data
        self._root=None
        self.lcol = lcol
        pass
    
    def fit(self):
        """
            this is recursive fuction which trains 
                Decision tree and builds it simultaneously
        """
        self._root=self._fit(self.data,list(self.data.columns),self.lcol)

    def _fit(self,data,col_list,lcol):
        
        attr,gain = find_best_node(data)
        
        if(gain == 0 or len(unique_vals(data,lcol))==1 or len(col_list)==1):
            return Leaf(unique_vals(data,lcol)[0])
        
        branches = {}
        col_list.remove(attr)

        for classname in unique_vals(data,attr):
            next_data = split(data,attr,classname)
            branches[classname] = self._fit(next_data[col_list],col_list,lcol);
            
        return DecisionNode(data,attr,branches)
    
    def _tree_structure(self,root,lvl):
        if root == None:
            return
        if isinstance(root,DecisionNode):
            print('\t'*2*lvl,'attribute : ',root.attr)
        elif isinstance(root,Leaf):
            print('\t'*2*lvl,'prediction : ',root.prediction)
            return

        for classname in unique_vals(root.data,root.attr):
            try:
                print('\t'*2*lvl,'edge : ',classname)
                self._tree_structure(root.childs[classname],lvl+1)
            except : 
                pass

    def visualtize(self):
        """
            call this to visualize the tree structure
        """
        if self._root==None:
            print('Call fit() to create a tree first')
            return
        self._tree_structure(self._root,0)

    def predict_point(self,root,test_data_point):
        """
            predicts the label for single data_point
            and returns the result

            root : root of the decision tree
            test_data_point : data point for which result is to be predicted

        """
        prediction=''
        if(isinstance(root,Leaf)):
            prediction = root.prediction
        elif(isinstance(root,DecisionNode)):
            prediction=self.predict_point(root.childs[test_data_point[root.attr]],test_data_point)
        return prediction

    def predict(self,test_data,lcol):
        """
            test_data : data whose output needs to be predicted
            lcol      : column in which the lables are stored
            returns accurracy of predictions in precentage(%)
        """
        if(list(self.data.columns)!=list(test_data.columns)):
            #data passed to the for prediction is not made for this decison tree
            print('Error : Data Columns does not match')
            print('required :',list(self.data.columns))
            print('found :',list(test_data.columns))
            return None
        cols = list(test_data.columns)
        cols.remove(lcol)
        test_records = test_data[cols].to_dict(orient = 'records')
        test_labels = test_data[[lcol]].to_dict(orient = 'records')
        currect_cnt = 0
        tot_records = len(test_records)
        rec_no = 0 
        for record in test_records:
            try : 
                prediction = self.predict_point(self._root,record)
                if prediction == test_labels[rec_no][lcol]:
                    currect_cnt+=1
            except  KeyError:
                pass
            rec_no+=1
        
        return (currect_cnt/tot_records)*100

    def getRoot(self):
        return self._root; 


if __name__ == '__main__':
    data = getdata()
    test_data=data
    # data,test_data = getBankData(0.75)
    tree = DecisionTree(data,list(data.columns)[-1])
    tree.fit()
    tree.visualtize()
    test_point = {
        'outlook':'rainy',
        'temp' : 'hot',
        'humidity' : 'high',
        'windy' : False,
    }
    print('prediction for',test_point,'is',tree.predict_point(tree.getRoot(),test_point))
    print('Accurracy : ',tree.predict(test_data,list(test_data.columns)[-1]))