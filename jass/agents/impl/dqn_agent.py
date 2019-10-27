import torch
import torch.nn.functional as F
from torch import nn
from torch import optim

from jass.agents.action import ChooseTrumpAction, PlayCardAction
from jass.agents.agent import Agent
from jass.agents.impl.random_agent import RandomAgent
from jass.agents.state import ChooseTrumpState, PlayCardState, State
from jass.agents.util.policy import Policy, EpsilonGreedyPolicy
from jass.agents.util.replay_memory import ReplayMemory, SARS
from jass.models.linear_dqn import LinearDQN

BATCH_SIZE = 128
GAMMA = 0.9  # 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10
MEMORY_CAPACITY = 10000

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DQNPolicy(Policy):
    def __init__(self, policy_net: nn.Module):
        self.policy_net = policy_net

    def __call__(self, state: State) -> State:
        with torch.no_grad():
            action_tensor = self.policy_net(state.tensor.unsqueeze(0)).squeeze()
            action_tensor -= action_tensor.min()
            action_tensor += 1
            action_tensor *= state.action_tensor_mask.float()
            # print(action_tensor)
            return state.action_type.from_tensor(action_tensor)


class DQNAgent(Agent):

    def __init__(self, train=True, state_dict=None):
        self.num_episode = 0
        self.train = train
        self.policy_net = LinearDQN.for_state(PlayCardState).to(device)
        self.policy = DQNPolicy(self.policy_net)
        if state_dict is not None:
            self.policy_net.load_state_dict(state_dict)

        if self.train:
            self.target_net = LinearDQN.for_state(PlayCardState).to(device)
            self.target_net.load_state_dict(self.policy_net.state_dict())  # same weights
            self.target_net.eval()

            self.optimizer = optim.RMSprop(self.policy_net.parameters())
            self.memory = ReplayMemory(MEMORY_CAPACITY)

            self.policy = EpsilonGreedyPolicy(
                original_policy=self.policy,
                eps_start=EPS_START,
                eps_end=EPS_END,
                eps_decay=EPS_DECAY,
            )
        self.prev_state = None
        self.prev_action = None
        self.prev_reward = None

    def play_card(self, state: PlayCardState) -> PlayCardAction:
        if self.prev_state is not None and self.train:
            sars = SARS(self.prev_state, self.prev_action, self.prev_reward, state)
            self.memory.push(sars)
            self.optimize_model()

        action = self.policy(state)
        self.prev_state = state
        self.prev_action = action
        return action

    def trick_end(self, reward: int, done: bool):
        self.prev_reward = reward
        if done and self.train:
            if self.num_episode % TARGET_UPDATE == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())
            self.num_episode += 1
            if self.num_episode % 20 == 0:
                torch.save(self.policy_net.state_dict(),
                           f'/Users/greg/Data/AI/jass/policy_net_v1/policy_net_v2_ep_{self.num_episode // 20:04d}.ckpt')
            sars = SARS(self.prev_state, self.prev_action, reward, None)
            self.memory.push(sars)
            self.optimize_model()

    def choose_trump(self, state: ChooseTrumpState) -> ChooseTrumpAction:
        ## todo this is can be done with dqn as well
        return RandomAgent.choose_trump(state)

    def optimize_model(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = self.memory.sample(BATCH_SIZE)

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor([not sars.is_final for sars in batch], device=device, dtype=torch.bool)
        non_final_next_states = torch.stack([sars.next_state.tensor for sars in batch if not sars.is_final])

        state_batch = torch.stack([sars.state.tensor for sars in batch])
        action_batch = torch.stack([sars.action.tensor for sars in batch])
        reward_batch = torch.tensor([sars.reward for sars in batch])

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch)[action_batch.bool()]  # .gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1)[0].
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(BATCH_SIZE, device=device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * GAMMA) + reward_batch.float()

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values)

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

#
# num_episodes = 50
# for i_episode in range(num_episodes):
#     # Initialize the environment and state
#     env.reset()
#     last_screen = get_screen()
#     current_screen = get_screen()
#     state = current_screen - last_screen
#     for t in count():
#         # Select and perform an action
#         action = select_action(state)
#         _, reward, done, _ = env.step_(action.item())
#         reward = torch.tensor([reward], device=device)
#
#         # Observe new state
#         last_screen = current_screen
#         current_screen = get_screen()
#         if not done:
#             next_state = current_screen - last_screen
#         else:
#             next_state = None
#
#         # Store the transition in memory
#         memory.push(state, action, next_state, reward)
#
#         # Move to the next state
#         state = next_state
#
#         # Perform one step of the optimization (on the target network)
#         optimize_model()
#         if done:
#             episode_durations.append(t + 1)
#             # plot_durations()
#             break
#     # Update the target network, copying all weights and biases in DQN
#     if i_episode % TARGET_UPDATE == 0:
#         target_net.load_state_dict(policy_net.state_dict())
#
# print('Complete')
