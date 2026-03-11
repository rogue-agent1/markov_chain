#!/usr/bin/env python3
"""markov_chain — Text generation using Markov chains. Zero deps."""
import sys, random

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = {}
        self.starts = []

    def train(self, text):
        words = text.split()
        if len(words) <= self.order:
            return
        for i in range(len(words) - self.order):
            key = tuple(words[i:i+self.order])
            nxt = words[i+self.order]
            self.chain.setdefault(key, []).append(nxt)
            if i == 0 or words[i-1].endswith('.'):
                self.starts.append(key)

    def generate(self, length=50, seed=None):
        if seed:
            random.seed(seed)
        if not self.starts:
            return ""
        key = random.choice(self.starts)
        result = list(key)
        for _ in range(length - self.order):
            options = self.chain.get(key)
            if not options:
                key = random.choice(self.starts)
                continue
            nxt = random.choice(options)
            result.append(nxt)
            key = tuple(result[-self.order:])
        return ' '.join(result)

    def stats(self):
        total_transitions = sum(len(v) for v in self.chain.values())
        return {
            'states': len(self.chain),
            'transitions': total_transitions,
            'starts': len(self.starts),
            'avg_options': total_transitions / len(self.chain) if self.chain else 0
        }

def main():
    sample = """The quick brown fox jumps over the lazy dog. The quick brown cat
    sits on the lazy mat. The lazy dog sleeps in the sun. The brown fox runs
    through the forest. The quick rabbit hops over the fence. The lazy cat
    watches the quick brown fox. The sun sets over the lazy town."""
    mc = MarkovChain(order=2)
    mc.train(sample)
    stats = mc.stats()
    print(f"Markov chain (order={mc.order}):")
    print(f"  States: {stats['states']}, Transitions: {stats['transitions']}")
    print(f"\nGenerated text:")
    for i in range(3):
        print(f"  {i+1}. {mc.generate(20, seed=i)}")

if __name__ == "__main__":
    main()
