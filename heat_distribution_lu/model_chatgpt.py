import numpy as np

Model = type('Model', (), {})

Model.u = (lambda self, x, y: 2 * x + y ** 2)

Model.get_initial_distribution = (lambda self: (lambda matrix: ([
    [matrix.__setitem__((x, y), self.u(x * self.nx, y * self.ny)) for y in range(len(matrix[x]))] for x in [0, len(matrix) - 1]
], [
    [matrix.__setitem__((x, y), self.u(x * self.nx, y * self.ny)) for x in range(len(matrix))] for y in [0, len(matrix[0]) - 1]
], matrix)[-1])(np.zeros(self.shape)))

Model.__init__ = (lambda self, nx, ny, dimensionality: (setattr(self, 'shape', (int(dimensionality[0] / nx), int(dimensionality[1] / ny))), setattr(self, 'nx', nx), setattr(self, 'ny', ny), setattr(self, 'initial_distribution', self.get_initial_distribution()), None)[-1])
