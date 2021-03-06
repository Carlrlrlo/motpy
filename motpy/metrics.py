import numpy as np
from scipy.spatial.distance import cdist


def calculate_iou(bboxes1, bboxes2, dim: int = 2):
    """ expected bboxes size: (-1, 2*dim) """
    bboxes1 = np.array(bboxes1).reshape((-1, dim * 2))
    bboxes2 = np.array(bboxes2).reshape((-1, dim * 2))

    coords_b1 = np.split(bboxes1, 2 * dim, axis=1)
    coords_b2 = np.split(bboxes2, 2 * dim, axis=1)

    coords_tl, coords_br = dict(), dict()  # tl and br points
    val_inter, val_b1, val_b2 = 1.0, 1.0, 1.0
    for d in range(dim):
        coords_tl[d] = np.maximum(coords_b1[d], np.transpose(coords_b2[d]))
        coords_br[d] = np.minimum(coords_b1[d + dim], np.transpose(coords_b2[d + dim]))

        val_inter *= np.maximum(coords_br[d] - coords_tl[d], 0)
        val_b1 *= coords_b1[d + dim] - coords_b1[d]
        val_b2 *= coords_b2[d + dim] - coords_b2[d]

    iou = val_inter / (val_b1 + np.transpose(val_b2) - val_inter)
    return iou


def angular_similarity(vectors1, vectors2):
    sim = 1 - cdist(vectors1, vectors2, 'cosine') / 2  # kept in range <0,1>
    return sim
