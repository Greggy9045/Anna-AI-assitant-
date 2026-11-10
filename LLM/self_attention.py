import numpy as np 
import math

class SelfAttention:
    def __init__(self, Esize):
        self.embedding_size = Esize

        self.Wq = np.random.randn(Esize, Esize)
        self.Wk = np.random.randn(Esize, Esize)
        self.Wv = np.random.randn(Esize, Esize)

    def generate_query(self, embedding):
        return embedding @ self.Wq
    
    def generate_key(self, embedding):
        return embedding @ self.Wk
    
    def generate_value(self, embedding):
        return embedding @ self.Wv

    def calculate_attention_scaling(self, Q, K):
        return (Q @ K.T) / math.sqrt(self.embedding_size)    # Outputs a numpy array 

    def softmax(self, scores):
        return (np.exp(scores - np.max(scores, axis=1, keepdims=True))) / (np.sum((np.exp(scores - np.max(scores, axis=1, keepdims=True))), axis=1, keepdims=True))

    def calculate_attention_output(self, Q, K, v):
        return self.softmax(self.apply_casual_mask(self.calculate_attention_scaling(Q, K))) @ v

    def casual_mask(self, sequence_length):
        return np.tril(np.ones((sequence_length, sequence_length)), k=0)

    def apply_casual_mask(self, scores):
        return np.where(self.casual_mask(sequence_length=scores.shape[0]) == 0, -np.inf, scores)

    def debugTestFunction(self):
        embeddings = np.random.randn(4, 4)

        Q = self.generate_query(embeddings)
        K = self.generate_key(embeddings)
        V = self.generate_value(embeddings)

        output = self.softmax(self.apply_casual_mask(self.calculate_attention_output(Q, K, V)))

        return output
    
selfattention = SelfAttention(4)

print(selfattention.debugTestFunction())

