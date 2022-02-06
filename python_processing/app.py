from fastapi import FastAPI
from tensorflow.keras.layers import (LSTM, Activation, Bidirectional, Dense,
                                     Dropout, Flatten, Input, Lambda, Multiply,
                                     Permute, RepeatVector, Embedding)
from tensorflow.keras.models import Model
import tensorflow.keras.backend as K
import numpy as np

app = FastAPI()



embedding_fn = 'data/vectors.txt'                   # GloVe embeddings
model_weights = "simple_lstm_glove_vectors_val.h5"  # Trained model weights
MAX_TOKENS = 100
HIDDEN_LAYER_NODES = 128

def pretrained_embedding_layer(word_to_vec_map, word_to_index):
    vocab_len = len(word_to_index) + 2  # adding 1 to fit embedding
    emb_dim = word_to_vec_map["cucumber"].shape[0] # dim of GloVe vectors 
    emb_matrix = np.zeros((vocab_len, emb_dim))
    for word, index in word_to_index.items():
        emb_matrix[index, :] = word_to_vec_map[word]
    embedding_layer = Embedding(vocab_len, emb_dim, trainable=False)
    embedding_layer.build((None,))
    embedding_layer.set_weights([emb_matrix])

    return embedding_layer

def read_glove_vecs(glove_file):
    with open(glove_file, encoding="utf8") as f:
        words = set()
        word_to_vec_map = {}
        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = np.array(line[1:], dtype=np.float64)
        
        i = 1
        words_to_index = {}
        index_to_words = {}
        for w in sorted(words):
            words_to_index[w] = i
            index_to_words[i] = w
            i = i + 1
    return words_to_index, index_to_words, word_to_vec_map

word_to_index, index_to_word, word_to_vec_map = read_glove_vecs(embedding_fn)

sentence_indices = Input(shape=(MAX_TOKENS,), dtype='int32')
embedding_layer = pretrained_embedding_layer(word_to_vec_map, word_to_index)
embeddings = embedding_layer(sentence_indices)

X = Bidirectional(LSTM(HIDDEN_LAYER_NODES, return_sequences=True), input_shape=(MAX_TOKENS,))(embeddings)
X = Dropout(0.5)(X)

attention = Dense(1, activation='tanh')(X)
attention = Flatten()(attention)
attention = Activation('softmax')(attention)
attention = RepeatVector(HIDDEN_LAYER_NODES * 2)(attention)
attention = Permute([2, 1])(attention)

sent_representation = Multiply()([X, attention])
sent_representation = Lambda(lambda xin: K.sum(xin, axis=1))(sent_representation)

X = Dropout(0.5)(sent_representation)
X = Dense(2, activation='softmax')(X)
X = Activation('softmax')(X)

model = Model(inputs=sentence_indices, outputs=X)
model.load_weights(model_weights)

@app.on_event("startup")
def start_up():
  print("Starting server.")

@app.get("/")
async def root():
  return "Hello world!"

@app.get("/process_media/{uri}")
def process_video(uri: str):
  """
  processes a given video, returns schema TBD

  uri -- gcs uri of media resource to process
  """

@app.get("/test")
def test_schema():
  return {"field": "value"}