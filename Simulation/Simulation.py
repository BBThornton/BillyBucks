import math
import random

from matplotlib import pyplot as plt


class Event:
    # Event_type: 0 for block, 1 for share
    def __init__(self, time, event_type: int, miner):
        self.time = time
        self.event_type = event_type
        self.miner = miner


class Miner:
    def __init__(self, name, hr):
        self.name = name
        self.hr = hr
        self.mined = 0
        self.shares_this_block = 0
        self.share_history = []
        self.reward_history = []
        self.shares_total = 0
        self.eligible = False
        self.rewards = 0

    def start_mining_block(self, network_difficulty, current_time):
        solve_time = -math.log(1 - random.random()) * (network_difficulty / self.hr)
        # print(self.name, "started mining block at", solve_time)
        event = Event(current_time + solve_time, 0, self)
        return event

    def start_mining_share(self, share_difficulty, current_time):
        solve_time = -math.log(1 - random.random()) * (share_difficulty / self.hr)
        # print(self.name, "started mining share at", solve_time)
        event = Event(current_time + solve_time, 1, self)
        return event

    def new_block(self, network_difficulty, share_difficulty, current_time):
        return self.start_mining_block(network_difficulty, current_time), self.start_mining_share(share_difficulty,
                                                                                                  current_time)

    def reset(self):
        self.share_history.append(self.shares_this_block)
        self.shares_this_block = 0
        self.eligible = False


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, event: Event):
        self.queue.append(event)
        self.queue.sort(key=lambda x: x.time)

    def pop(self):
        return self.queue.pop(0)

    def remove(self, miner):
        for event in self.queue:
            if event.miner == miner:
                self.queue.remove(event)

    def print_index(self, index):
        print(self.queue[index].time)

    def reset(self):
        self.queue = []


def init(pq, miners, network_difficulty, share_difficulty, current_time):
    for miner in miners:
        pq.push(miner.start_mining_block(network_difficulty, current_time))
        pq.push(miner.start_mining_share(share_difficulty, current_time))
    # print(pq.queue)


def reset(pq, miners, network_difficulty, share_difficulty, current_time):
    # resets the miners and the queue then repopulates the queue
    for miner in miners:
        miner.reset()
    pq.reset()
    init(pq, miners, network_difficulty, share_difficulty, current_time)


def update_difficulty(target_time, height, times, difficulties):
    # print("target time:", target_time)
    # print("difficulty:", difficulties[height-1])
    T = target_time
    N = 60
    L = 0
    sum_target = 0
    for i in range(height - N, height):
        L += max(-4*T,min(6 * T, times[i]-times[i-1]))*i
    if L < N * N * target_time / 20:
        L = N * N * target_time / 20

    average_D = (sum(difficulties[height - N:height]) / N)

    if average_D > 2000000 * N * N * target_time:
        next_D = (average_D / (200 * L)) * (N * (N + 1) * target_time * 99)
    else:
        next_D = (average_D * N * (N + 1) * target_time * 99) / (200 * L)

    i = 1000000000
    while (i > 1):
        if next_D > i * 100:
            next_D = ((next_D + i / 2) / i) * i
            break
        else:
            i /= 10

    return next_D


def TimeToBlock():
    num_blocks = 50
    miner = Miner("miner", 50)
    target_time = 30
    network_difficulty = target_time
    avg_complete = 0
    avg_share = 0
    for i in range(num_blocks):
        avg_complete += miner.start_mining_block(network_difficulty, 0).time
        avg_share += miner.start_mining_share(share_difficulty=network_difficulty / 100, current_time=0).time
    print("average time to mine block:", avg_complete / num_blocks)
    print("average time to mine share:", avg_share / num_blocks)


def main_loop(num_bl, hrs):
    num_blocks = num_bl
    pq = PriorityQueue()
    miners = [Miner("Miner 1", hrs[0]), Miner("Miner 2", hrs[1]), Miner("Miner 3", hrs[2])]

    target_time = 30  # seconds
    network_difficulty = target_time * sum(hrs)*2
    # print("Network difficulty:", network_difficulty)

    """
    Allow the faster miner to keep mining
    the block probaility for the fastest miner << the share probaility for the slowest miner * threshold
    
    """

    threshold = 10

    share_difficulty = network_difficulty / (threshold * len(miners))
    # share_difficulty = 4

    current_time = 0
    init(pq, miners, network_difficulty, share_difficulty, current_time)

    eligible_count = 0
    reward = 100

    block_completion_time = [0]
    difficulties = [0]

    while num_blocks > 0:
        # Get the next event
        event = pq.pop()

        current_time = event.time
        if event.event_type == 1:
            # Share event
            miner = event.miner
            miner.shares_this_block += 1
            miner.shares_total += 1
            if miner.shares_this_block >= threshold and miner.hr > 2:
                # miner is done remove all remaining events for this miner
                pq.remove(miner)
                miner.eligible = True
                eligible_count += 1
            else:
                pq.push(miner.start_mining_share(share_difficulty, current_time))
        else:
            print(num_bl - num_blocks)

            # print("BLOCK EVENT")
            # Block event
            block_completion_time.append((current_time*1000 - sum(block_completion_time)))
            difficulties.append(network_difficulty)
            # if len(block_completion_time) > 65:
            #     network_difficulty = update_difficulty(target_time, len(block_completion_time), block_completion_time,
            #                                            difficulties)
            #     print("network difficulty:", network_difficulty)
            #     share_difficulty = network_difficulty / (threshold * len(miners))

            miner = event.miner

            miner.eligible = True
            eligible_count += 1

            miner.mined += 1
            num_blocks -= 1
            for miner in miners:
                if miner.eligible:
                    miner.rewards += reward / eligible_count
                    miner.reward_history.append(reward / eligible_count)
                else:
                    miner.reward_history.append(0)

            eligible_count = 0
            reset(pq, miners, network_difficulty, share_difficulty, current_time)

    print("Block completion time:", sum(block_completion_time) / len(block_completion_time))

    for miner in miners:
        print(miner.name, miner.mined)
        print(miner.name, miner.shares_total / num_bl)
        print(miner.name, miner.rewards)

    import numpy as np

    fig, ax = plt.subplots()
    n = 5000
    ax.set_ylim(0,18)
    plt.subplots_adjust(left=0.2, bottom=0.2)
    time = list(range(0, len(miners[0].share_history), n))
    average_shares_miner0 = [sum(miners[0].share_history[i:i + n]) / n for i in
                             range(0, len(miners[0].share_history), n)]
    average_shares_miner1 = [sum(np.add(miners[1].share_history[i:i + n],1.5)) / n for i in
                             range(0, len(miners[1].share_history), n)]
    average_shares_miner2 = [sum(miners[2].share_history[i:i + n]) / n for i in
                             range(0, len(miners[2].share_history), n)]
    ax.plot(time, average_shares_miner0, label="Miner HR = 1")
    ax.plot(time, average_shares_miner1, label="Miner HR = 10")
    ax.plot(time, average_shares_miner2, label="Miner HR = 50")
    ax.set_title("Average Number of Shares Submitted per 5000 Block Cycles \n Using the Balanced Mining Framework")
    ax.set_xlabel("Block Number/Height")
    ax.set_ylabel("Average Number of submitted shares \n (Averaged over 5000 Block Cycles)")

    ax.legend()
    plt.show()
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.2)
    time = list(range(len(block_completion_time) - 1))
    ax.set_title("Cumulative Reward Generated By Different Hash Rate Miners \n Using the Balanced Mining Framework")
    ax.set_xlabel("Block Number/Height")
    ax.set_ylabel("Cumulative Reward (BillyBucks)")
    ax.plot(time, np.cumsum(miners[0].reward_history), label="Miner HR = 1")
    ax.plot(time, np.cumsum(miners[1].reward_history), label="Miner HR = 10")
    ax.plot(time, np.cumsum(miners[2].reward_history), label="Miner HR = 50")
    ax.legend()
    plt.show()


def without_balancing(num_bl, hrs):
    num_blocks = num_bl
    pq = PriorityQueue()
    miners = [Miner("Miner 1", hrs[0]), Miner("Miner 2", hrs[1]), Miner("Miner 3", hrs[2])]

    target_time = 30  # seconds
    network_difficulty = target_time * sum(hrs)
    # print("Network difficulty:", network_difficulty)

    """
    Allow the faster miner to keep mining
    the block probaility for the fastest miner << the share probaility for the slowest miner * threshold

    """

    threshold = 10
    share_difficulty = network_difficulty / (threshold * len(miners))
    # share_difficulty = 4

    current_time = 0
    init(pq, miners, network_difficulty, share_difficulty, current_time)

    eligible_count = 0
    reward = 100

    block_completion_time = [0]
    difficulties = [0]

    while num_blocks > 0:
        # Get the next event
        event = pq.pop()

        current_time = event.time
        if event.event_type == 1:
            # Share event
            miner = event.miner
            miner.shares_this_block += 1
            miner.shares_total += 1
            pq.push(miner.start_mining_share(share_difficulty, current_time))
        else:
            block_completion_time.append(current_time*1000)
            difficulties.append(network_difficulty)
            miner = event.miner
            miner.mined += 1
            num_blocks -= 1
            miner.shares_this_block += 1
            total_shares = 0
            for miner in miners:
                total_shares += miner.shares_this_block
            for miner in miners:
                if miner.shares_this_block > 0:
                    miner.rewards += reward * (miner.shares_this_block / total_shares)
                    miner.reward_history.append(reward * (miner.shares_this_block / total_shares))
                else:
                    miner.reward_history.append(0)

            reset(pq, miners, network_difficulty, share_difficulty, current_time)

    print("Block completion time:", sum(block_completion_time) / len(block_completion_time))

    for miner in miners:
        print(miner.name, miner.mined)
        print(miner.name, miner.shares_total / num_bl)
        print(miner.name, miner.rewards)

    import numpy as np

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.2)
    n = 5000
    time = list(range(0, len(miners[0].share_history), n))
    average_shares_miner0 = [sum(miners[0].share_history[i:i + n]) / n for i in
                             range(0, len(miners[0].share_history), n)]
    average_shares_miner1 = [sum(np.add(miners[1].share_history[i:i + n],3)) / n for i in
                             range(0, len(miners[1].share_history), n)]
    average_shares_miner2 = [sum(miners[2].share_history[i:i + n]) / n for i in
                             range(0, len(miners[2].share_history), n)]
    ax.plot(time, average_shares_miner0, label="Miner HR = 1")
    ax.plot(time, average_shares_miner1, label="Miner HR = 10")
    ax.plot(time, average_shares_miner2, label="Miner HR = 50")
    ax.set_title("Average Number of Shares Submitted per 5000 Block Cycles \n Without the Balanced Mining Framework")
    ax.set_xlabel("Block Number/Height")
    ax.set_ylabel("Average Number of submitted shares \n (Averaged over 5000 Block Cycles)")
    ax.legend()
    plt.show()
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.2, bottom=0.2)
    time = list(range(len(block_completion_time) - 1))
    ax.set_title("Cumulative Reward Generated By Different Hash Rate Miners \n Without the Balanced Mining Framework")
    ax.set_xlabel("Block Number/Height")
    ax.set_ylabel("Cumulative Reward (BillyBucks)")
    ax.plot(time, np.cumsum(miners[0].reward_history), label="Miner HR = 1")
    ax.plot(time, np.cumsum(miners[1].reward_history), label="Miner HR = 10")
    ax.plot(time, np.cumsum(miners[2].reward_history), label="Miner HR = 50")
    ax.legend()
    plt.show()


if __name__ == '__main__':
    import seaborn as sns

    sns.set_theme()
    main_loop(100000, [1, 10, 50])
    without_balancing(100000, [1, 10, 50])
    # TimeToBlock()
