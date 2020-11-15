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
            
            path_l += ' ' + "{} {} <= {};".format(indent, name, threshold)
            path_l += ' ' + str(recurse(tree_.children_left[node], depth + 1, path_l, path_l, paths))
            #print(path_l)
            paths.append(path_l)
            
            path_r += ' ' + "{} {} > {};".format(indent, name, threshold)
            path_r += ' ' + str(recurse(tree_.children_right[node], depth + 1, path_r, path_r, paths))
            #print(path_r)
            paths.append(path_r)
        else:
            #r1 = "{}return {}".format(indent, tree_.value[node])
            r2 = tree_.value[node]
            leaf_support = r2[0][0]+r2[0][1]
            class_1_proba = 1.0 * r2[0][1] / leaf_support 
            # r1+indent+str(r2[0][0])+indent+str(r2[0][1])+indent+str(leaf_support)+indent+str(class_1_proba)
            return str(r2[0][0])+indent+str(r2[0][1])+indent+str(leaf_support)+indent+str(class_1_proba)

    paths = []
    _ = recurse(0, 1, '', '', paths)
    
    paths = [p.strip().split('\t') for p in paths if len(p.strip().split('\t')) > 1]
    paths = [[' '.join(p[:-4])]+[' '.join(p[:-5])+' return '+str(p[-1])]+p[-4:] for p in paths]
    
    return paths

def get_most_probable_classification_tree_paths(tree, feature_names, n=5):
    paths = get_classification_tree_paths(tree, feature_names)
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.sort_values(['class_1_proba','leaf_support'], ascending=[False,False])
    return paths.head(n)[['segment','class_1_proba']]

def get_most_probable_classification_ensemble_paths(model, feature_names, n=5):
    paths = []
    for tree_i in model.estimators_:
        paths += get_classification_tree_paths(tree_i, feature_names)
        
    paths = pd.DataFrame(paths, columns=['s0','segment','class_0_support','class_1_support','leaf_support','class_1_proba'])
    paths = paths.drop_duplicates().sort_values(['class_1_proba','leaf_support'], ascending=[False,False]).reset_index(drop=True)
    
    return paths.head(n)[['segment','class_1_proba']]
    
def get_regression_tree_paths(model, feature_names):
    global value_data
    value_data = pd.DataFrame(columns=['path', 'value', 'sample', 'revenue'])
     
    def recurse(tree, node, features):
        global value_data
                
        if tree.children_left[node] == -1 and tree.children_right[node] == -1:
            value_data = value_data.append({'path' : features, 
                                            'value' : tree.value[node][0][0], 
                                            'sample' : tree.n_node_samples[node],
                                            'revenue' : tree.value[node][0][0] * tree.n_node_samples[node]}, ignore_index=True)
            return
        
        feature_name = feature_names[tree.feature[node]]
        threshold = tree.threshold[node]
        
        
        
        if tree.children_left[node] != -1:
            left_features = features + feature_name + ' <= ' + str(threshold) + ';'
            recurse(tree, tree.children_left[node], left_features)
            
        if tree.children_right[node] != -1:
            right_features = features + feature_name + ' > ' + str(threshold) + ';'
            recurse(tree, tree.children_right[node], right_features)

    recurse(model.tree_, 0, '')
    
    return value_data

def get_most_probable_regression_tree_paths(model, feature_names, n=5):
    paths = get_regression_tree_paths(model, feature_names)[['path','revenue']]
    paths = paths.sort_values(by='revenue', ascending=False).rename({'path':'segment'}, axis=1).reset_index(drop=True)
    return paths.head(n)

def get_most_probable_regression_ensemble_paths(model, feature_names, n=5):
    paths = pd.DataFrame(columns=['path','revenue'])
    for model_i in model.estimators_:
        paths = pd.concat([paths, get_regression_tree_paths(model_i, feature_names)[['path','revenue']]], axis=0, sort=False, ignore_index=True)
        
    paths = paths.sort_values(by='revenue', ascending=False).rename({'path':'segment'}, axis=1).reset_index(drop=True)
    return paths.head(n)
    