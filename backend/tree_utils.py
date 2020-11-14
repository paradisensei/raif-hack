import numpy as np
import pandas as pd
import sys, os, random, re, datetime
from imp import reload

from sklearn.tree import _tree
from sklearn.ensemble import RandomForestClassifier



def print_tree_paths(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)

def get_classification_tree_paths(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    #print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth, path_l, path_r, paths):
        indent = "\t"
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            
            path_l += ' ' + "{}if {} <= {}".format(indent, name, threshold)
            path_l += ' ' + str(recurse(tree_.children_left[node], depth + 1, path_l, path_l, paths))
            #print(path_l)
            paths.append(path_l)
            
            path_r += ' ' + "{}if {} > {}".format(indent, name, threshold)
            path_r += ' ' + str(recurse(tree_.children_right[node], depth + 1, path_r, path_r, paths))
            #print(path_r)
            paths.append(path_r)
        else:
            r1 = "{}return {}".format(indent, tree_.value[node])
            r2 = tree_.value[node]
            leaf_support = r2[0][0]+r2[0][1]
            class_1_proba = 1.0 * r2[0][1] / leaf_support 
            return r1+indent+str(r2[0][0])+indent+str(r2[0][1])+indent+str(leaf_support)+indent+str(class_1_proba)

    paths = []
    _ = recurse(0, 1, '', '', paths)
    
    paths = [p.strip().split('\t') for p in paths if len(p.strip().split('\t')) > 1]
    paths = [[' '.join(p[:-4])]+[' '.join(p[:-5])+' return '+str(p[-1])]+p[-4:] for p in paths]
    
    return paths

def get_most_probable_classification_tree_paths(tree, feature_names, n=5):
    paths = get_classification_tree_paths(tree, feature_names)
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.sort_values(['class_1_proba','leaf_support'], ascending=[False,False])
    return paths.head(n)[['segment','leaf_support','class_1_proba']]

def get_most_probable_classification_ensemble_paths(model, feature_names, n=5):
    paths = []
    for tree_i in model.estimators_:
        paths += get_classification_tree_paths(tree_i, feature_names)
        
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.drop_duplicates().sort_values(['class_1_proba','leaf_support'], ascending=[False,False]).reset_index(drop=True)
    
    return paths.head(n)[['segment','leaf_support','class_1_proba']]
    
def get_regression_tree_paths(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    #print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth, path_l, path_r, paths):
        indent = "\t"
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            
            path_l += ' ' + "{}if {} <= {}".format(indent, name, threshold)
            path_l += ' ' + str(recurse(tree_.children_left[node], depth + 1, path_l, path_l, paths))
            #print(path_l)
            paths.append(path_l)
            
            path_r += ' ' + "{}if {} > {}".format(indent, name, threshold)
            path_r += ' ' + str(recurse(tree_.children_right[node], depth + 1, path_r, path_r, paths))
            #print(path_r)
            paths.append(path_r)
        else:
            r1 = "{}return {}".format(indent, tree_.value[node])
            r2 = tree_.value[node]
            leaf_support = r2[0][0]+r2[0][1]
            class_1_proba = 1.0 * r2[0][1] / leaf_support 
            return r1+indent+str(r2[0][0])+indent+str(r2[0][1])+indent+str(leaf_support)+indent+str(class_1_proba)

    paths = []
    _ = recurse(0, 1, '', '', paths)
    
    paths = [p.strip().split('\t') for p in paths if len(p.strip().split('\t')) > 1]
    paths = [[' '.join(p[:-4])]+[' '.join(p[:-5])+' return '+str(p[-1])]+p[-4:] for p in paths]
    
    return paths

def get_most_probable_regression_tree_paths(tree, feature_names, n=5):
    paths = get_classification_tree_paths(tree, feature_names)
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.sort_values(['class_1_proba','leaf_support'], ascending=[False,False])
    return paths.head(n)[['segment','leaf_support','class_1_proba']]

def get_most_probable_regression_ensemble_paths(model, feature_names, n=5):
    paths = []
    for tree_i in model.estimators_:
        paths += get_classification_tree_paths(tree_i, feature_names)
        
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.drop_duplicates().sort_values(['class_1_proba','leaf_support'], ascending=[False,False]).reset_index(drop=True)
    
    return paths.head(n)[['segment','leaf_support','class_1_proba']]
    