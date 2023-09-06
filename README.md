# status_estimator_of_walls
A simple POC (Proof of Concept) implementation for computer vision in the construction industry, where building walls and laying bricks is done by programmed robots. The project aims to create "eyes" for such a robot.

This code is meant to be a very small step towards a vision system for brick laying robots.
It contains no neural networks for classification, it would come on next steps.
This project does the following functions:
- takes a jpg image of wall as an input.
- does image analysis to detect the bricks in the wall image.
- builds a wall object according to the data extracted from the image analysis.
- can build wall objects given wall dimensions only: hieght and width.
- can compare between a desired destination (numerical wall object), and the actual wall object built from the image.
