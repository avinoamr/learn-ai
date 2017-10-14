# We are now able to find N x-values such that:
#
#   f(x) = TARGET ; x = ?
#
# But the real-life use-cases are exactly inversed: we're given an input X
# vector and we need to find the answer:
#
#   f(x) = ?
#
# of course, we don't know what f does. But lets start by first covering all
# linear functions[1], thus ones that can be reduced to the form:
#
#   f(x,y,z, ...) = ax + by + cz + ... + C = ?
#
# Where the x values are given. All that's left for us to do is to discover the
# weights (a, b, c, ...) & bias (C). These weights are encoded in a w-vector
# that we'll need to learn as we're given examples of inputs and outputs.
#
# Similarily the bias is a single scalar we'll need to learn, in exactly the
# same way as the other weights. So supporting it might include a duplication
# of the same code used for the weights. Instead of duplicating the code, we can
# just regard the bias as 1 extra weight to be learned (N + 1), with the
# exception that the input for that weight is always 1. In other words, the bias
# behaves just like a normal weight for an input that's always fixed at 1.
#
# [1] Of course, that's an unsubstentiated assumption to make for many use
# cases. Generally, there are two ways to generalize for non-linear functions:
#   1. We can extend the input to include polynomial components. Instead of just
#       using the input as is, we can first produce multiple copies of the same
#       inputs, only raised to the power of 2, 3, etc.
#   2. Using hidden layers. A concept I will maybe cover later.
#
import numpy as np

# no constant TARGET; we need to find it.
N = 3
E = 0.0001
STEP = 0.01
ITERATIONS = 1000

# slightly different implementation of f() just for fun:
#   f(X) = 10 + 8x1 -2x2 + x3/2
#
# So the learned weights are [8, -2, .5] and the bias 10.
#
# Notice that this code will not be able to learn non-linear functions (x^2).
# But many real-life situations can be reduced to a linear expression.
def f(X):
    return 10 + 8 * X[0] - 2 * X[1] + X[2] / 2

# same loss function as before, except that now it can't rely on a constant
# TARGET value for all inputs, but instead it receives the value as input
def loss(actual, target):
    return (actual - target) ** 2

# initial weights. before we've learned the input, now that the input is given
# and immutable we learn the weights by which to multiply this input. In fact,
# these weights can represent any linear function, so all that's left to do is
# find these weights and we have our function approximation!
w = np.random.rand(1 + N) * 2 - 1 # 1-extra weight for the bias at index 0
for j in xrange(ITERATIONS): # can we stop early once we reach our target?

    # first we need a new input for each iteration. In reality, we should
    # receive these inputs from an external training data set. But for now we'll
    # cheat, by just randomizing an input
    inp = np.random.rand(N) * 2 - 1 # cheat.

    # the target, or correct value, for this input
    target = f(inp)

    # we start by making our prediction. Again, because it's assumed to be a
    # linear function, thus it must be reducible to the form of:
    #
    #   f(x) = w1x1 + w2x2 + w3x3 + ... + C = ?
    #
    # thus we need to multiply all inputs with their weights, element wise, and
    # sum up the result.
    inp = np.insert(inp, 0, 1.) # inject a fixed input of 1 for the bias weight
    out = sum(inp * w)

    # now, lets find our current loss - comparing our prediction to the actual
    # value produced by f():
    l = loss(out, target)
    print "#%d f(%s) = %f (loss: %f)" % (j, inp, target, l)

    # just as before, we now want to make infinitisimal changes to our weights,
    # in order to find how the loss changes w.r.t to every individual weight.
    # This is identical to what we did before.
    d = np.zeros(1 + N) # N derivatives - one per weight
    for i in range(1 + N):
        # add an inifinitsimal change to the current index of the input. It's an
        # immutable version of: w[i] += E
        e = np.zeros(1 + N)
        e[i] = E

        # sample the loss function after adding E to w[i]
        # we're making a new prediction, just like before, only now we add the
        # epsilon to the current weight i. Also notice that the target of our
        # loss doesn't change obviously (because the inp is the same), only the
        # predition does
        li = loss(sum(inp * (w + e)), target)

        # derviative of the input - or how the loss() changes w.r.t inp[i]
        d[i] = (li - l) / E

    # now we update the weights, same as before.
    # element-wise update to the new inp in the gradient direction. ie:
    #   inp[i] = STEP * d[i] * - 1 ; for every i in N = all of the inputs
    w += STEP * d * -1

# finally - lets print out our weights to see what we did. You should expect the
# weights to resemble the ones in f(). Remember that the first weight is
# actually the bias
print "W = %s" % w
