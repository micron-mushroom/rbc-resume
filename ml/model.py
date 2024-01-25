# BTW this is just me following along with the tutorial at
# https://www.tensorflow.org/text/tutorials/text_generation#build_the_model

# I was mainly playing in the python repl but defining giant classes in the repl
# would be quite time consuming and inefficient. It would also distract me from 
# the process I was was trying to do myself (training and inspecting the model)

# This is a pain, but the lack of autocomplete is more annoying.
import keras.api._v2.keras as keras
import tensorflow as tf

# I find this pretty straightforward.
class Model(keras.Model):
    def __init__(self, vocab_size, embedding_dim, rnn_units):
        super().__init__(self)
        self.embedding = keras.layers.Embedding(vocab_size, embedding_dim)
        self.gru = keras.layers.GRU(rnn_units, return_sequences=True, return_state=True)
        # `vocab_size` since we are calculating the most probable next 
        # character in the sequence.
        self.dense = keras.layers.Dense(vocab_size)

    def call(self, inputs, states=None, return_states=False, training=False,):
        x = self.embedding(inputs, training=training)
        if states is None:
            states = self.gru.get_initial_state(x)
        x, states = self.gru(x, initial_state=states, training=training)
        x = self.dense(x, training=training)

        return x, states if return_states else x


class OneStep(keras.Model):
    def __init__(self, model, chars_from_ids, ids_from_chars, temperature=1.0):
        super().__init__(self)

        self.temperature = temperature
        self.model = model
        self.chars_from_ids = chars_from_ids
        self.ids_from_chars = ids_from_chars

        # Filter UNK out of the output sequence
        skip_ids = self.ids_from_chars(["[UNK]"])[:, None]
        sparse_mask = tf.SparseTensor(values=[-float("inf")] * len(skip_ids), indices=skip_ids, dense_shape=[len(ids_from_chars.get_vocabulary())])
        self.prediction_mask = tf.sparse.to_dense(sparse_mask)

    @tf.function
    def generate_a_char(self, inputs, states=None):
        code_points = tf.strings.split(inputs, "UTF-8")
        input_ids = self.ids_from_chars(code_points).to_tensor()

        logits, states = self.model(input_ids, states=states, return_states=True)
        print(logits)
        logits = (logits[:, -1, :] / self.temperature)
        print(logits)
        logits = logits + self.prediction_mask

        output_ids = tf.random.categorical(logits, num_samples=1)
        output_ids = tf.squeeze(output_ids, axis=-1)

        output_chars = self.chars_from_ids(output_ids)
        return output_chars, states



