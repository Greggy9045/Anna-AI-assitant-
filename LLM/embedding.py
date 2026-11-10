import numpy as np
import math

class Embedding:
    def __init__(self, Vsize, Esize):                         # class specific variables
        self.vocab_size = Vsize                     # How many tokens are known 
        self.embedding_size = Esize                # How many IDS per token 

        self.errors = {}

        self.embeddings = np.random.randn(self.vocab_size, self.embedding_size)
        
    def save_embeddings(self):
        np.save("embeddings.npy", self.embeddings)

    def load_embeddings(self):
        try :
            self.embeddings = np.load("embeddings.npy")
        except FileNotFoundError as e:
            self.errors[e] = "file not found"

            print(self.errors)

    def get_embedding(self, token_id):
        return self.embeddings[token_id]

    def update_embedding(self, token_id, new_values):
        try:
            if len(new_values) != self.embedding_size:
                self.errors["Incorrect Size"] = f"Incorret Embedding size. Size given {new_values} vs expected {self.embedding_size}"
                raise ValueError("Incorret Embedding size")

            self.embeddings[token_id] = new_values
            return self.embeddings
        
        except ValueError as e :
            self.errors[e] = f"Incorret Embedding size. Size given {len(new_values)} vs expected size"

class PostionalEmbedding:
    def __init__(self, sequence_length, embedding_size):
        self.sequence_length = sequence_length  # Max number of tokens in a sentence
        self.embedding_size = embedding_size    # Number of dimensions per token embedding

    def generate_encoding(self):
        fill = self.sequence_length * self.embedding_size
        matrix = np.zeros(fill).reshape(self.sequence_length, self.embedding_size)

        for pos in range(self.sequence_length ):
            for i in range(self.embedding_size):
                exponent = (2 * i) / self.embedding_size

                if i % 2 == 0 : # sine function releated equation (pos , 2i)
                    equation = math.sin(pos / (10000 ** exponent))

                elif i % 2 != 0 : # cosine function releated equation (pos , 2i + 1)
                    equation = math.cos(pos / (10000 ** exponent))

                matrix[pos][i] = equation
        return matrix

    def apply_encoding(self, embedding):
        return embedding + self.generate_encoding()

embedding = Embedding(10, 4)
postionalembedding = PostionalEmbedding(10, 4)

embedding.load_embeddings()

print(f"""
Embeddings : 
{embedding.embeddings}

Encoding : 
    generate_encoding   : 
{postionalembedding.generate_encoding()}

    apply_encoding      : 
{postionalembedding.apply_encoding(embedding.embeddings)} 


Errors :
    {embedding.errors}

 """)

embedding.save_embeddings()

