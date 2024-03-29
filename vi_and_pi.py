# Names: Sofia McKerrow and Wenpeng Jiang
# Student IDs: s3626804, s3674270

### MDP Value Iteration and Policy Iteration
### Acknowledgement: start-up codes were adapted with permission from Prof. Emma Brunskill of Stanford University

import numpy as np
import gym
import time
import rmit_rl_env

np.set_printoptions(precision=3)

"""
For policy_evaluation, policy_improvement, policy_iteration and value_iteration,
the parameters P, nS, nA, gamma are defined as follows:

	P: nested dictionary
		From gym.core.Environment
		For each pair of states in [1, nS] and actions in [1, nA], P[state][action] is a
		tuple of the form (probability, nextstate, reward, terminal) where
			- probability: float
				the probability of transitioning from "state" to "nextstate" with "action"
			- nextstate: int
				denotes the state we transition to (in range [0, nS - 1])
			- reward: int
				either 0 or 1, the reward for transitioning from "state" to
				"nextstate" with "action"
			- terminal: bool
			  True when "nextstate" is a terminal state (hole or goal), False otherwise
	nS: int
		number of states in the environment
	nA: int
		number of actions in the environment
	gamma: float
		Discount factor. Number in range [0, 1)
"""

def policy_evaluation(P, nS, nA, policy, gamma=0.9, tol=1e-3):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	policy: np.array[nS]
		The policy to evaluate. Maps states to actions.
	tol: float
		Terminate policy evaluation when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns
	-------
	value_function: np.ndarray[nS]
		The value function of the given policy, where value_function[s] is
		the value of state s
	"""

	value_function = np.zeros(nS)

	############################
	# YOUR IMPLEMENTATION HERE #
	
	while True:
		old_value_function = np.copy(value_function)

		# iterate through each state
		for state in range(nS):
			policy_action = policy[state]
			# calculate the value function under the policy
			value_function[state] = sum([prob * (reward + gamma * old_value_function[next_state]) \
				for prob, next_state, reward, terminal in P[state][policy_action]])

		# if values have converged, stop iterations
		if (np.sum((np.fabs(old_value_function - value_function))) <= tol):
			break

	############################
	
	return value_function

def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new_policy: np.ndarray[nS]
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""

	new_policy = np.zeros(nS, dtype='int')

	############################
	# YOUR IMPLEMENTATION HERE #

	# iterate through each state
	def one_step_look_ahead(P, state, nA, value_from_policy, gamma=0.9):
		action_values = np.zeros(nA)

		for action in range(nA):
			for prob,next_state,reward,terminal in P[state][action]:
				#sum value of all possible state in with action
				action_values[action] += prob * (reward + (gamma * value_from_policy[next_state]))
		return action_values

	for state in range(nS):
		#one step look ahead
		action_values = one_step_look_ahead(P, state, nA, value_from_policy, gamma)
		new_policy[state] = np.argmax(action_values)
	
	############################
	
	return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, tol=10e-3):
	"""Runs policy iteration.

	You should call the policy_evaluation() and policy_improvement() methods to
	implement this method.

	Parameters
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		tol parameter used in policy_evaluation()
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)

	############################
	# YOUR IMPLEMENTATION HERE #

	max_iterations = 100000
	
	for i in range(max_iterations):
		# get state value function for policy
		value_function = policy_evaluation(P, nS, nA, policy, gamma, tol)
		# use the state value function to improve the policy
		new_policy = policy_improvement(P, nS, nA, value_function, policy, gamma)

		# check if the policy has converged
		if (np.all(policy == new_policy)):
			print ('Policy converged in %d iterations.' %(i+1))
			break
		
		# update the policy
		policy = new_policy

	############################
	
	return value_function, policy

def value_iteration(P, nS, nA, gamma=0.9, tol=1e-3):
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P, nS, nA, gamma:
		defined at beginning of file
	tol: float
		Terminate value iteration when
			max |value_function(s) - prev_value_function(s)| < tol
	Returns:
	----------
	value_function: np.ndarray[nS]
	policy: np.ndarray[nS]
	"""

	value_function = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)

	############################
	# YOUR IMPLEMENTATION HERE #

	max_iterations = 200000
	
	for i in range(max_iterations):
		# stopping condition
		delta = 0

		# iterate through each state
		for state in range(nS):
			actions_values = np.zeros(nA)

			# loop over possible actions
			for act in range(nA):
				for prob, next_state, reward, done in P[state][act]:
					# use Bellman equation to get action values
					actions_values[act] += prob * (reward + gamma * value_function[next_state])

			# get the highest action value
			best_action_value = max(actions_values)

			# get the biggest difference between best action value and the previous value function
			delta = max(delta, abs(best_action_value - value_function[state]))

			# update value function for the current state
			value_function[state] = best_action_value

			# update the policy based on the best action
			best_action = np.argmax(actions_values)
			policy[state] = best_action
		
		# check if the values have reached convergence -> iterations can stop
		if delta < tol * (1 - gamma) / gamma:
			print ('Value iteration converged in %d iterations.' %(i+1))
			break

	############################

	return value_function, policy

def render_single(env, policy, max_steps=100):
  """
    This function does not need to be modified
    Renders policy once on environment. Watch your agent play!

    Parameters
    ----------
    env: gym.core.Environment
      Environment to play on. Must have nS, nA, and P as
      attributes.
    Policy: np.array of shape [env.nS]
      The action to take at a given state
  """

  episode_reward = 0
  ob = env.reset()
  for t in range(max_steps):
    env.render()
    time.sleep(0.25)
    a = policy[ob]
    ob, rew, done, _ = env.step(a)
    episode_reward += rew
    if done:
      break
  env.render();
  if not done:
    print("The agent didn't reach a terminal state in {} steps.".format(max_steps))
  else:
  	print("Episode reward: %f" % episode_reward)


# Edit below to run policy and value iteration on different environments and
# visualize the resulting policies in action!
# You may change the parameters in the functions below
if __name__ == "__main__":

	# comment/uncomment these lines to switch between deterministic/stochastic environments
	# env = gym.make("Deterministic-4x4-FrozenLake-v0")
	env = gym.make("Stochastic-4x4-FrozenLake-v0")

	print("\n" + "-"*25 + "\nBeginning Policy Iteration\n" + "-"*25)

	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_pi, 100)

	print("\n" + "-"*25 + "\nBeginning Value Iteration\n" + "-"*25)

	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, tol=1e-3)
	render_single(env, p_vi, 100)


