# Solving problems thrown at them
# Manual vs learning with Neural Network / Machine Learning

# Problem: a girl notes down the colour, length and width of her flowers,
# all of her flowers have been recorded with the common red or blue,
# but it seems that she has forgotten to write down the colour of her last
# flower.

template = ["colour", "length", "width"]

dataset = [
    ["red", 3, 1.5],
    ["blue", 2, 1],
    ["red", 4, 1.5],
    ["blue", 3, 1],
    ["red", 3.5, 0.5],
    ["blue", 2, 0.5],
    ["red", 5.5, 1],
    ["blue", 1, 1],
    ["?", 4.5, 1]
]

# Manual way 1: get the average value of widthXlength for red/blue, then
# compare.
# Manual way 2: graphing a scatter plot, with the lengthxwidth being x/y values,
# with the red/blue colour going on the plot. Plot the mystery value,
# and see where it resides amongst the other colours.

# Cost function is "how bad our computer is going"
# Takes in the data and predictions to the cost function,
# which tells us how bad the computer is.
# We want to "minimize" the cost output.
