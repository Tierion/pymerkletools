import hashlib
from math import sqrt


class MerkleTools(object):
    def __init__(self, hash_type="sha256"):
        hash_type = hash_type.lower()
        if hash_type not in ["sha256", "md5", ]:
            raise Exception('`hash_type` {} nor supported'.format(hash_type))
        elif hash_type == 'sha256':
            self.hash_function = hashlib.sha256
        elif hash_type == 'md5':
            self.hash_function = hashlib.md5

        self.reset_tree()

    def reset_tree(self):
        self.leaves = list()
        self.levels = None
        self.is_ready = False

    def add_leaf(self, values, do_hash=True):
        self.is_ready = False
        if isinstance(values, tuple) or isinstance(values, list):
            for v in values:
                if do_hash:
                    v = self.hash_function(v).digest()
                self.leaves.append(v)
        else:
            if do_hash:
                v = self.hash_function(values).digest()
            self.leaves.append(v)

    def get_leaf(self, index):
        return self.leaves[index]

    def get_leaf_count(self):
        return len(self.leaves)

    def get_tree_ready_state(self):
        return self.is_ready

    def _calculate_next_level(self):
        solo_leave = None
        N = len(self.levels[0])  # number of leaves on the level
        if N % 2 == 1:  # if odd number of leaves on the level
            solo_leave = self.levels[0][-1]
            N -= 1

        new_level = []
        for l, r in zip(self.levels[0][0:N:2], self.levels[0][1:N:2]):
            new_level.append(self.hash_function(l+r).digest())
        if solo_leave is not None:
            new_level.append(solo_leave)
        self.levels = [new_level, ] + self.levels  # prepend new level

    def make_tree(self):
        self.is_ready = False
        if self.get_leaf_count() > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self._calculate_next_level()
        self.is_ready = True

    def get_merkle_root(self):
        if self.is_ready:
            return self.levels[0][0]
        else:
            return None

    def get_proof(self, index):
        if not self.is_ready or index > len(self.leaves) or index < 0:
            return None
        else:
            proof = []
            for x in range(len(self.levels) - 1, 0, -1):
                level_len = len(self.levels[x])
                if index == level_len - 1 and level_len % 2 == 1:  # skip if level has odd number of leaves
                    index = int(sqrt(index // 2))
                else:
                    is_right_node = index % 2
                    sibling_index = index - 1 if is_right_node else index + 1
                    sibling_pos = "left" if is_right_node else "right"
                    sibling_value = self.levels[x][sibling_index]
                    proof.append({sibling_pos: sibling_value})
                    index = int(sqrt(index // 2))
            return proof

    def validate_proof(self, proof, target_hash, merkle_root):
        if len(proof) == 0:
            return target_hash == merkle_root
        else:
            proof_hash = target_hash
            for x in range(len(proof)):
                try:
                    # the sibling is a left node
                    proof_hash = self.hash_function(proof[x]['left'] + proof_hash).digest()
                except:
                    # the sibling is a right node
                    proof_hash = self.hash_function(proof_hash + proof[x]['right']).digest()
            return proof_hash == merkle_root


if __name__ == "__main__":
    mt = MerkleTools()
    mt.add_leaf("tierion")
    mt.add_leaf(["bitcoin", "blockchain"])
    assert mt.get_leaf_count() == 3
    assert mt.is_ready == False
    mt.make_tree()
    assert mt.is_ready == True
    print "root:", mt.get_merkle_root().encode('hex')
    print mt.get_proof(1)
    print mt.validate_proof(mt.get_proof(1), mt.get_leaf(1), mt.get_merkle_root())
