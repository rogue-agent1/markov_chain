#!/usr/bin/env python3
"""Markov chain text generator."""
import sys, random, collections
order=int(sys.argv[1]) if len(sys.argv)>1 else 2
length=int(sys.argv[2]) if len(sys.argv)>2 else 200
text=sys.stdin.read() if len(sys.argv)<4 else open(sys.argv[3]).read()
chain=collections.defaultdict(list)
for i in range(len(text)-order):
    chain[text[i:i+order]].append(text[i+order])
if not chain: sys.exit("Need more text")
key=random.choice(list(chain.keys())); out=[key]
for _ in range(length):
    if key not in chain: key=random.choice(list(chain.keys()))
    c=random.choice(chain[key]); out.append(c); key=key[1:]+c
print(''.join(out))
