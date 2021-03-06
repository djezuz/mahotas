=====================
Principles of Mahotas
=====================
The Why of mahotas
------------------

Here are the principles of mahotas, in decreasing order of importance:

1. Just work
2. Well documented
3. Fast code
4. Simple code
5. Minimal dependencies

Just work
---------

The first principle is that things should *just work*. This means two things:
(1) there should be no bugs, and (2) interfaces should be flexible or fail
well.

To avoid bugs, tests are extensively used. Every reported bug leads to a new
test case, so that it never happens again. New features should at least have a
smoke test (test that runs the feature and verifies some basic properties of
the output).

Interfaces are designed to be as flexible as possible. No specific types are
required unless it is really needed or in performance-enhancing features (such
as using ``out`` parameters).

The user should never be able to crash the Python interpreter with mahotas.

Well documented
---------------

No public function is without a complete docstring. In addition to that *hard
documentation*, there is also *soft documentation* with examples.

Fast code
---------

The code should be as fast as possible without sacrificing generality (see
*just work* above). This is why C++ templates are used for type independent
code.

Simple code
-----------

The code should be simple.

Minimal dependencies
--------------------

Try to avoid dependencies. Right now, building mahotas depends on a C++
compiler, numpy. These are unlikely to ever change. To run mahotas, we need
numpy and either imread or freeimage.

The imread/freeimage dependency is a soft dependency: everything, except for imread
works without it. The code is written to ensure that ``import``-ing mahotas
without freeimage will not trigger an error unless the ``imread()`` function is
used.

