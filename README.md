# Rubic's cube solver with Lego Mindstorms EV3

This is a hobby project to solve Rubic's cube by using Lego Mindstorms EV3. Both the physical design and code are original. High-level idea was gotten from other similar projects but on purpose they were not used as reference. Afaik, the most well-known solution with good building instructions is [MindCuber](http://mindcuber.com/).

This solution uses [ev3dev](http://www.ev3dev.org/) that is a full Linux operating system that runs on top of Lego Mindstorms EV3. Code is written in Python by using the Python binding for ev3dev ([1](https://github.com/rhempel/ev3dev-lang-python), [2](https://sites.google.com/site/ev3python/)) that allows controlling motors and sensors easily. The code could be run directly in the EV3 but I've preferred using [RPyC server](http://ev3dev-lang-python.readthedocs.io/en/latest/rpyc.html). See also instructions how to [share internet via bluetooth for EV3](http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/).

![Physical structure of the Rubic's cube solver](https://cloud.githubusercontent.com/assets/10807957/21730845/3c5da95a-d45a-11e6-9396-857b790677ab.png)

## About the solution

My main interest in the project was to get the physical structure working and to be able to control the motors and sensors smoothly with Python. The solution can be divided into four parts:

### 1. Physical controls

The solutions uses three motors and one color sensor. Referring to the above pic, the left most motor, called **lift**, is used to roll the cube. The second motor, called **base**, on top of which the cube rests, is used to turn the cube. The last motor, called **hand**, can either hold the top two layers of the cube on place while the base rotates (current state in the above pic), or move the color sensor to measurement position. For each of these physical control, there is a separate python class, namely *Base*, *Hand* and *Lift*.

When each of these classes are initiated, motors reset their positions. Lift finds both extreme positions. Hand touches the rubic cube to find its extreme. Base assume that it's aligned when inited.

### 2. Rubic's cube movements

There is a standard notation how Rubic's cube movements are marked. For example, R means that rotate the right face clockwise 90 degrees. See the full [notation](https://ruwix.com/the-rubiks-cube/notation/) for reference. Given the individual physical controls, the *Mover* class allows using standard Rubic's cube movement notation to modify the cube. To make a single move, it first orients the cube such that the desired face is on bottom and then uses hand to keep it on place while turning the face.

### 3. Measuring the cube's initial state

Python class called *Inspector* uses Hand's color measurement sensor to measure the initial state of the rubic cube. The measurement is currently quite unstable and still under work. Identifying the color is hard and depends on the lighting. Especially detecting red and orange from each other can fail. Also aligning the cube and sensor needs to be very exact. If the measurement fails, the initial state can be input by hand.

### 4. Finding the solution

Given the initial state, the solution uses currently [Ruwix online Rubic's cube solver](https://ruwix.com/online-rubiks-cube-solver-program/) to find the optimal sequence of movements. As it does not provide direct API access, the cube input format was reverse engineered and the output is read by using [Selenium](http://www.seleniumhq.org/). This can be later replaced by custom solver.

### 5. Joining the parts

There is not a final clean code for this, but the rubic_test.py contains current testing code that has been used to run different parts. It first connects the ev3 by RPyC, initializes the physical control classes, measures initial states, finds the solution path and makes the movements. That's it.
