import gym
import numpy as np
import random
import tensorflow as tf
from ..parameters import HP
from ..models.modelBase import modelBase
from ..models.DQNBaseModel import DQNBaseModel


# a neural network with two hidden layers (128 nodes for each)

class FNN(DQNBaseModel):

	def defineInput(self):
		return tf.placeholder(shape=[None, self.input_size],dtype=tf.float32, name="X")

	def defineNNArchitecture(self):
		with tf.name_scope("layer1"):
			W1 = tf.get_variable("W1", shape=[self.input_size, 128],initializer =tf.truncated_normal_initializer(0, 0.02))
			b1 = tf.get_variable("b1", shape=[1, 128], initializer=tf.constant_initializer(0.0))
			A1 = tf.add(tf.matmul(self.X, W1), b1, name= "A")
			Z1 = tf.nn.relu(A1, name= "Z")
		with tf.name_scope("layer2"):
			W2 = tf.get_variable("W2", shape=[128, 128], initializer = tf.truncated_normal_initializer(0, 0.02))
			b2 = tf.get_variable("b2", shape=[1, 128], initializer=tf.constant_initializer(0.0))
			A2 = tf.add(tf.matmul(Z1, W2), b2, name="A")
			Z2 = tf.nn.relu(A2, name="Z")
		with tf.name_scope("outputLayer"):
			W3 = tf.get_variable("W3", shape=[128, self.output_size], initializer = tf.truncated_normal_initializer(0, 0.02))
			b3 = tf.get_variable("b3", shape=[1, self.output_size], initializer=tf.constant_initializer(0.0))
			self.Qprime = tf.add(tf.matmul(Z2, W3), b3, name="output")
		self.P = tf.argmax(self.Qprime, 1, name="prectedAction")
		self.Qmean = tf.reduce_mean(tf.reduce_max(self.Qprime, axis = 1))
		self.QmeanSummary = tf.summary.scalar("Qmean", self.Qmean)
		self.weights = [W1, b1, W2, b2, W3, b3]

	def defineTrainer(self):
		return tf.train.GradientDescentOptimizer(learning_rate = HP['learning_rate'])

	def preprocess(self, input_val):
		return input_val
