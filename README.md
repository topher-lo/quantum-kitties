# Quantum Kitties
A furry web-browser game that demonstrates quantum superposition and entanglement on IBM's quantum computer.

The game was developed as a project at [ICHack19](https://ichack.org/). We placed 2nd in the "Best Newcomer Category".

## Inspiration
We wanted to learn the fundementals of quantum computing and found the idea of putting "Schrödinger's cats" on the web hilarious.

## What it does
1) Each quantum kitty is represented by 3 qubits. 
2) At the start of the game, random pairs ("twins") of kitties are entangled.
3) The player chooses quantum kittens to put into Schrödinger's quantum black box, i.e. to put these kittens into superposition.
4) Backend builds a quantum circuits to entangle kitty twins and put choosen kitties into superposition.
5) Sends circuit instructions either to IBM's quantum simulator or one of IBM Q's three working quantum computers.
6) Measure the kitties in superposition to find out if the chosen kitties collapsed into a "dead" or "alive" state.

## How we built it
Front-end: HTML, Bulma (CSS Framework), (some) Javascript
Back-end: Python on Django, QISkit, Matplotlib

## Challenges we ran into
Learning how quantum circuits work.

## Accomplishments that we’re proud of
We learned the basics of quantum circuits.

## What we learned
How to manipulate qubits via quantum circuit gates and build simple quantum programs. 

## What’s next for Quantum Kitties
Benevolent dictatorship: twins are spared the horror of Schrödinger's black box.
