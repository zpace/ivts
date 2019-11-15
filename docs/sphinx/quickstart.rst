
.. _quickstart:

Getting started with ivts
===============================

`ivts` works by helping you generate draws from a probability distribution by transforming the unit-uniform: to use a specific probability distribution, specify its functional form and its inverse-CDF!

At present, I've written iCDFs for the linear distribution (:class:`ivts.dists.Linear`) and a single (non-broken) power law (:class:`ivts.dists.BoundedPowerLaw`)

Here's how you build your own distribution:

1) Write down your probability density function (PDF), :math:`p(x)`, which need not be normalized

2) Find your un-normalized cumulative distribution function (CDF), by integrating the PDF. Then find the normalization constant by integrating over the domain :math:`(a, b)`:

.. math::
    P(x) = K \int p(x) dx

.. math::
    K = \left( \int_a^b p(x) dx \right)^{-1}

3) And find a way to invert :math:`P(x)`. So you solve the equation

.. math::
    P(P^{-1}(u)) = u

for :math:`P(x)`. `ivts` works when you can write down a functional form for :math:`P(x)`, but in principle would work if you can numerically invert :math:`P(x)`.
