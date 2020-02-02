"""Swaps two subsystems within a state or operator."""
from typing import List, Union
import numpy as np
from toqito.perms.permute_systems import permute_systems


def swap(rho: np.ndarray,
         sys: List[int] = None,
         dim: Union[List[int], int] = None,
         row_only: bool = False) -> np.ndarray:
    """
    Swap two subsystems within a state or operator.

    Swaps the two subsystems of the vector or matrix `rho`, where the
    dimensions of the (possibly more than 2) subsystems are given by `dim` and
    the indices of the two subsystems to be swapped are specified in the 1-by-2
     vector `sys`.

    If `rho` is non-square and not a vector, different row and column
    dimensions can be specified by putting the row dimensions in the first row
    of `dim` and the column dimensions in the second row of `dim`.

    If `row_only` is set to `True`, then only the rows of `rho` are swapped,
    but not the columns -- this is equivalent to multiplying `rho` on the left
    by the corresponding swap operator, but not on the right.

    :param rho: A vector or matrix to have its subsystems swapped.
    :param sys: Default: [1, 2]
    :param dim: Default: [sqrt(len(X), sqrt(len(X)))]
    :param row_only: Default: False
    :return: The swapped matrix.
    """
    eps = np.finfo(float).eps
    if len(rho.shape) == 1:
        rho_dims = (1, rho.shape[0])
    else:
        rho_dims = rho.shape

    round_dim = np.round(np.sqrt(rho_dims))

    if sys is None:
        sys = [1, 2]

    if isinstance(dim, list):
        dim = np.array(dim)
    if dim is None:
        dim = np.array([[round_dim[0], round_dim[0]],
                        [round_dim[1], round_dim[1]]])

    if isinstance(dim, int):
        dim = np.array([[dim, rho_dims[0]/dim],
                        [dim, rho_dims[1]/dim]])
        if np.abs(dim[0, 1] - np.round(dim[0, 1])) + \
           np.abs(dim[1, 1] - np.round(dim[1, 1])) >= 2*np.prod(rho_dims)*eps:
            val_error = """
                InvalidDim: The value of `dim` must evenly divide the number of
                rows and columns of `rho`; please provide the `dim` array 
                containing the dimensions of the subsystems.
            """
            raise ValueError(val_error)

        dim[0, 1] = np.round(dim[0, 1])
        dim[1, 1] = np.round(dim[1, 1])
        num_sys = 2
    else:
        num_sys = len(dim)

    # Verify that the input sys makes sense.
    if any(sys) < 1 or any(sys) > num_sys:
        val_error = """
            InvalidSys: The subsystems in `sys` must be between 1 and 
            `len(dim).` inclusive.
        """
        raise ValueError(val_error)
    if len(sys) != 2:
        val_error = """
            InvalidSys: `sys` must be a vector with exactly two elements.
        """
        raise ValueError(val_error)

    # Swap the indicated subsystems.
    perm = list(range(1, num_sys+1))
    perm = perm[::-1]
    return permute_systems(rho, perm, dim, row_only)
